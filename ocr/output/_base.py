from abc import ABC
from abc import abstractmethod

from pydantic import BaseModel
from pydantic import ConfigDict


class Output(ABC, BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str

    @abstractmethod
    async def save_results(self, result: str) -> None:
        pass
