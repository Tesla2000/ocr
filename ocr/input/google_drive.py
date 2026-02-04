from pathlib import Path
from tempfile import mkdtemp
from typing import Annotated
from typing import Any
from typing import Literal
from typing import TYPE_CHECKING

from google.oauth2.service_account import Credentials
from ocr.input._base import Input
from pydantic import AfterValidator

if TYPE_CHECKING:
    from googleapiclient.discovery import Resource


def _validate_credentials_path(path: Path) -> Path:
    if not path.exists():
        raise ValueError(f"Credentials file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Credentials path is not a file: {path}")
    return path


class GoogleDriveInput(Input):
    type: Literal["google-drive"] = "google-drive"
    credentials_path: Annotated[
        Path, AfterValidator(_validate_credentials_path)
    ]
    directory_id: str
    temp_directory: Path = Path(mkdtemp(dir="/dev/shm"))
    _service: "Resource"

    def model_post_init(self, context: Any, /) -> None:
        from googleapiclient.discovery import build

        credentials = Credentials.from_service_account_file(  # type: ignore[no-untyped-call]
            str(self.credentials_path),
            scopes=["https://www.googleapis.com/auth/drive.readonly"],
        )
        self._service = build("drive", "v3", credentials=credentials)

    def get_images(self) -> tuple[Path, ...]:
        from googleapiclient.http import MediaIoBaseDownload

        query = f"'{self.directory_id}' in parents and trashed=false"
        results = (
            self._service.files()
            .list(q=query, fields="files(id, name)", orderBy="name")
            .execute()
        )
        files = results.get("files", ())
        temp_dir = self.temp_directory
        temp_dir.mkdir(parents=True, exist_ok=True)
        image_files = []
        for file in files:
            file_name = file["name"]
            if not any(
                file_name.lower().endswith(ext)
                for ext in self.supported_extensions
            ):
                continue
            file_path = temp_dir / file_name
            request = self._service.files().get_media(fileId=file["id"])
            with file_path.open("wb") as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
            image_files.append(file_path)
        return tuple(image_files)
