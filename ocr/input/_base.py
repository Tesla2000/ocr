from abc import ABC
from abc import abstractmethod

from ocr.models import ImageFile
from pydantic import BaseModel
from pydantic import ConfigDict


class Input(BaseModel, ABC):
    model_config = ConfigDict(extra="forbid")
    type: str
    supported_extensions: tuple[str, ...] = (
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tiff",
        ".tif",
        ".webp",
    )

    @abstractmethod
    def get_images(self) -> tuple[ImageFile, ...]:
        pass
