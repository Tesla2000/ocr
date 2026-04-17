import types
from collections.abc import Callable, Mapping, Sequence
from typing_extensions import Self

import requests
import requests.adapters
from google.auth import transport

class _RequestMethodsBase: ...

RequestMethods = _RequestMethodsBase
_LOGGER: object = None

class _Response(transport.Response):
    def __init__(self, response: object) -> None: ...
    @property
    def status(self) -> int: ...
    @property
    def headers(self) -> Mapping[str, str]: ...
    @property
    def data(self) -> bytes: ...

class TimeoutGuard:
    remaining_timeout: object

    def __init__(
        self,
        timeout: object,
        timeout_error_type: type[Exception] = requests.exceptions.Timeout,
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None: ...

class Request(transport.Request):
    http: object

    def __init__(self, http: object | None = None) -> None: ...
    def __del__(self) -> None: ...
    def __call__(
        self,
        url: str,
        method: str = "GET",
        body: bytes | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float | None = None,
        **kwargs: object,
    ) -> _Response: ...

class _MutualTlsAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, cert: bytes, key: bytes) -> None: ...
    def init_poolmanager(self, *args: object, **kwargs: object) -> None: ...
    def proxy_manager_for(self, *args: object, **kwargs: object) -> object: ...

class _MutualTlsOffloadAdapter(requests.adapters.HTTPAdapter):
    signer: object

    def __init__(self, enterprise_cert_file_path: str) -> None: ...
    def init_poolmanager(self, *args: object, **kwargs: object) -> None: ...
    def proxy_manager_for(self, *args: object, **kwargs: object) -> object: ...

class AuthorizedHttp(RequestMethods):
    http: object
    credentials: object

    def __init__(
        self,
        credentials: object,
        http: object | None = None,
        refresh_status_codes: Sequence[int] = ...,
        max_refresh_attempts: int = ...,
        default_host: str | None = None,
    ) -> None: ...
    def configure_mtls_channel(
        self,
        client_cert_callback: Callable[[], tuple[bytes, bytes]] | None = ...,
    ) -> bool: ...
    def urlopen(
        self,
        method: str,
        url: str,
        body: object = None,
        headers: object = None,
        **kwargs: object,
    ) -> _Response: ...
    def __enter__(self) -> object: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None: ...
    def __del__(self) -> None: ...
    @property
    def headers(self) -> Mapping[str, str]: ...
    @headers.setter
    def headers(self, value: Mapping[str, str]) -> None: ...
