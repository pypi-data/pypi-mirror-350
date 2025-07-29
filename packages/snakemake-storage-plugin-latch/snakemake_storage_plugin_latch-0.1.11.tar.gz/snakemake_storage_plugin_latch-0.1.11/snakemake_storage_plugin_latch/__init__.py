import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, List, Optional, ParamSpec, TypeVar, cast
from urllib.parse import urlparse

import dateutil.parser as dp
import gql
from gql.transport.requests import RequestsHTTPTransport
from latch_persistence import LatchPersistence
from snakemake_interface_storage_plugins.io import (
    IOCacheStorageInterface,
    Mtime,
    get_constant_prefix,
)
from snakemake_interface_storage_plugins.settings import StorageProviderSettingsBase
from snakemake_interface_storage_plugins.storage_object import (
    StorageObjectGlob,
    StorageObjectRead,
    StorageObjectWrite,
)
from snakemake_interface_storage_plugins.storage_provider import (
    ExampleQuery,
    Operation,
    QueryType,
    StorageProviderBase,
    StorageQueryValidationResult,
)

P = ParamSpec("P")
T = TypeVar("T")


def with_retry(max_retries: int = 3):
    def decorator(f: Callable[P, T]) -> Callable[P, T]:
        def decorated(*args: P.args, **kwargs: P.kwargs) -> T:
            retries = 0
            while True:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    retries += 1

                    if retries >= max_retries:
                        raise e

        return decorated

    return decorator


@dataclass
class StorageProviderSettings(StorageProviderSettingsBase): ...


class LatchPathValidationException(ValueError): ...


class AuthenticationError(RuntimeError): ...


def get_root(p: Path) -> str:
    if p == Path("/") or p.match("/*"):
        return p.name

    return get_root(p.parent)


expr = re.compile(r"^/ldata")


# idempotent
def to_latch_url(path: str) -> str:
    return expr.sub("latch:/", path)


def is_ldata_path(path: str) -> bool:
    return get_root(Path(path).resolve()) == "ldata"


@dataclass
class LatchPath:
    domain: str
    path: str

    @classmethod
    def parse(cls, path: str):
        url = to_latch_url(path)
        parsed = urlparse(url)

        if parsed.scheme != "latch":
            raise LatchPathValidationException(f"invalid latch path: {url}")

        return cls(parsed.netloc, parsed.path)

    def local_suffix(self) -> str:
        if self.domain == "":
            return f"inferred{self.path}"

        return f"{self.domain}{self.path}"

    def unparse(self) -> str:
        return f"latch://{self.domain}{self.path}"

    def __str__(self):
        return self.unparse()

    def __repr__(self):
        return f"LatchPath({repr(self.domain)}, {repr(self.path)})"


class StorageProvider(StorageProviderBase):
    def __post_init__(self):
        auth_header: Optional[str] = None

        token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID", "")
        if token != "":
            auth_header = f"Latch-Execution-Token {token}"

        if auth_header is None:
            token_path = Path.home() / ".latch" / "token"
            if token_path.exists():
                auth_header = f"Latch-SDK-Token {token_path.read_text().strip()}"

        if auth_header is None:
            raise AuthenticationError(
                "Unable to find credentials to connect to gql server, aborting"
            )

        url = (
            f"https://vacuole.{os.environ.get('LATCH_SDK_DOMAIN', 'latch.bio')}/graphql"
        )

        self.gql = gql.Client(
            transport=RequestsHTTPTransport(
                url=url, headers={"Authorization": auth_header}, retries=5, timeout=90
            )
        )
        self.lp = LatchPersistence()

    @classmethod
    def example_queries(cls) -> List[ExampleQuery]:
        """Return valid example queries (at least one) with description."""
        return [
            ExampleQuery("latch://123.account/hello", "basic latch path", QueryType.ANY)
        ]

    def rate_limiter_key(self, query: str, operation: Operation) -> Any:
        """Return a key for identifying a rate limiter given a query and an operation.

        This is used to identify a rate limiter for the query.
        E.g. for a storage provider like http that would be the host name.
        For s3 it might be just the endpoint URL.
        """
        try:
            return LatchPath.parse(query).domain
        except LatchPathValidationException:
            return "local"

    def default_max_requests_per_second(self) -> float:
        """Return the default maximum number of requests per second for this storage
        provider."""

        return 10

    def use_rate_limiter(self) -> bool:
        """Return False if no rate limiting is needed for this provider."""

        return False

    @classmethod
    def is_valid_query(cls, query: str) -> StorageQueryValidationResult:
        """Return whether the given query is valid for this storage provider."""

        valid: bool = True
        reason: Optional[str] = None

        if is_ldata_path(query):
            try:
                LatchPath.parse(query)
            except LatchPathValidationException as e:
                valid = False
                reason = str(e)

        return StorageQueryValidationResult(query, valid, reason)


@dataclass
class LatchFileAttrs:
    exists: bool
    type: Optional[str]
    size: Optional[int]
    modify_time: Optional[float]


