from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from ocr.models import OCRResult
from ocr.services.writers._writer import Writer


class CombinedWriter(Writer):
    type: Literal["combined"] = "combined"
    output_file: Path

    def write_results(self, results: Iterable[OCRResult]) -> None:
        self.output_file.parent.mkdir(exist_ok=True, parents=True)
        self.output_file.write_text(
            "\n".join(
                result.extracted_text for result in results if result.success
            )
        )
