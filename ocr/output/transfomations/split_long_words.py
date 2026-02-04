import re
import sys
from collections.abc import Collection
from collections.abc import Generator
from collections.abc import Sequence
from itertools import combinations
from itertools import count
from typing import Any
from typing import Literal
from typing import TYPE_CHECKING

from pydantic import PositiveInt

if TYPE_CHECKING:
    from pyphen import Pyphen
from ocr.output.transfomations.transformation import Transformation


class SplitLongWords(Transformation):
    type: Literal["split-long-words"] = "split-long-words"
    max_syllable_group_length: PositiveInt = 9
    separator: str = " "
    lang: str = "pl_PL"
    _dic: "Pyphen"

    def model_post_init(self, __context: Any) -> None:
        from pyphen import Pyphen

        self._dic = Pyphen(lang=self.lang)

    async def transform(self, text: str) -> str:
        words = re.findall(r"\S+|\s+", text)
        return "".join(map(self._transform_word, words))

    def _transform_word(self, word: str) -> str:
        leading_punct = ""
        trailing_punct = ""
        clean_word = word
        match = re.match(r"^(\W*)(\w+)(\W*)$", word)
        if match:
            leading_punct, clean_word, trailing_punct = match.groups()
        syllables = self._get_syllables(clean_word)
        if not syllables:
            return word
        grouped = self._group_syllables(syllables)
        return leading_punct + self.separator.join(grouped) + trailing_punct

    def _get_syllables(self, word: str) -> tuple[str, ...]:
        if not self._dic:
            return (word,)
        hyphenated = self._dic.inserted(word)
        if not hyphenated:
            return (word,)
        return tuple(hyphenated.split("-"))

    def _group_syllables(self, syllables: tuple[str, ...]) -> tuple[str, ...]:
        if len(syllables) <= 1:
            return syllables
        if sum(map(len, syllables)) <= self.max_syllable_group_length:
            return ("".join(syllables),)

        def get_longest_group(borders: Collection[int]) -> int:
            max_length = 0
            for syllable_group in self._borders_to_syllables(
                borders, syllables
            ):
                group_length = sum(map(len, syllable_group))
                if len(syllable_group) == 1:
                    group_length = min(
                        group_length, self.max_syllable_group_length
                    )
                max_length = max(max_length, group_length)
            return max_length

        for n_groups in count(2):
            best_borders = min(
                combinations(
                    reversed(range(len(syllables) - 1)), n_groups - 1
                ),
                key=get_longest_group,
            )
            if (
                get_longest_group(best_borders)
                <= self.max_syllable_group_length
            ):
                break
        return tuple(
            map("".join, self._borders_to_syllables(best_borders, syllables))
        )

    @staticmethod
    def _borders_to_syllables(
        borders: Collection[int], syllables: Sequence[str]
    ) -> Generator[list[str], None, None]:
        ordered_borders = iter(sorted(borders))
        next_border = next(ordered_borders) + 0.5
        syllable_group = []
        for index, syllable in enumerate(syllables):
            if index < next_border:
                syllable_group.append(syllable)
                continue
            yield syllable_group
            syllable_group = [syllable]
            next_border = next(ordered_borders, sys.maxsize) + 0.5
        yield syllable_group
