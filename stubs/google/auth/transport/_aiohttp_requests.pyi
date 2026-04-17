from collections.abc import Mapping, Sequence

from google.auth import transport
from google.auth.transport import Response

class _CombinedResponse(transport.Response):
    def __init__(self, response: object) -> None: ...
    @property
    def status(self) -> int: ...
    @property
    def headers(self) -> Mapping[str, str]: ...
    @property
    def data(self) -> bytes: ...
    async def raw_content(self) -> bytes: ...
    async def content(self) -> bytes: ...

class _Response(transport.Response):
    def __init__(self, response: object) -> None: ...
    @property
    def status(self) -> int: ...
    @property
    def headers(self) -> Mapping[str, str]: ...
    @property
    def data(self) -> bytes: ...

class Request(transport.Request):
    session: object

    def __init__(self, session: object | None = None) -> None: ...
    def __call__(
        self,
        url: str,
        method: str = "GET",
        body: bytes | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float | None = None,
        **kwargs: object,
    ) -> Response: ...

class AuthorizedSession:
    credentials: object

    def __init__(
        self,
        credentials: object,
        refresh_status_codes: Sequence[int] = ...,
        max_refresh_attempts: int = ...,
        refresh_timeout: float | None = None,
        auth_request: Request | None = None,
        auto_decompress: bool = False,
        **kwargs: object,
    ) -> None: ...
    async def request(
        self,
        method: str,
        url: str,
        data: object = None,
        headers: Mapping[str, str] | None = None,
        max_allowed_time: float | None = None,
        timeout: float | None = None,
        auto_decompress: bool = False,
        **kwargs: object,
    ) -> _Response: ...
