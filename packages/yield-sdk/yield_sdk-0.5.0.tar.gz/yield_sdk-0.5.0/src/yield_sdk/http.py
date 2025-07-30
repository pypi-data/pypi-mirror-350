from collections.abc import Mapping
import typing as t
import typing_extensions as tx


if t.TYPE_CHECKING:
    import httpx
    import urllib3


# Status code, headers, body
Response: t.TypeAlias = tuple[int, Mapping[str, str], str]


class SyncHTTPClient(t.Protocol):
    def close(self) -> None:
        ...

    def request(self, method: str, url: str, headers: Mapping[str, str] | None, body: str | None) -> Response:
        ...


class Urllib3HTTPClient(SyncHTTPClient):
    _http: "urllib3.PoolManager"

    def __init__(self, pool_manager: "urllib3.PoolManager"):
        self._http = pool_manager

    @tx.override
    def close(self) -> None:
        pass # not necessary

    @tx.override
    def request(self, method: str, url: str, headers: Mapping[str, str] | None, body: str | None) -> Response:
        # explicitly encode body to bytes because older versions of urllib3 used a different encoding by default
        response = self._http.request(method, url, headers=headers, body=body.encode() if body is not None else None)

        return (response.status, response.headers, response.data.decode())


class HttpxSyncHTTPClient(SyncHTTPClient):
    _http: "httpx.Client"

    def __init__(self, client: "httpx.Client"):
        self._http = client

    @tx.override
    def close(self) -> None:
        self._http.close()

    @tx.override
    def request(self, method: str, url: str, headers: Mapping[str, str] | None, body: str | None) -> Response:
        response = self._http.request(method, url, headers=headers, content=body)

        return (response.status_code, response.headers, response.text)


class AsyncHTTPClient(t.Protocol):
    async def aclose(self) -> None:
        ...

    async def request(self, method: str, url: str, headers: Mapping[str, str] | None, body: str | None) -> Response:
        ...
