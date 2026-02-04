from enum import IntEnum
from logging import getLogger
from logging import INFO
from logging import Logger
from typing import Any
from typing import Literal

from ocr.output.transfomations.llm_cleanup.provider import Anthropic
from ocr.output.transfomations.llm_cleanup.provider import AnyProvider
from ocr.output.transfomations.llm_cleanup.provider.message import Message
from ocr.output.transfomations.transformation import Transformation
from pydantic import Field


class LogLevel(IntEnum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


class LLMCleanup(Transformation):
    type: Literal["llm-cleanup"] = "llm-cleanup"
    logging_level: LogLevel = LogLevel(INFO)
    llm_provider: AnyProvider = Field(default_factory=Anthropic)
    _logger: Logger

    def model_post_init(self, context: Any, /) -> None:
        self._logger = getLogger("llm_cleanup")
        self._logger.setLevel(self.logging_level)

    system_prompt: str = """You are a text cleanup assistant. Your task is to:
1. Fix OCR mistakes and typos
2. Remove page numbers
3. Remove chapter titles and headers
4. Remove footers and repeated elements
5. Preserve the actual content and maintain proper paragraph structure
6. Fix formatting issues
7. Keep original context intact don't skip any parts

Return only the cleaned text without any explanations or metadata. You will be given text in polish

EXAMPLE:
    Before:
    Łatwość poznawcza
    A powtarzajare de
    przez szata graficzna
    utorowana idea
    dobry nastrój
    5. Łatwość poznawcza
    uczucie prawdziwości
    ATWOŚC
    uczucie przyjemności
    uczucie larwości
    83
    na wiele
    Za kandym razem, kiedy to sobie uświadamiasz - a może nawet wte.
    kiedy sobie nie uświadamiasz - w twoim mózgu dokonują się
    operacie mające utrzymywać i aktualizować odpowiedzi
    wanych pytan: Czy dzieje się coś nowego? Czy coś mi grozi? Czy
    wko w porzadku? Czy nie trzeba zwrócić uwagi na coś innego?

    After:
    Za każdym razem, kiedy to sobie uświadamiasz - a może nawet wtedy
    kiedy sobie nie uświadamiasz - w twoim mózgu dokonują się
    operacie mające utrzymywać i aktualizować odpowiedzi
    ważnych pytań: Czy dzieje się coś nowego? Czy coś mi grozi? Czy
    wszystko w porządku? Czy nie trzeba zwrócić uwagi na coś innego?

Don't include example in response
    """

    async def transform(self, text: str) -> str:
        cleaned_content = await self.llm_provider.clean(
            messages=(
                Message("system", self.system_prompt),
                Message("user", text),
            ),
        )
        self._logger.debug(
            f"Cleaned data of length {len(text)} to {len(cleaned_content)} characters"
        )
        return cleaned_content
