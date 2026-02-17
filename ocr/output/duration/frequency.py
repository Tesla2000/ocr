import re
from typing import Any
from typing import Literal

from ocr.output.duration._base import DurationCalculator
from wordfreq import word_frequency


class FrequencyDurationCalculator(DurationCalculator):
    type: Literal["frequency"] = "frequency"
    language: str = "pl"
    min_duration: float = 0.5
    max_duration: float = 2.0
    base_frequency: float = 1e-5
    _word_pattern: re.Pattern[str]

    def model_post_init(self, context: Any, /) -> None:
        self._word_pattern = re.compile(r"\w+")

    def calculate_duration(self, word: str) -> float:
        cleaned_word = "".join(self._word_pattern.findall(word.lower()))
        frequency: float = word_frequency(cleaned_word, self.language)
        if frequency == 0:
            return self.max_duration
        normalized_freq = frequency / self.base_frequency
        duration = self.min_duration + (
            self.max_duration - self.min_duration
        ) / (1 + normalized_freq)
        return max(self.min_duration, min(self.max_duration, duration))
