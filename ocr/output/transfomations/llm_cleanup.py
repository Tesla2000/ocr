from logging import CRITICAL
from logging import DEBUG
from logging import ERROR
from logging import getLogger
from logging import INFO
from logging import Logger
from logging import NOTSET
from logging import WARNING
from typing import Any
from typing import Literal

from ocr.output.transfomations.transformation import Transformation
from openai import AsyncOpenAI
from pydantic import PositiveFloat
from pydantic import SecretStr


class LLMCleanup(Transformation):
    type: Literal["llm-cleanup"] = "llm-cleanup"
    openai_api_key: SecretStr
    model: str = "gpt-4.1-nano"
    timeout: PositiveFloat = 30.0
    logging_level: Literal[CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET] = (
        INFO
    )
    _client: AsyncOpenAI
    _logger: Logger

    def model_post_init(self, context: Any, /) -> None:
        self._client = AsyncOpenAI(
            api_key=self.openai_api_key.get_secret_value(),
            timeout=self.timeout,
        )
        self._logger = getLogger("llm_cleanup")
        self._logger.setLevel(self.logging_level)

    system_prompt: str = """You are a text cleanup assistant. Your task is to:
1. Fix OCR mistakes and typos
2. Remove page numbers
3. Remove chapter titles and headers
4. Remove footers and repeated elements
5. Preserve the actual content and maintain proper paragraph structure
6. Fix formatting issues

Return only the cleaned text without any explanations or metadata. You will be given text in polish

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
    """

    async def transform(self, text: str) -> str:
        response = await self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": text},
            ],
        )
        cleaned_content = response.choices[0].message.content
        self._logger.debug(
            f"Cleaned data of length {len(text)} to {len(cleaned_content)} characters"
        )
        return cleaned_content
