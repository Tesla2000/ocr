import unittest

from ocr.output.transfomations.split_long_words import SplitLongWords


class TestSplitLongWords(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.transformation = SplitLongWords(
            separator="-",
        )

    async def test_transform_preserves_short_words(self) -> None:
        text = "To jest krótki tekst"
        result = await self.transformation.transform(text)
        self.assertEqual(result, text)

    async def test_transform_splits_very_long_polish_word(self) -> None:
        text = "konstantynopolitańczykowianeczka"
        result = await self.transformation.transform(text)
        self.assertIn("-", result)
        self.assertNotEqual(result, text)
        self.assertGreater(len(result), len(text))

    async def test_transform_preserves_whitespace(self) -> None:
        text = "  krótkie   słowa  "
        result = await self.transformation.transform(text)
        self.assertEqual(result, text)

    async def test_transform_preserves_punctuation(self) -> None:
        transformation = SplitLongWords(
            separator="-", max_syllable_group_length=5
        )
        text = "(prawdopodobnie)!"
        result = await transformation.transform(text)
        self.assertTrue(result.startswith("("))
        self.assertTrue(result.endswith(")!"))

    def test_get_syllables_returns_tuple(self) -> None:
        result = self.transformation._get_syllables("słowo")
        self.assertIsInstance(result, tuple)

    def test_get_syllables_polish_word(self) -> None:
        result = self.transformation._get_syllables("warszawa")
        self.assertIsInstance(result, tuple)
        self.assertGreater(len(result), 0)

    def test_group_syllables_single_syllable(self) -> None:
        syllables = ("word",)
        result = self.transformation._group_syllables(syllables)
        self.assertEqual(result, syllables)

    def test_group_syllables_fits_in_one_group(self) -> None:
        syllables = ("a", "bc", "def")
        result = self.transformation._group_syllables(syllables)
        self.assertEqual(result, ("abcdef",))

    def test_group_syllables_splits_evenly(self) -> None:
        self.transformation.max_syllable_group_length = 10
        syllables = ("abc", "def", "ghi", "jkl", "mno", "pqr")
        result = self.transformation._group_syllables(syllables)
        self.assertGreater(len(result), 1)
        lengths = [len(group) for group in result]
        max_diff = max(lengths) - min(lengths)
        self.assertLessEqual(max_diff, 3)

    def test_group_syllables_respects_max_length(self) -> None:
        self.transformation.max_syllable_group_length = 5
        syllables = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j")
        result = self.transformation._group_syllables(syllables)
        for group in result:
            self.assertLessEqual(
                len(group), self.transformation.max_syllable_group_length + 2
            )

    def test_transform_word_with_leading_punctuation(self) -> None:
        transformation = SplitLongWords(
            separator="-", max_syllable_group_length=5
        )
        result = transformation._transform_word("(prawdopodobnie")
        self.assertTrue(result.startswith("("))

    def test_transform_word_with_trailing_punctuation(self) -> None:
        transformation = SplitLongWords(
            separator="-", max_syllable_group_length=5
        )
        result = transformation._transform_word("prawdopodobnie!")
        self.assertTrue(result.endswith("!"))

    def test_custom_separator(self) -> None:
        transformation = SplitLongWords(
            separator="·", max_syllable_group_length=5
        )
        result = transformation._transform_word("prawdopodobnie")
        self.assertIn("·", result)

    def test_group_syllables_empty_tuple(self) -> None:
        result = self.transformation._group_syllables(())
        self.assertEqual(result, ())

    async def test_real_polish_word_niepodległość(self) -> None:
        transformation = SplitLongWords(
            separator="-", max_syllable_group_length=8
        )
        text = "niepodległość"
        result = await transformation.transform(text)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    async def test_real_polish_word_przeszukiwanie(self) -> None:
        transformation = SplitLongWords(
            separator="-", max_syllable_group_length=8
        )
        text = "przeszukiwanie"
        result = await transformation.transform(text)
        self.assertIn("-", result)

    async def test_mixed_text_with_long_and_short_words(self) -> None:
        transformation = SplitLongWords(
            separator="-", max_syllable_group_length=8
        )
        text = "To jest prawdopodobnie niepodległość Polski"
        result = await transformation.transform(text)
        self.assertIn("-", result)
        self.assertIn("To", result)
        self.assertIn("jest", result)

    async def test_multiple_long_words(self) -> None:
        transformation = SplitLongWords(
            separator="-", max_syllable_group_length=8
        )
        text = "prawdopodobnie niepodległość"
        result = await transformation.transform(text)
        split_count = result.count("-")
        self.assertGreater(split_count, 0)

    def test_group_syllables_creates_similar_sized_groups(self) -> None:
        syllables = ("ko", "mu", "ni", "ka", "cyj", "ność")
        result = self.transformation._group_syllables(syllables)
        self.assertGreater(len(result), 1)
        lengths = [len(group) for group in result]
        self.assertLessEqual(max(lengths) - min(lengths), 3)

    def test_transform_word_short_word_unchanged(self) -> None:
        result = self.transformation._transform_word("kot")
        self.assertEqual(result, "kot")

    def test_get_syllables_preserves_word_content(self) -> None:
        word = "przykład"
        result = self.transformation._get_syllables(word)
        combined = "".join(result)
        self.assertEqual(combined.lower(), word.lower())

    def test_group_syllables_prioritizes_first_group_length(self) -> None:
        self.transformation.max_syllable_group_length = 7
        syllables = ("aaaa", "bbb", "cccc")
        result = self.transformation._group_syllables(syllables)
        self.assertEqual(result, ("aaaabbb", "cccc"))
        lengths = [len(group) for group in result]
        self.assertEqual(lengths, [7, 4])


class TestSplitLongWordsConfiguration(unittest.IsolatedAsyncioTestCase):
    def test_default_values(self) -> None:
        transformation = SplitLongWords(
            separator="-",
        )
        self.assertEqual(transformation.max_syllable_group_length, 10)
        self.assertEqual(transformation.separator, "-")
        self.assertEqual(transformation.lang, "pl_PL")
        self.assertEqual(transformation.type, "split-long-words")

    def test_custom_values(self) -> None:
        transformation = SplitLongWords(
            max_syllable_group_length=15, separator="·", lang="en_US"
        )
        self.assertEqual(transformation.max_syllable_group_length, 15)
        self.assertEqual(transformation.separator, "·")
        self.assertEqual(transformation.lang, "en_US")

    def test_pyphen_instance_created(self) -> None:
        transformation = SplitLongWords(
            separator="-",
        )
        self.assertIsNotNone(transformation._dic)

    async def test_too_long_syllable(self) -> None:
        transformation = SplitLongWords(max_syllable_group_length=5)
        long_syllable_element = "chrząszczowy?"
        transformed_text = await transformation.transform(
            long_syllable_element
        )
        self.assertEqual("chrząsz czowy?", transformed_text)


if __name__ == "__main__":
    unittest.main()
