import os
from collections.abc import Collection
from pathlib import Path
from typing import Literal

from ocr.output.local_ouptup import AnyLocalOutput
from ocr.output.local_ouptup._base import Output
from ocr.output.transfomations import AnyTransformation
from pydantic import Field


class RClone(Output):
    type: Literal["rclone"] = "rclone"
    shared_directory: Path
    output_path: str
    local_output: AnyLocalOutput
    transformations: list[AnyTransformation] = Field(
        default_factory=list,
        max_length=0,
        description="Transformations don't apply on this level",
    )

    async def save_results(self, results: Collection[str]) -> None:
        await self.local_output.save_results(results)
        os.system(f"rclone copy {self.shared_directory} {self.output_path}")
