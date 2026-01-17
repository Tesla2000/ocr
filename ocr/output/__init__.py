from typing import Union

from ocr.output.combined import CombinedOutput
from ocr.output.separate import SeparateOutput

AnyOutput = Union[CombinedOutput, SeparateOutput]

__all__ = [
    "AnyOutput",
    "CombinedOutput",
    "SeparateOutput",
]
