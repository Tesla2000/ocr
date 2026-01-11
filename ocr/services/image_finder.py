from pathlib import Path
from typing import Annotated

from ocr.models import ImageFile
from pydantic import AfterValidator
from pydantic import BaseModel


def _validate_path(path: Path) -> Path:
    if not path.exists():
        raise ValueError(f"Input directory does not exist: {path}")
    if not path.is_dir():
        raise ValueError(f"Input path is not a directory: {path}")
    return path


class ImageFinder(BaseModel):
    input_directory: Annotated[Path, AfterValidator(_validate_path)]
    supported_extensions: tuple[str, ...] = (
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tiff",
        ".tif",
        ".webp",
    )

    def find_images(self) -> tuple[ImageFile, ...]:
        return tuple(
            ImageFile(path=file_path)
            for file_path in self.input_directory.iterdir()
            if file_path.suffix.lower() in self.supported_extensions
        )
