from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from typing import Optional

from ocr.output.transfomations.llm_cleanup.provider.message import Message
from pydantic import BaseModel
from pydantic import PositiveFloat


class LLMProvider(BaseModel, ABC):
    type: str
    timeout: Optional[PositiveFloat] = None

    @abstractmethod
    async def clean(self, messages: Iterable[Message]) -> str:
        pass
