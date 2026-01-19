from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from ocr.output._base import Output


class SeparateOutput(Output):
    type: Literal["separate"] = "separate"
    output_directory: Path

    async def save_results(self, results: Iterable[str]) -> None:
        self.output_directory.mkdir(parents=True, exist_ok=True)
        for index, result in enumerate(results, 1):
            output_path = (self.output_directory / str(index)).with_suffix(
                ".txt"
            )
            output_path.write_text(result, encoding="utf-8")
