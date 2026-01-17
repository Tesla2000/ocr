import asyncio
from asyncio import Semaphore
from collections.abc import Sequence

from ocr.models import ImageFile
from ocr.models import OCRResult
from ocr.vision_client import VisionClient
from pydantic import BaseModel
from pydantic import PositiveInt


class TextExtractor(BaseModel):
    vision_client: VisionClient
    n_tasks: PositiveInt = 12
    return_exceptions: bool = False

    async def extract_from_images(
        self, images: Sequence[ImageFile]
    ) -> tuple[OCRResult, ...]:
        tasks = [self._extract_single(image) for image in images]
        async with Semaphore(self.n_tasks):
            results = tuple(
                await asyncio.gather(
                    *tasks, return_exceptions=self.return_exceptions
                )
            )
        if self.return_exceptions:
            results = tuple(
                (
                    OCRResult(
                        image_file=image,
                        extracted_text="",
                        success=False,
                        error_message=str(result),
                    )
                    if not isinstance(result, OCRResult)
                    else result
                )
                for result, image in zip(results, images)
            )
        return results

    async def _extract_single(self, image: ImageFile) -> OCRResult:
        text = await asyncio.to_thread(
            self.vision_client.extract_text, image.path
        )
        return OCRResult(image_file=image, extracted_text=text, success=True)
