import unittest

from ocr.output.duration.frequency import FrequencyDurationCalculator


class TestFrequencyDurationCalculator(unittest.TestCase):
    def test_common_words_have_shorter_duration_than_rare_words(self) -> None:
        calculator = FrequencyDurationCalculator()
        common_words = [
            "jest",
            "to",
            "i",
            "w",
            "na",
            "się",
            "z",
            "nie",
            "po",
            "do",
        ]
        rare_words = [
            "wytchnienie",
            "miękisz",
            "niedościgniony",
            "rozgoryczony",
            "pokrzywdzony",
            "cierpnąć",
            "niepowtarzalny",
            "przystępny",
        ]
        common_durations = [
            calculator.calculate_duration(word) for word in common_words
        ]
        rare_durations = [
            calculator.calculate_duration(word) for word in rare_words
        ]
        avg_common = sum(common_durations) / len(common_durations)
        avg_rare = sum(rare_durations) / len(rare_durations)
        self.assertLess(avg_common * 2, avg_rare)
        for common_duration in common_durations:
            self.assertLess(common_duration, calculator.max_duration)
        for rare_duration in rare_durations:
            self.assertGreater(rare_duration, calculator.min_duration)


if __name__ == "__main__":
    unittest.main()
