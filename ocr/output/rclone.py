import os
from pathlib import Path
from typing import Literal

from ocr.output import CombinedOutput
from ocr.output._base import Output


class RClone(Output):
    type: Literal["rclone"] = "rclone"
    shared_directory: Path
    output_path: str
    local_output: CombinedOutput

    async def _save_results(self, result: str) -> None:
        await self.local_output.save_results(result)
        os.system(f"rclone copy {self.shared_directory} {self.output_path}")
