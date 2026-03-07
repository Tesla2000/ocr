from pathlib import Path
from tempfile import mkdtemp
from typing import Annotated
from typing import Literal

from ocr.input._base import Input
from pdf2image import convert_from_path
from pydantic import AfterValidator
from pydantic import PositiveInt


def _validate_pdf_path(path: Path) -> Path:
    if not path.exists():
        raise ValueError(f"PDF file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"PDF path is not a file: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"File is not a PDF: {path}")
    return path


class PdfInput(Input):
    type: Literal["pdf"] = "pdf"
    pdf_path: Annotated[Path, AfterValidator(_validate_pdf_path)]
    start_page: PositiveInt = 1
    number_of_pages: PositiveInt = 1
    temp_directory: Path = Path(mkdtemp(dir="/dev/shm"))

    def get_images(self) -> tuple[Path, ...]:
        last_page = self.start_page + self.number_of_pages - 1
        images = convert_from_path(
            self.pdf_path,
            first_page=self.start_page,
            last_page=last_page,
        )
        self.temp_directory.mkdir(parents=True, exist_ok=True)
        paths: list[Path] = []
        for i, image in enumerate(images):
            image_path = (
                self.temp_directory / f"page_{self.start_page + i}.png"
            )
            image.save(str(image_path), "PNG")
            paths.append(image_path)
        return tuple(paths)
