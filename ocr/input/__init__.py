from typing import Annotated
from typing import Union

from ocr.input.directory import DirectoryInput
from ocr.input.google_drive import GoogleDriveInput
from ocr.input.google_drive_directory import GoogleDriveDirectoryInput
from pydantic import Field

AnyInput = Annotated[
    Union[DirectoryInput, GoogleDriveInput, GoogleDriveDirectoryInput],
    Field(discriminator="type"),
]

__all__ = [
    "AnyInput",
]
