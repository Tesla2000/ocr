from pathlib import Path

from pydantic import BaseModel


class ImageFile(BaseModel):
    path: Path

    @property
    def output_path(self) -> Path:
        return self.path.with_suffix(".txt")


class OCRResult(BaseModel):
    image_file: ImageFile
    extracted_text: str
    success: bool
    error_message: str = ""
