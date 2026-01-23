from collections.abc import Iterable
from typing import Any
from typing import Literal
from typing import TYPE_CHECKING

from pydantic import PositiveInt

if TYPE_CHECKING:
    from anthropic import AsyncAnthropic
from pydantic import SecretStr
from ocr.output.transfomations.llm_cleanup.provider._base import LLMProvider
from ocr.output.transfomations.llm_cleanup.provider.message import Message


class Anthropic(LLMProvider):
    type: Literal["anthropic"] = "anthropic"
    anthropic_api_key: SecretStr
    _client: "AsyncAnthropic"
    model: str = "claude-haiku-4-5"
    max_tokens: PositiveInt = 64000

    def model_post_init(self, context: Any, /) -> None:
        from anthropic import AsyncAnthropic

        self._client = AsyncAnthropic(
            api_key=self.anthropic_api_key.get_secret_value(),
            timeout=self.timeout,
        )

    async def clean(self, messages: Iterable[Message]) -> str:
        messages_list = list(messages)
        system_messages = [m for m in messages_list if m.role == "system"]
        user_messages = [m for m in messages_list if m.role != "system"]
        system_content = (
            "\n\n".join(m.content for m in system_messages)
            if system_messages
            else None
        )
        response = await self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_content,
            messages=[
                {"role": m.role, "content": m.content} for m in user_messages
            ],
        )
        return response.content[0].text
