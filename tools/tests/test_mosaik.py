import unittest

from tools.mosaik.media import format_fps, has_alpha, parse_fraction


class MediaHelpersTests(unittest.TestCase):
    def test_parse_fraction(self):
        self.assertAlmostEqual(parse_fraction("30000/1001"), 29.97002997, places=5)

    def test_parse_invalid_fraction(self):
        self.assertIsNone(parse_fraction("0/0"))
        self.assertIsNone(parse_fraction("N/A"))

    def test_format_fps(self):
        self.assertEqual(format_fps("60/1"), "60")
        self.assertEqual(format_fps("30000/1001"), "29.97")

    def test_detect_alpha_pixel_formats(self):
        self.assertTrue(has_alpha({"codec_name": "cfhd", "pix_fmt": "gbrap12le"}))
        self.assertFalse(has_alpha({"codec_name": "h264", "pix_fmt": "yuv420p"}))
        self.assertIsNone(has_alpha({"codec_name": "dxv", "pix_fmt": "rgba"}))


if __name__ == "__main__":
    unittest.main()
