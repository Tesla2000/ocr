from typing import Literal

from ocr.output.duration._base import DurationCalculator


class DefaultDurationCalculator(DurationCalculator):
    type: Literal["default"] = "default"

    def calculate_duration(self, word: str) -> float:
        return 1.0
