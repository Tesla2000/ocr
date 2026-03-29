import logging
from typing import Annotated
from typing import TYPE_CHECKING
from typing import TypeAlias
from typing import Union

from ocr.output.duration._base import DurationCalculator
from ocr.output.duration.default import DefaultDurationCalculator
from pydantic import Field

__all__ = [
    "AnyDurationCalculator",
    "DurationCalculator",
    "DefaultDurationCalculator",
]
if TYPE_CHECKING:
    from ocr.output.duration.frequency import FrequencyDurationCalculator

    AnyDurationCalculator: TypeAlias = Annotated[
        Union[
            DefaultDurationCalculator,
            FrequencyDurationCalculator,
        ],
        Field(discriminator="type"),
    ]
else:
    _logger = logging.getLogger(__name__)
    _calculators: list[type[DurationCalculator]] = [DefaultDurationCalculator]
    try:
        from ocr.output.duration.frequency import FrequencyDurationCalculator

        _calculators.append(FrequencyDurationCalculator)
        __all__.append("FrequencyDurationCalculator")
    except ImportError as e:
        _logger.warning(
            f"Package necessary to use frequency duration calculator is not installed, frequency duration is disabled.\n{e}"
        )
    AnyDurationCalculator = Annotated[
        Union.__getitem__(tuple(_calculators)),
        Field(discriminator="type"),
    ]
