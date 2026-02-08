from collections.abc import Iterable
from typing import Annotated
from typing import Any
from typing import Literal

from ocr.output.transfomations.llm_cleanup.provider._base import LLMProvider
from ocr.output.transfomations.llm_cleanup.provider.message import Message
from openai import AsyncOpenAI
from pydantic import AfterValidator
from pydantic import SecretStr


def _validate_api_key(key: SecretStr) -> SecretStr:
    if not key.get_secret_value():
        raise ValueError("API key cannot be empty")
    return key


class OpenAI(LLMProvider):
    type: Literal["openai"] = "openai"
    openai_api_key: Annotated[SecretStr, AfterValidator(_validate_api_key)] = (
        SecretStr("")
    )
    _client: AsyncOpenAI
    model: str = "gpt-5-nano"

    def model_post_init(self, context: Any, /) -> None:
        self._client = AsyncOpenAI(
            api_key=self.openai_api_key.get_secret_value(),
            timeout=self.timeout,
        )

    async def clean(self, messages: Iterable[Message]) -> str:
        response = await self._client.chat.completions.create(
            model=self.model,
            messages=[m.as_dict() for m in messages],
        )
        content = response.choices[0].message.content
        if not isinstance(content, str):
            raise ValueError("OpenAI returned empty content")
        return content
