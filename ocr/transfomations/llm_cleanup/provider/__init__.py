import logging
from typing import Annotated
from typing import TYPE_CHECKING
from typing import TypeAlias
from typing import Union

from ocr.transfomations.llm_cleanup.provider._base import LLMProvider
from pydantic import Field

if TYPE_CHECKING:
    from ocr.transfomations.llm_cleanup.provider.anthropic import Anthropic
    from ocr.transfomations.llm_cleanup.provider.openai import OpenAI

    AnyProvider: TypeAlias = Annotated[
        Union[Anthropic, OpenAI],
        Field(discriminator="type"),
    ]
else:
    _logger = logging.getLogger(__name__)
    __all__ = ["AnyProvider"]
    _providers: list[type[LLMProvider]] = []
    try:
        from ocr.transfomations.llm_cleanup.provider.anthropic import (
            Anthropic,
        )

        _providers.append(Anthropic)
        __all__.append("Anthropic")
    except ImportError as e:
        _logger.warning(
            f"Package necessary to use Anthropic provider is not installed, Anthropic is disabled.\n{e}"
        )
    try:
        from ocr.transfomations.llm_cleanup.provider.openai import OpenAI

        _providers.append(OpenAI)
        __all__.append("OpenAI")
    except ImportError as e:
        _logger.warning(
            f"Package necessary to use OpenAI provider is not installed, OpenAI is disabled.\n{e}"
        )
    if not _providers:
        raise ImportError(
            "No LLM providers available. Install anthropic or openai."
        )
    AnyProvider = Annotated[
        Union.__getitem__(_providers), Field(discriminator="type")
    ]
