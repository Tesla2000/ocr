from typing import Annotated
from typing import Union

from ocr.input.directory import DirectoryInput
from ocr.input.google_drive import GoogleDriveInput
from pydantic import Field

AnyInput = Annotated[
    Union[DirectoryInput, GoogleDriveInput], Field(discriminator="type")
]

__all__ = [
    "AnyInput",
]
