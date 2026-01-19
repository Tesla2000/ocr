from abc import ABC
from abc import abstractmethod
from collections.abc import Collection

from ocr.text_cleanup import TextCleanup
from pydantic import BaseModel
from pydantic import ConfigDict


class Output(ABC, BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str
    text_cleanup: TextCleanup

    @abstractmethod
    async def save_results(self, results: Collection[str]) -> None:
        pass
