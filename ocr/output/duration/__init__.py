import logging
from typing import Annotated
from typing import TypeAlias
from typing import Union

from ocr.output.duration._base import DurationCalculator
from ocr.output.duration.default import DefaultDurationCalculator
from pydantic import Field

_logger = logging.getLogger(__name__)
AnyDurationCalculator: TypeAlias = Annotated[
    Union[DefaultDurationCalculator],
    Field(discriminator="type"),
]
__all__ = [
    "AnyDurationCalculator",
    "DurationCalculator",
    "DefaultDurationCalculator",
]
try:
    from ocr.output.duration.frequency import FrequencyDurationCalculator

    AnyDurationCalculator = Annotated[  # type: ignore[assignment, misc]
        Union[AnyDurationCalculator, FrequencyDurationCalculator],
        Field(discriminator="type"),
    ]
    __all__.append("FrequencyDurationCalculator")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use frequency duration calculator is not installed, frequency duration is disabled.\n{e}"
    )
