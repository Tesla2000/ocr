from typing import Literal

from ocr.output.timed import TimedOutput
from ocr.output.timed import WordDurationPair
from ocr.transfomations.split_long_words import SplitLongWords
from pydantic import Field


class TimedSplitOutput(TimedOutput):
    type: Literal["timed-split"] = "timed-split"
    word_splitter: SplitLongWords = Field(default_factory=SplitLongWords)

    async def _save_results(self, result: str) -> None:
        self.duration_calculator.reset()
        self.path.parent.mkdir(exist_ok=True, parents=True)
        words = result.split()
        pairs: list[str] = []
        for word in words:
            duration = self.duration_calculator.calculate_duration(word)
            split_result = await self.word_splitter.transform(word)
            parts = split_result.split()
            pairs.extend(
                WordDurationPair(
                    word=part, duration=duration / len(parts)
                ).model_dump_json()
                for part in parts
            )
        self.path.write_text("\n".join(pairs))
