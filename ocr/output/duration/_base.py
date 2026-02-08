from abc import ABC
from abc import abstractmethod

from pydantic import BaseModel
from pydantic import ConfigDict


class DurationCalculator(ABC, BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str

    @abstractmethod
    def calculate_duration(self, word: str) -> float:
        pass
