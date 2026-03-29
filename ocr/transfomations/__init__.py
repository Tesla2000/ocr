import logging
from typing import Annotated
from typing import TYPE_CHECKING
from typing import TypeAlias
from typing import Union

from ocr.transfomations.duplicate_long_words import DuplicateLongWords
from ocr.transfomations.join_words_moving_center import JoinWordsMovingCenter
from ocr.transfomations.transformation import Transformation
from pydantic import BaseModel
from pydantic import Field

__all__ = []
if TYPE_CHECKING:
    from ocr.transfomations.llm_cleanup import LLMCleanup
    from ocr.transfomations.split_long_words import SplitLongWords

    AnyTransformation: TypeAlias = Annotated[
        Union[
            DuplicateLongWords,
            JoinWordsMovingCenter,
            SplitLongWords,
            LLMCleanup,
        ],
        Field(discriminator="type"),
    ]
else:
    _logger = logging.getLogger(__name__)
    _transformations: list[type[Transformation]] = [
        DuplicateLongWords,
        JoinWordsMovingCenter,
    ]
    __all__ = [
        "Transformation",
        "DuplicateLongWords",
        "JoinWordsMovingCenter",
        "AnyTransformation",
    ]
    try:
        from ocr.transfomations.split_long_words import SplitLongWords

        _transformations.append(SplitLongWords)
        __all__.append("SplitLongWords")
    except ImportError as e:
        _logger.warning(
            f"Package necessary to use split long words is not installed, split long words is disabled.\n{e}"
        )
    try:
        from ocr.transfomations.llm_cleanup import LLMCleanup

        _transformations.append(LLMCleanup)
        __all__.append("LLMCleanup")
    except ImportError as e:
        _logger.warning(
            f"Package necessary to use LLM cleanup is not installed, LLM cleanup is disabled.\n{e}"
        )
    AnyTransformation = Annotated[
        Union.__getitem__(_transformations), Field(discriminator="type")
    ]


class TransformationsApplier(BaseModel):
    transformations: tuple[AnyTransformation, ...] = ()

    async def apply_transformations(self, text: str) -> str:
        for t in self.transformations:
            text = await t.transform(text)
        return text


__all__.append("TransformationsApplier")
