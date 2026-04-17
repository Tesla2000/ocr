import grpc

class AuthMetadataPlugin(grpc.AuthMetadataPlugin):
    def __init__(
        self,
        credentials: object,
        request: object,
        default_host: str | None = None,
    ) -> None: ...
    def __call__(self, context: object, callback: object) -> None: ...

def secure_authorized_channel(
    credentials: object,
    request: object,
    target: str,
    ssl_credentials: object = ...,
    client_cert_callback: object = ...,
    **kwargs: object,
) -> grpc.Channel: ...

class SslCredentials:
    def __init__(self) -> None: ...
    @property
    def ssl_credentials(self) -> object: ...
    @property
    def is_mtls(self) -> bool: ...
