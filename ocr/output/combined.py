from pathlib import Path
from typing import Literal

from ocr.output._base import Output


class CombinedOutput(Output):
    type: Literal["combined"] = "combined"
    path: Path

    async def _save_results(self, result: str) -> None:
        self.path.parent.mkdir(exist_ok=True, parents=True)
        self.path.write_text(result)
