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
    _client: AsyncOpenAI

    def model_post_init(self, context: Any, /) -> None:
        self._client = AsyncOpenAI(
            api_key=self.openai_api_key.get_secret_value(),
            timeout=self.timeout,
        )

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
        stream = await self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": text},
            ],
            stream=True,
        )
        chunks = []
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                chunks.append(chunk.choices[0].delta.content)
        return "".join(chunks)
