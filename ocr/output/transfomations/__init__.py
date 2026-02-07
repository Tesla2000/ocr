from typing import Annotated
from typing import Union

from ocr.output.transfomations.duplicate_long_words import DuplicateLongWords
from ocr.output.transfomations.join_words_moving_center import (
    JoinWordsMovingCenter,
)
from ocr.output.transfomations.llm_cleanup.llm_cleanup import LLMCleanup
from ocr.output.transfomations.split_long_words import SplitLongWords
from ocr.output.transfomations.transformation import Transformation
from pydantic import Field

AnyTransformation = Annotated[
    Union[
        LLMCleanup,
        SplitLongWords,
        DuplicateLongWords,
        JoinWordsMovingCenter,
    ],
    Field(discriminator="type"),
]

__all__ = [
    "Transformation",
    "LLMCleanup",
    "SplitLongWords",
    "DuplicateLongWords",
    "JoinWordsMovingCenter",
    "AnyTransformation",
]
