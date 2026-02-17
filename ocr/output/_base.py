from abc import ABC
from abc import abstractmethod

from ocr.transfomations import TransformationsApplier
from pydantic import ConfigDict


class Output(ABC, TransformationsApplier):
    model_config = ConfigDict(extra="forbid")
    type: str

    async def save_results(self, result: str) -> None:
        result = await self.apply_transformations(result)
        await self._save_results(result)

    @abstractmethod
    async def _save_results(self, result: str) -> None:
        pass
