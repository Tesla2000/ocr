import logging
from typing import Annotated
from typing import TypeAlias
from typing import Union

from ocr.input.directory import DirectoryInput
from pydantic import Field

_logger = logging.getLogger(__name__)
AnyInput: TypeAlias = Annotated[
    Union[DirectoryInput,], Field(discriminator="type")
]
__all__ = [
    "AnyInput",
    "DirectoryInput",
]
try:
    from ocr.input.google_drive import GoogleDriveInput

    AnyInput = Annotated[
        Union[AnyInput, GoogleDriveInput], Field(discriminator="type")
    ]
    __all__.append("GoogleDriveInput")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use Google Drive input is not installed, Google Drive input is disabled.\n{e}"
    )
try:
    from ocr.input.google_drive_directory import GoogleDriveDirectoryInput

    AnyInput = Annotated[
        Union[AnyInput, GoogleDriveDirectoryInput], Field(discriminator="type")
    ]
    __all__.append("GoogleDriveDirectoryInput")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use Google Drive directory input is not installed, Google Drive directory input is disabled.\n{e}"
    )
try:
    from ocr.input.pdf import PdfInput

    AnyInput = Annotated[
        Union[AnyInput, PdfInput], Field(discriminator="type")
    ]
    __all__.append("PdfInput")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use PDF input is not installed, PDF input is disabled.\n{e}"
    )
