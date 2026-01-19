from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from ocr.output._base import Output


class CombinedOutput(Output):
    type: Literal["combined"] = "combined"
    file: Path

    async def save_results(self, results: Iterable[str]) -> None:
        combined_text = "\n".join(results)
        cleaned_text = await self.text_cleanup.cleanup_text(combined_text)
        self.file.parent.mkdir(exist_ok=True, parents=True)
        self.file.write_text(cleaned_text)
