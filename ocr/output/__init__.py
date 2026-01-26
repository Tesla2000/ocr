from typing import Annotated
from typing import Union

from ocr.output.google_drive import GoogleDriveOutput
from ocr.output.local_ouptup.combined import CombinedOutput
from ocr.output.local_ouptup.separate import SeparateOutput
from ocr.output.rclone import RClone
from pydantic import Field

AnyOutput = Annotated[
    Union[CombinedOutput, SeparateOutput, GoogleDriveOutput, RClone],
    Field(discriminator="type"),
]

__all__ = [
    "AnyOutput",
    "CombinedOutput",
    "SeparateOutput",
    "RClone",
    "GoogleDriveOutput",
]
