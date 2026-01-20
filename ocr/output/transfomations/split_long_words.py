import re
from typing import Literal
from typing import TYPE_CHECKING

from pydantic import PositiveInt

if TYPE_CHECKING:
    from pyphen import Pyphen
from ocr.output.transfomations.transformation import Transformation


class SplitLongWords(Transformation):
    type: Literal["split-long-words"] = "split-long-words"
    max_syllable_group_length: PositiveInt = 10
    separator: str = " "
    lang: str = "pl_PL"
    _dic: "Pyphen"

    def model_post_init(self, __context) -> None:
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
        total_length = sum(len(s) for s in syllables)
        if total_length <= self.max_syllable_group_length:
            return ("".join(syllables),)
        num_groups = (
            total_length + self.max_syllable_group_length - 1
        ) // self.max_syllable_group_length
        target_size = total_length / num_groups
        groups = []
        current_group = []
        current_length = 0
        for syllable in syllables:
            current_group.append(syllable)
            current_length += len(syllable)
            if current_length >= target_size and len(groups) < num_groups - 1:
                groups.append("".join(current_group))
                current_group = []
                current_length = 0
        if current_group:
            groups.append("".join(current_group))
        return tuple(groups)
