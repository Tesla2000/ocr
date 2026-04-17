import abc
from collections.abc import Mapping
from typing import NamedTuple

from google.auth import external_account

class SubjectTokenSupplier(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_subject_token(self, context: object, request: object) -> str: ...

class _TokenContent(NamedTuple):
    content: str
    location: str

class _FileSupplier(SubjectTokenSupplier):
    def __init__(
        self, path: str, format_type: str, subject_token_field_name: str | None
    ) -> None: ...
    def get_subject_token(self, context: object, request: object) -> str: ...

class _UrlSupplier(SubjectTokenSupplier):
    def __init__(
        self,
        url: str,
        format_type: str,
        subject_token_field_name: str | None,
        headers: Mapping[str, str] | None,
    ) -> None: ...
    def get_subject_token(self, context: object, request: object) -> str: ...

class _X509Supplier(SubjectTokenSupplier):
    def __init__(
        self, trust_chain_path: str | None, leaf_cert_callback: object
    ) -> None: ...
    def get_subject_token(self, context: object, request: object) -> str: ...

class Credentials(external_account.Credentials, metaclass=abc.ABCMeta):
    def __init__(
        self,
        audience: str,
        subject_token_type: str,
        token_url: str = "https://sts.googleapis.com/v1/token",
        credential_source: Mapping[str, object] | None = None,
        subject_token_supplier: SubjectTokenSupplier | None = None,
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
    def refresh(self, request: object) -> None: ...
