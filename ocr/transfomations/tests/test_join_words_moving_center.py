import unittest

from ocr.transfomations import (
    JoinWordsMovingCenter,
)


class TestJoinWordsMovingCenter(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.transformation = JoinWordsMovingCenter(sequence_length=30)

    async def test_transform_empty_text(self) -> None:
        result = await self.transformation.transform("")
        self.assertEqual(result, "")

    async def test_transform_single_word(self) -> None:
        text = "hello"
        result = await self.transformation.transform(text)
        self.assertEqual("hello", result.strip("⠀"))

    async def test_transform_two_words(self) -> None:
        text = "hello world"
        result = await self.transformation.transform(text)
        lines = result.split("\n")
        self.assertEqual(len(lines), 2)
        self.assertIn("hello", lines[0])
        self.assertIn("world", lines[0])
        self.assertIn("hello", lines[1])
        self.assertIn("world", lines[1])

    async def test_transform_uses_braille_separator(self) -> None:
        text = "hello world"
        result = await self.transformation.transform(text)
        self.assertIn("\u2800", result)

    async def test_transform_centers_current_word(self) -> None:
        text = "one two three four five"
        result = await self.transformation.transform(text)
        lines = result.split("\n")
        self.assertEqual(len(lines), 5)
        first_line = lines[0]
        self.assertTrue(first_line.lstrip("⠀").startswith("one"))
        middle_line = lines[2]
        self.assertIn("three", middle_line)

    async def test_transform_respects_character_limit(self) -> None:
        transformation = JoinWordsMovingCenter(sequence_length=20)
        text = "one two three four five six seven"
        result = await transformation.transform(text)
        lines = result.split("\n")
        for line in lines:
            self.assertEqual(len(line), 20)

    async def test_transform_with_short_sequence_length(self) -> None:
        transformation = JoinWordsMovingCenter(sequence_length=15)
        text = "quick brown fox jumps"
        result = await transformation.transform(text)
        lines = result.split("\n")
        self.assertEqual(len(lines), 4)
        for line in lines:
            self.assertEqual(len(line), 15)

    async def test_transform_with_long_sequence_length(self) -> None:
        transformation = JoinWordsMovingCenter(sequence_length=100)
        text = "the quick brown fox jumps over lazy dog"
        result = await transformation.transform(text)
        lines = result.split("\n")
        for line in lines:
            self.assertEqual(len(line), 100)

    async def test_sequences_are_padded_to_exact_length(self) -> None:
        transformation = JoinWordsMovingCenter(sequence_length=50)
        text = "hello world test"
        result = await transformation.transform(text)
        lines = result.split("\n")
        for line in lines:
            self.assertEqual(len(line), 50)

    async def test_current_word_centered_in_sequence(self) -> None:
        transformation = JoinWordsMovingCenter(sequence_length=50)
        text = "test"
        result = await transformation.transform(text)
        lines = result.split("\n")
        line = lines[0]
        self.assertEqual(len(line), 50)
        stripped = line.strip("\u2800")
        self.assertEqual(stripped, "test")
        left_padding = line.index("t")
        right_padding = len(line) - line.rindex("t") - 1
        self.assertAlmostEqual(left_padding, right_padding, delta=1)

    async def test_window_expands_symmetrically(self) -> None:
        transformation = JoinWordsMovingCenter(sequence_length=25)
        text = "a b c d e"
        result = await transformation.transform(text)
        lines = result.split("\n")
        middle_line = lines[2]
        self.assertIn("a", middle_line)
        self.assertIn("b", middle_line)
        self.assertIn("c", middle_line)
        self.assertIn("d", middle_line)
        self.assertIn("e", middle_line)

    async def test_extract_words_removes_whitespace(self) -> None:
        text = "  hello   world  "
        result = await self.transformation.transform(text)
        self.assertNotIn("  ", result)

    async def test_custom_separator(self) -> None:
        transformation = JoinWordsMovingCenter(
            sequence_length=30, word_separator=" "
        )
        text = "hello world"
        result = await transformation.transform(text)
        self.assertIn(" ", result)

    async def test_real_sentence(self) -> None:
        transformation = JoinWordsMovingCenter(sequence_length=40)
        text = "To jest przykładowe zdanie testowe"
        result = await transformation.transform(text)
        lines = result.split("\n")
        self.assertEqual(len(lines), 5)
        for line in lines:
            self.assertEqual(len(line), 40)


class TestJoinWordsMovingCenterConfiguration(unittest.IsolatedAsyncioTestCase):
    def test_default_values(self) -> None:
        transformation = JoinWordsMovingCenter()
        self.assertEqual(transformation.sequence_length, 50)
        self.assertEqual(transformation.word_separator, "\u2800")
        self.assertEqual(transformation.type, "join-words-moving-center")

    def test_custom_values(self) -> None:
        transformation = JoinWordsMovingCenter(
            sequence_length=25, word_separator="|"
        )
        self.assertEqual(transformation.sequence_length, 25)
        self.assertEqual(transformation.word_separator, "|")


if __name__ == "__main__":
    unittest.main()
