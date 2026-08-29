import unittest

from tools.mosaik.media import format_fps, parse_fraction


class MediaHelpersTests(unittest.TestCase):
    def test_parse_fraction(self):
        self.assertAlmostEqual(parse_fraction("30000/1001"), 29.97002997, places=5)

    def test_parse_invalid_fraction(self):
        self.assertIsNone(parse_fraction("0/0"))
        self.assertIsNone(parse_fraction("N/A"))

    def test_format_fps(self):
        self.assertEqual(format_fps("60/1"), "60")
        self.assertEqual(format_fps("30000/1001"), "29.97")


if __name__ == "__main__":
    unittest.main()
