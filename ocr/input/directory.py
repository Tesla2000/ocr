import os.path
from pathlib import Path
from typing import Annotated
from typing import Literal

from ocr.input._base import Input
from pydantic import AfterValidator


def _validate_path(path: Path) -> Path:
    if not path.exists():
        raise ValueError(f"Input directory does not exist: {path}")
    if not path.is_dir():
        raise ValueError(f"Input path is not a directory: {path}")
    return path


class DirectoryInput(Input):
    type: Literal["directory"] = "directory"
    input_directory: Annotated[Path, AfterValidator(_validate_path)]

    def get_images(self) -> tuple[Path, ...]:
        return tuple(
            file_path
            for file_path in sorted(
                (
                    file_path
                    for file_path in self.input_directory.iterdir()
                    if file_path.suffix.lower() in self.supported_extensions
                ),
                key=os.path.getmtime,
            )
        )
