from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from ocr.output._base import Output


class CombinedOutput(Output):
    type: Literal["combined"] = "combined"
    file: Path

    async def save_results(self, results: Iterable[str]) -> None:
        self.file.parent.mkdir(exist_ok=True, parents=True)
        self.file.write_text(
            await self._apply_transformations("\n".join(results))
        )
