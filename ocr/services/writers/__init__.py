from typing import Union

from ocr.services.writers.combined_writer import CombinedWriter
from ocr.services.writers.separate_writer import SeparateWriter

AnyWriter = Union[CombinedWriter, SeparateWriter]

__all__ = [
    "AnyWriter",
    "CombinedWriter",
    "SeparateWriter",
]
