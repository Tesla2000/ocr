import logging
from typing import Annotated
from typing import TYPE_CHECKING
from typing import Union

from ocr.output.combined import CombinedOutput
from ocr.output.rclone import RClone
from ocr.output.timed import TimedOutput
from pydantic import Field

_logger = logging.getLogger(__name__)
_output_types: list[type] = [CombinedOutput, TimedOutput, RClone]
_timed_output_types: list[type] = [TimedOutput]
__all__ = [
    "AnyOutput",
    "AnyTimedOutput",
    "CombinedOutput",
    "TimedOutput",
    "RClone",
]
try:
    from ocr.output.google_drive import GoogleDriveOutput

    _output_types.append(GoogleDriveOutput)
    __all__.append("GoogleDriveOutput")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use Google Drive output is not installed, Google Drive output is disabled.\n{e}"
    )
try:
    from ocr.output.timed_split import TimedSplitOutput

    _output_types.append(TimedSplitOutput)
    _timed_output_types.append(TimedSplitOutput)
    __all__.append("TimedSplitOutput")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use timed split output is not installed, timed split output is disabled.\n{e}"
    )
if TYPE_CHECKING:
    AnyTimedOutput = Annotated[
        Union[TimedOutput, TimedSplitOutput],
        Field(discriminator="type"),
    ]
else:
    AnyTimedOutput = Annotated[
        Union.__getitem__(tuple(_timed_output_types)),
        Field(discriminator="type"),
    ]
try:
    from ocr.output.timed_viewer import TimedWordsViewer

    TimedWordsViewer.model_rebuild()
    _output_types.append(TimedWordsViewer)
    __all__.append("TimedWordsViewer")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use timed viewer output is not installed, timed viewer output is disabled.\n{e}"
    )
if TYPE_CHECKING:
    AnyOutput = Annotated[
        Union[
            CombinedOutput,
            TimedOutput,
            RClone,
            GoogleDriveOutput,
            TimedSplitOutput,
            TimedWordsViewer,
        ],
        Field(discriminator="type"),
    ]
else:
    AnyOutput = Annotated[
        Union.__getitem__(tuple(_output_types)),
        Field(discriminator="type"),
    ]