class StorageObject(StorageObjectRead, StorageObjectWrite, StorageObjectGlob):
    def __post_init__(self):
        self.provider = cast(StorageProvider, self.provider)
        self.is_remote = is_ldata_path(self.query)

        if self.is_remote:
            self.path = LatchPath.parse(self.query)
        else:
            self.path = Path(self.query)

        self.successfully_stored = False

    @with_retry()
    def _get_file_attrs(self) -> LatchFileAttrs:
        if not self.is_remote:
            if not self.path.exists():
                return LatchFileAttrs(False, None, None, None)

            typ = "obj" if self.path.is_file() else "dir"
            stat = self.path.stat()
            return LatchFileAttrs(True, typ, stat.st_size, stat.st_mtime)

        res = self.provider.gql.execute(
            gql.gql(
                """
                query GetFileAttrs($argPath: String!) {
                    ldataResolvePathToNode(path: $argPath) {
                        path
                        ldataNode {
                            finalLinkTarget {
                                id
                                type
                                pending
                                removed
                                ldataObjectMeta {
                                    contentSize
                                    modifyTime
                                }
                            }
                        }
                    }
                }
                """
            ),
            {"argPath": str(self.path)},
        )["ldataResolvePathToNode"]

        if res is None or res["ldataNode"] is None:
            raise AuthenticationError(
                f"latch path {self.path} either does not exist or signer lacks permission to view it"
            )

        flt = res["ldataNode"]["finalLinkTarget"]

        exists = (
            not flt["removed"]
            and not flt["pending"]
            and (res["path"] is None or res["path"] == "")
        )

        if not exists:
            return LatchFileAttrs(False, None, None, None)

        size = None
        modify_time = None

        meta = flt["ldataObjectMeta"]
        if meta is not None:
            size = meta["contentSize"]
            if size is not None:
                size = int(size)

            modify_time = meta["modifyTime"]
            if modify_time is not None:
                modify_time = dp.isoparse(modify_time).timestamp()

        return LatchFileAttrs(exists, flt["type"].lower(), size, modify_time)

    async def inventory(self, cache: IOCacheStorageInterface):
        """From this file, try to find as much existence and modification date
        information as possible. Only retrieve that information that comes for free
        given the current object.
        """

        attrs = self._get_file_attrs()

        cache.exists_in_storage[self.cache_key()] = attrs.exists

        if attrs.size is not None:
            cache.size[self.cache_key()] = attrs.size

        if attrs.modify_time is not None:
            cache.mtime[self.cache_key()] = Mtime(storage=attrs.modify_time)

    def get_inventory_parent(self) -> Optional[str]:
        """Return the parent directory of this object."""

        return None

    def local_suffix(self) -> str:
        """Return a unique suffix for the local path, determined from self.query."""
        if self.is_remote:
            return self.path.local_suffix()

        return str(self.path.resolve())

    def cleanup(self):
        """Perform local cleanup of any remainders of the storage object."""
        pass

    def exists(self) -> bool:
        if self.successfully_stored:
            return True

        return self._get_file_attrs().exists

    def mtime(self) -> float:
        mtime = self._get_file_attrs().modify_time
        if mtime is not None:
            return mtime

        return 0

    def size(self) -> int:
        size = self._get_file_attrs().size
        if size is not None:
            return size

        return 0

    @with_retry()
    def retrieve_object(self):
        if not self.is_remote:
            return

        local = self.local_path().resolve()
        if self._get_file_attrs().type != "obj":
            self.provider.lp.download_directory(str(self.path), str(local))
            return

        self.provider.lp.download(str(self.path), str(local))

    def store_object(self):
        self._store_object()
        self.successfully_stored = True

    @with_retry()
    def _store_object(self):
        if not self.is_remote:
            return

        local = self.local_path().resolve()
        if local.is_dir():
            self.provider.lp.upload_directory(str(local), str(self.path))
            return

        self.provider.lp.upload(str(local), str(self.path))

    def remove(self):
        # todo(ayush): not implementing for now bc idk how i feel about letting snakemake kill things
        ...

    def list_candidate_matches(self) -> Iterable[str]:
        """Return a list of candidate matches in the storage for the query."""

        # This is used by glob_wildcards() to find matches for wildcards in the query.
        # The method has to return concretized queries without any remaining wildcards.
        # Use snakemake_executor_plugins.io.get_constant_prefix(self.query) to get the
        # prefix of the query before the first wildcard.

        prefix = get_constant_prefix(str(self.path))

        if not self.is_remote:
            for res in Path(prefix).glob("*"):
                yield str(res)

            return

        res = self.provider.gql.execute(
            gql.gql(
                """
                query SnakemakeGlobs($argPath: String!) {
                    ldataGetDescendants(argPath: $argPath) {
                        nodes {
                            id
                            path
                        }
                    }
                }
                """,
            ),
            {"argPath": prefix},
        )["ldataGetDescendants"]

        if res is None:
            raise AuthenticationError(
                f"latch path {self.path} either does not exist or signer lacks permission to view it"
            )

        for node in res["nodes"]:
            yield node["path"]
