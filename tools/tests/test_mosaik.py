from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from tools.mosaik.instar import discover_media_files, run_instar
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


class InstarTests(unittest.TestCase):
    def test_discover_media_files_is_recursive_and_filters_extensions(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "clip.MP4").touch()
            (root / "notes.txt").touch()
            nested = root / "nested"
            nested.mkdir()
            (nested / "loop.mov").touch()

            self.assertEqual(
                discover_media_files(root),
                [root / "clip.MP4", nested / "loop.mov"],
            )

    def test_run_instar_aggregates_shared_diagnostics(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first.mp4"
            second = root / "second.mov"
            first.touch()
            second.touch()

            def fake_diagnose(path, **_kwargs):
                status = "PASS" if Path(path).name == "first.mp4" else "WARN"
                return {
                    "overall_status": status,
                    "video": {"codec": "dxv", "width": 1920, "height": 1080, "average_fps": "60"},
                }

            with patch("tools.mosaik.instar.diagnose_file", side_effect=fake_diagnose):
                report = run_instar(root)

            self.assertEqual(report["overall_status"], "WARN")
            self.assertEqual(report["files_found"], 2)
            self.assertEqual([item["status"] for item in report["items"]], ["PASS", "WARN"])


if __name__ == "__main__":
    unittest.main()
