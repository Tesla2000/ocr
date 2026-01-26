from typing import Annotated
from typing import Union

from pydantic import Field

from .combined import CombinedOutput
from .separate import SeparateOutput

AnyLocalOutput = Annotated[
    Union[CombinedOutput, SeparateOutput], Field(discriminator="type")
]

__all__ = [
    "CombinedOutput",
    "SeparateOutput",
    "AnyLocalOutput",
]
