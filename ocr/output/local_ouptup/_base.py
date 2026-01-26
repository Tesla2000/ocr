from abc import ABC
from abc import abstractmethod
from collections.abc import Collection

from ocr.output.transfomations import AnyTransformation
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class Output(ABC, BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str
    transformations: list[AnyTransformation] = Field(default_factory=list)

    @abstractmethod
    async def save_results(self, results: Collection[str]) -> None:
        pass

    async def _apply_transformations(self, text: str) -> str:
        for transformation in self.transformations:
            text = await transformation.transform(text)
        return text
