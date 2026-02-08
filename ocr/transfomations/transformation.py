from abc import ABC
from abc import abstractmethod

from pydantic import BaseModel
from pydantic import ConfigDict


class Transformation(BaseModel, ABC):
    model_config = ConfigDict(extra="forbid")
    type: str

    @abstractmethod
    async def transform(self, text: str) -> str:
        pass
