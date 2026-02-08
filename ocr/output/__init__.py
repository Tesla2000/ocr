import logging
from typing import Annotated
from typing import TypeAlias
from typing import Union

from ocr.output.local_ouptup.combined import CombinedOutput
from ocr.output.local_ouptup.separate import SeparateOutput
from ocr.output.rclone import RClone
from pydantic import Field

_logger = logging.getLogger(__name__)
AnyOutput: TypeAlias = Annotated[
    Union[CombinedOutput, SeparateOutput, RClone],
    Field(discriminator="type"),
]
__all__ = [
    "AnyOutput",
    "CombinedOutput",
    "SeparateOutput",
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
