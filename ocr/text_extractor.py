import asyncio
from asyncio import Semaphore
from collections.abc import Iterable
from pathlib import Path

from ocr.vision_client import VisionClient
from pydantic import BaseModel
from pydantic import PositiveInt


class TextExtractor(BaseModel):
    vision_client: VisionClient
    n_tasks: PositiveInt = 12
    return_exceptions: bool = False

    async def extract_from_images(
        self, images: Iterable[Path]
    ) -> tuple[str, ...]:
        tasks = [self._extract_single(image) for image in images]
        async with Semaphore(self.n_tasks):
            return tuple(await asyncio.gather(*tasks))

    async def _extract_single(self, image_path: Path) -> str:
        text = await asyncio.to_thread(
            self.vision_client.extract_text, image_path
        )
        return text
