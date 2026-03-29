from pathlib import Path
from typing import Literal

from ocr.input.google_drive import GoogleDriveInput


class GoogleDriveDirectoryInput(GoogleDriveInput):
    type: Literal["google-drive-directory"] = "google-drive-directory"

    def get_images(self) -> tuple[Path, ...]:
        query = f"'{self.directory_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = (
            self._service.files()
            .list(
                q=query,
                fields="files(id, name, modifiedTime)",
                orderBy="modifiedTime desc",
                pageSize=1,
            )
            .execute()
        )
        folders = results.get("files", ())
        if not folders:
            return ()
        most_recent_dir_id = folders[0]["id"]
        return GoogleDriveInput(
            **self.model_dump(exclude={"directory_id", "type"}),
            directory_id=most_recent_dir_id,
        ).get_images()
