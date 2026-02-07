import re
from itertools import chain
from math import ceil
from typing import Literal

from ocr.output.transfomations.transformation import Transformation
from pydantic import PositiveInt


class DuplicateLongWords(Transformation):
    type: Literal["duplicate-long-words"] = "duplicate-long-words"
    max_syllable_group_length: PositiveInt = 9

    async def transform(self, text: str) -> str:
        words = re.findall(r"\S+|\s+", text)
        return " ".join(chain.from_iterable(map(self._duplicate_word, words)))

    def _duplicate_word(self, word: str) -> tuple[str, ...]:
        return ceil(len(word) / self.max_syllable_group_length) * (word,)
