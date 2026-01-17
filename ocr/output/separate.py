from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from ocr.models import OCRResult
from ocr.output._base import Output


class SeparateOutput(Output):
    type: Literal["separate"] = "separate"
    output_directory: Path

    def save_results(self, results: Iterable[OCRResult]) -> None:
        self.output_directory.mkdir(parents=True, exist_ok=True)
        for result in results:
            if not result.success:
                continue
            output_path = (
                self.output_directory / result.image_file.output_path.name
            ).with_suffix(".txt")
            output_path.write_text(result.extracted_text, encoding="utf-8")
