import logging
from typing import Annotated
from typing import TypeAlias
from typing import Union

from ocr.output.combined import CombinedOutput
from ocr.output.rclone import RClone
from ocr.output.timed import TimedOutput
from pydantic import Field

_logger = logging.getLogger(__name__)
AnyOutput: TypeAlias = Annotated[
    Union[CombinedOutput, TimedOutput, RClone],
    Field(discriminator="type"),
]
__all__ = [
    "AnyOutput",
    "CombinedOutput",
    "TimedOutput",
    "RClone",
]
try:
    from ocr.output.google_drive import GoogleDriveOutput

    AnyOutput = Annotated[  # type: ignore[misc]
        Union[AnyOutput, GoogleDriveOutput], Field(discriminator="type")
    ]
    __all__.append("GoogleDriveOutput")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use Google Drive output is not installed, Google Drive output is disabled.\n{e}"
    )
try:
    from ocr.output.timed_viewer import TimedWordsViewer

    AnyOutput = Annotated[  # type: ignore[misc]
        Union[AnyOutput, TimedWordsViewer], Field(discriminator="type")
    ]
    __all__.append("TimedWordsViewer")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use Google Drive output is not installed, Google Drive output is disabled.\n{e}"
    )
