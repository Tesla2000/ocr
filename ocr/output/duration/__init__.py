from typing import Annotated
from typing import TypeAlias
from typing import Union

from ocr.output.duration._base import DurationCalculator
from ocr.output.duration.default import DefaultDurationCalculator
from pydantic import Field

AnyDurationCalculator: TypeAlias = Annotated[
    Union[DefaultDurationCalculator],
    Field(discriminator="type"),
]
__all__ = [
    "AnyDurationCalculator",
    "DurationCalculator",
    "DefaultDurationCalculator",
]
