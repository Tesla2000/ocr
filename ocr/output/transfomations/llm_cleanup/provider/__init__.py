import logging
from typing import Annotated
from typing import Any
from typing import TypeAlias
from typing import Union

from pydantic import Field

_logger = logging.getLogger(__name__)
__all__ = ["AnyProvider"]
AnyProvider: TypeAlias = Any
try:
    from ocr.output.transfomations.llm_cleanup.provider.anthropic import (
        Anthropic,
    )

    AnyProvider = Annotated[Union[Anthropic], Field(discriminator="type")]  # type: ignore[misc]
    __all__.append("Anthropic")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use Anthropic provider is not installed, Anthropic is disabled.\n{e}"
    )
    AnyProvider = None  # type: ignore[misc]
try:
    from ocr.output.transfomations.llm_cleanup.provider.openai import OpenAI

    if AnyProvider is not None:
        AnyProvider = Annotated[  # type: ignore[misc]
            Union[AnyProvider, OpenAI], Field(discriminator="type")
        ]
    else:
        AnyProvider = Annotated[Union[OpenAI], Field(discriminator="type")]  # type: ignore[misc]
    __all__.append("OpenAI")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use OpenAI provider is not installed, OpenAI is disabled.\n{e}"
    )
if AnyProvider is None:
    raise ImportError(
        "No LLM providers available. Install anthropic or openai."
    )
