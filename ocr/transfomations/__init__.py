import logging
from typing import Annotated
from typing import TypeAlias
from typing import Union

from ocr.transfomations.duplicate_long_words import DuplicateLongWords
from ocr.transfomations.join_words_moving_center import JoinWordsMovingCenter
from ocr.transfomations.transformation import Transformation
from pydantic import Field

_logger = logging.getLogger(__name__)
AnyTransformation: TypeAlias = Annotated[
    Union[DuplicateLongWords, JoinWordsMovingCenter],
    Field(discriminator="type"),
]
__all__ = [
    "Transformation",
    "DuplicateLongWords",
    "JoinWordsMovingCenter",
    "AnyTransformation",
]
try:
    from ocr.transfomations.split_long_words import SplitLongWords

    AnyTransformation = Annotated[  # type: ignore[misc]
        Union[AnyTransformation, SplitLongWords], Field(discriminator="type")
    ]
    __all__.append("SplitLongWords")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use split long words is not installed, split long words is disabled.\n{e}"
    )
try:
    from ocr.transfomations.llm_cleanup import LLMCleanup

    AnyTransformation = Annotated[  # type: ignore[misc]
        Union[AnyTransformation, LLMCleanup], Field(discriminator="type")
    ]
    __all__.append("LLMCleanup")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use LLM cleanup is not installed, LLM cleanup is disabled.\n{e}"
    )
