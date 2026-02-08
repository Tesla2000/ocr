from io import BytesIO
from pathlib import Path
from typing import Annotated
from typing import Any
from typing import Literal

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from ocr.output._base import Output
from pydantic import AfterValidator


def _validate_credentials_path(path: Path) -> Path:
    if not path.exists():
        raise ValueError(f"Credentials file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Credentials path is not a file: {path}")
    return path


class GoogleDriveOutput(Output):
    type: Literal["google-drive"] = "google-drive"
    credentials_path: Annotated[
        Path, AfterValidator(_validate_credentials_path)
    ]
    directory_id: str
    filename: str
    _service: Any = None

    def model_post_init(self, context: Any, /) -> None:
        credentials = Credentials.from_service_account_file(  # type: ignore[no-untyped-call]
            str(self.credentials_path),
            scopes=["https://www.googleapis.com/auth/drive.file"],
        )
        self._service = build("drive", "v3", credentials=credentials)

    async def save_results(self, result: str) -> None:
        file_metadata = {
            "name": self.filename,
            "parents": [self.directory_id],
        }
        media = MediaIoBaseUpload(
            BytesIO(result.encode("utf-8")),
            mimetype="text/plain",
            resumable=True,
        )
        self._service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id",
        ).execute()
