import abc
from collections.abc import Mapping
from dataclasses import dataclass

from google.auth import external_account

@dataclass
class AwsSecurityCredentials:
    access_key_id: str
    secret_access_key: str
    session_token: str | None = None

class RequestSigner:
    def __init__(self, region_name: str) -> None: ...
    def get_request_options(
        self,
        aws_security_credentials: AwsSecurityCredentials,
        url: str,
        method: str,
        request_payload: str = "",
        additional_headers: Mapping[str, str] | None = None,
    ) -> Mapping[str, str]: ...

class AwsSecurityCredentialsSupplier(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_aws_security_credentials(
        self, context: object, request: object
    ) -> AwsSecurityCredentials: ...
    @abc.abstractmethod
    def get_aws_region(self, context: object, request: object) -> str: ...

class _DefaultAwsSecurityCredentialsSupplier(AwsSecurityCredentialsSupplier):
    def __init__(self, credential_source: Mapping[str, object]) -> None: ...
    def get_aws_security_credentials(
        self, context: object, request: object
    ) -> AwsSecurityCredentials: ...
    def get_aws_region(self, context: object, request: object) -> str: ...

class Credentials(external_account.Credentials, metaclass=abc.ABCMeta):
    def __init__(
        self,
        audience: str,
        subject_token_type: str,
        token_url: str = "https://sts.googleapis.com/v1/token",
        credential_source: Mapping[str, object] | None = None,
        aws_security_credentials_supplier: (
            AwsSecurityCredentialsSupplier | None
        ) = None,
        *args: object,
        **kwargs: object,
    ) -> None: ...
    def retrieve_subject_token(self, request: object) -> str: ...
    @classmethod
    def from_info(
        cls, info: Mapping[str, object], **kwargs: object
    ) -> Credentials: ...
    @classmethod
    def from_file(cls, filename: str, **kwargs: object) -> Credentials: ...
