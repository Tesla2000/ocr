from collections.abc import Iterable
from typing import Any
from typing import Literal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openai import AsyncOpenAI
from pydantic import SecretStr
from ocr.output.transfomations.llm_cleanup.provider._base import LLMProvider
from ocr.output.transfomations.llm_cleanup.provider.message import Message


class OpenAI(LLMProvider):
    type: Literal["openai"] = "openai"
    openai_api_key: SecretStr
    _client: "AsyncOpenAI"
    model: str = "gpt-5-nano"

    def model_post_init(self, context: Any, /) -> None:
        from openai import AsyncOpenAI

        self._client = AsyncOpenAI(
            api_key=self.openai_api_key.get_secret_value(),
            timeout=self.timeout,
        )

    async def clean(self, messages: Iterable[Message]) -> str:
        response = await self._client.chat.completions.create(
            model=self.model,
            messages=[m._asdict() for m in messages],
        )
        return response.choices[0].message.content
