from typing import Annotated
from typing import Union

from ocr.output.transfomations.llm_cleanup.provider.anthropic import Anthropic
from ocr.output.transfomations.llm_cleanup.provider.openai import OpenAI
from pydantic import Field

AnyProvider = Annotated[Union[OpenAI, Anthropic], Field(discriminator="type")]
