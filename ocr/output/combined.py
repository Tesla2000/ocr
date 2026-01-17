from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from ocr.models import OCRResult
from ocr.output._base import Output


class CombinedOutput(Output):
    type: Literal["combined"] = "combined"
    output_file: Path

    def save_results(self, results: Iterable[OCRResult]) -> None:
        self.output_file.parent.mkdir(exist_ok=True, parents=True)
        self.output_file.write_text(
            "\n".join(
                result.extracted_text for result in results if result.success
            )
        )
