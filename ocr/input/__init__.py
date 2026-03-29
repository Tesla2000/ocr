import logging
from typing import Annotated
from typing import TYPE_CHECKING
from typing import TypeAlias
from typing import Union

from ocr.input.directory import DirectoryInput
from pydantic import Field

_logger = logging.getLogger(__name__)
_input_types: list[type] = [DirectoryInput]
__all__ = [
    "AnyInput",
    "DirectoryInput",
]
try:
    from ocr.input.google_drive import GoogleDriveInput

    _input_types.append(GoogleDriveInput)
    __all__.append("GoogleDriveInput")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use Google Drive input is not installed, Google Drive input is disabled.\n{e}"
    )
try:
    from ocr.input.google_drive_directory import GoogleDriveDirectoryInput

    _input_types.append(GoogleDriveDirectoryInput)
    __all__.append("GoogleDriveDirectoryInput")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use Google Drive directory input is not installed, Google Drive directory input is disabled.\n{e}"
    )
try:
    from ocr.input.pdf import PdfInput

    _input_types.append(PdfInput)
    __all__.append("PdfInput")
except ImportError as e:
    _logger.warning(
        f"Package necessary to use PDF input is not installed, PDF input is disabled.\n{e}"
    )
if TYPE_CHECKING:
    AnyInput: TypeAlias = Annotated[
        Union[
            DirectoryInput,
            GoogleDriveInput,
            GoogleDriveDirectoryInput,
            PdfInput,
        ],
        Field(discriminator="type"),
    ]
else:
    AnyInput: TypeAlias = Annotated[
        Union.__getitem__(tuple(_input_types)), Field(discriminator="type")
    ]
