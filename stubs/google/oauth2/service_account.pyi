from typing import Any, Sequence
from google.auth.credentials import Credentials as BaseCredentials
from google.auth.transport import Request

class Credentials(BaseCredentials):
    @classmethod
    def from_service_account_file(
        cls,
        filename: str,
        *,
        scopes: Sequence[str] | None = None,
        **kwargs: Any,
    ) -> Credentials: ...
    def refresh(self, request: Request) -> None: ...
