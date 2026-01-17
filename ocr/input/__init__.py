from typing import Union

from ocr.input.directory import DirectoryInput
from ocr.input.google_drive import GoogleDriveInput

AnyInput = Union[DirectoryInput, GoogleDriveInput]

__all__ = [
    "AnyInput",
]
