import unittest

from qaniujaaqpait.converter import syllabify, romanize


class TestInuktitutConverter(unittest.TestCase):
    def test_basic_syllables(self):
        self.assertEqual(syllabify("pi"), "ᐱ")
        self.assertEqual(syllabify("maa"), "ᒫ")
        self.assertEqual(syllabify("s"), "ᔅ")
        self.assertEqual(syllabify("q"), "ᖅ")
        self.assertEqual(romanize("ᐱ"), "pi")

    def test_digraphs(self):
        self.assertEqual(syllabify("qquu"), "ᖅᑰ")
        self.assertEqual(syllabify("nngii"), "ᙲ")
        self.assertEqual(syllabify("qquu"), "ᖅᑰ")
        self.assertEqual(syllabify("nngii"), "ᙲ")
        self.assertEqual(romanize("ᖅᑰ"), "qquu")
        self.assertEqual(romanize("ᙲ"), "nngii")

    def test_round_trip(self):
        original = "qaniujaaqpait llu"
        syllabics = syllabify(original)
        result = romanize(syllabics)
        self.assertEqual(result, original)

    def test_unknown_characters(self):
        self.assertEqual(syllabify("xyz"), "xyz")
        self.assertEqual(romanize("xyz"), "xyz")

    def test_mixed_text(self):
        mixed = "heyo qquu"
        self.assertEqual(syllabify(mixed), "heyo ᖅᑰ")
        back = romanize("heyo ᖅᑰ")
        self.assertEqual(back, "heyo qquu")


if __name__ == "__main__":
    unittest.main()
