from pathlib import Path
from typing import Literal

from ocr.output._base import Output
from ocr.output.duration import AnyDurationCalculator
from ocr.output.duration import DefaultDurationCalculator
from pydantic import BaseModel
from pydantic import Field


class WordDurationPair(BaseModel):
    word: str
    duration: float


class TimedOutput(Output):
    type: Literal["timed"] = "timed"
    path: Path
    duration_calculator: AnyDurationCalculator = Field(
        default_factory=DefaultDurationCalculator
    )

    async def save_results(self, result: str) -> None:
        self.path.parent.mkdir(exist_ok=True, parents=True)
        words = result.split()
        self.path.write_text(
            "\n".join(
                WordDurationPair(
                    word=word,
                    duration=self.duration_calculator.calculate_duration(word),
                ).model_dump_json()
                for word in words
            )
        )
