from typing import Annotated
from typing import Union

from ocr.output.combined import CombinedOutput
from ocr.output.google_drive import GoogleDriveOutput
from ocr.output.separate import SeparateOutput
from pydantic import Field

AnyOutput = Annotated[
    Union[CombinedOutput, SeparateOutput, GoogleDriveOutput],
    Field(discriminator="type"),
]

__all__ = [
    "AnyOutput",
    "CombinedOutput",
    "SeparateOutput",
]
