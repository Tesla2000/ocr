from collections.abc import Generator
from collections.abc import Iterable
from collections.abc import Sequence
from math import ceil
from typing import Literal

from ocr.output.transfomations.transformation import Transformation
from pydantic import PositiveInt


class JoinWordsMovingCenter(Transformation):
    type: Literal["join-words-moving-center"] = "join-words-moving-center"
    sequence_length: PositiveInt = 30
    word_separator: str = "\u2800"

    async def transform(self, text: str) -> str:
        words = text.split()
        return "\n".join(self._generate_lines(words))

    def _generate_lines(
        self, words: Sequence[str]
    ) -> Generator[str, None, None]:
        for index, word in enumerate(words, 1):
            word_length = len(word)
            half_word_length = ceil(word_length / 2)
            previous_words = self._take_words_in_limit(
                half_word_length, reversed(words[: index - 1])
            )
            result = self.word_separator.join(
                (
                    previous_words.pop(),
                    *previous_words,
                    word,
                    *self._take_words_in_limit(
                        half_word_length, words[index:]
                    ),
                )
            ).rjust(self.sequence_length, self.word_separator)
            assert len(result) == self.sequence_length
            yield result

    def _take_words_in_limit(
        self, half_word_length: int, words_iterable: Iterable[str]
    ) -> list[str]:
        words: list[str] = []
        for word in words_iterable:
            n_remaining_characters = self._calc_remaining_characters(
                half_word_length, words
            )
            if n_remaining_characters < len(word):
                break
            words.append(word)
        words.append(
            self.word_separator
            * (self._calc_remaining_characters(half_word_length, words) + 1)
        )
        return words

    def _calc_remaining_characters(
        self, half_word_length: int, words: Sequence[str]
    ) -> int:
        return self.sequence_length // 2 - len(
            " ".join((half_word_length * " ", *words, " "))
        )
