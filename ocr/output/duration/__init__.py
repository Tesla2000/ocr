import logging
from typing import Annotated
from typing import TYPE_CHECKING
from typing import TypeAlias
from typing import Union

from ocr.output.duration._base import DurationCalculator
from ocr.output.duration.default import DefaultDurationCalculator
from pydantic import Field

if TYPE_CHECKING:
    from ocr.output.duration.frequency import FrequencyDurationCalculator
    from ocr.output.duration.transformer import TransformerDurationCalculator

    AnyDurationCalculator: TypeAlias = Annotated[
        Union[
            DefaultDurationCalculator,
            FrequencyDurationCalculator,
            TransformerDurationCalculator,
        ],
        Field(discriminator="type"),
    ]
else:
    _logger = logging.getLogger(__name__)
    _calculators: list[type[DurationCalculator]] = [DefaultDurationCalculator]
    __all__ = [
        "AnyDurationCalculator",
        "DurationCalculator",
        "DefaultDurationCalculator",
    ]
    try:
        from ocr.output.duration.frequency import FrequencyDurationCalculator

        _calculators.append(FrequencyDurationCalculator)
        __all__.append("FrequencyDurationCalculator")
    except ImportError as e:
        _logger.warning(
            f"Package necessary to use frequency duration calculator is not installed, frequency duration is disabled.\n{e}"
        )
    try:
        from ocr.output.duration.transformer import (
            TransformerDurationCalculator,
        )

        _calculators.append(TransformerDurationCalculator)
        __all__.append("TransformerDurationCalculator")
    except ImportError as e:
        _logger.warning(
            f"Package necessary to use transformer duration calculator is not installed, transformer duration is disabled.\n{e}"
        )
    AnyDurationCalculator = Annotated[
        Union.__getitem__(_calculators),
        Field(discriminator="type"),
    ]
