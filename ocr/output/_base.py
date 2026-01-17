from abc import ABC
from abc import abstractmethod
from collections.abc import Collection

from ocr.models import OCRResult
from pydantic import BaseModel
from pydantic import ConfigDict


class Output(ABC, BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str

    @abstractmethod
    def save_results(self, results: Collection[OCRResult]) -> None:
        pass
