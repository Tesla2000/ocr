from abc import ABC
from abc import abstractmethod
from pathlib import Path

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
    def get_images(self) -> tuple[Path, ...]:
        pass
