from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from tools.mosaik.instar import discover_media_files, run_instar
from tools.mosaik.media import format_fps, has_alpha, parse_fraction
from tools.mosaik.resolume import run_resolume_audit


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


class ResolumeAuditTests(unittest.TestCase):
    def test_audit_extracts_composition_and_deduplicates_media(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            media = root / "loop.mp4"
            media.touch()
            composition = root / "show.avc"
            composition.write_text(
                f'''<?xml version="1.0" encoding="utf-8"?>
<Composition name="Composition" numDecks="1" numLayers="2" numColumns="3">
  <versionInfo name="Resolume Arena" majorVersion="7" minorVersion="26" microVersion="0" revision="1"/>
  <CompositionInfo name="Test Show" width="1920" height="1080"/>
  <Deck name="Deck">
    <Clip name="Clip" layerIndex="0" columnIndex="0">
      <VideoTrack><VideoSource width="1920" height="1080" type="VideoFormatReaderSource">
        <VideoFormatReaderSource fileName="{media}"/>
      </VideoSource></VideoTrack>
    </Clip>
    <Clip name="Clip" layerIndex="1" columnIndex="0">
      <VideoTrack><VideoSource width="1920" height="1080" type="VideoFormatReaderSource">
        <VideoFormatReaderSource fileName="{media}"/>
      </VideoSource></VideoTrack>
    </Clip>
  </Deck>
</Composition>''',
                encoding="utf-8",
            )

            report = run_resolume_audit(composition, skip_media=True)

            self.assertEqual(report["overall_status"], "WARN")
            self.assertEqual(report["composition"]["name"], "Test Show")
            self.assertEqual(report["composition"]["width"], 1920)
            self.assertEqual(report["statistics"]["clips"], 2)
            self.assertEqual(report["statistics"]["media_files"], 1)
            self.assertEqual(report["media"][0]["occurrences"], 2)
            self.assertEqual(report["media"][0]["status"], "NOT_ANALYZED")

    def test_audit_creates_safe_plan_for_non_dxv_media(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            media = root / "loop.mp4"
            media.touch()
            composition = root / "show.avc"
            composition.write_text(
                f'<Composition><CompositionInfo name="Show" width="1920" height="1080"/>'
                f'<Clip layerIndex="0" columnIndex="0"><VideoFile value="{media}"/></Clip></Composition>',
                encoding="utf-8",
            )

            with patch("tools.mosaik.resolume.diagnose_file", return_value={
                "overall_status": "WARN",
                "video": {"codec": "h264", "width": 1920, "height": 1080},
            }):
                report = run_resolume_audit(composition)

            risks = [action["risk"] for action in report["action_plan"]]
            operations = [action["operation"] for action in report["action_plan"]]
            self.assertEqual(report["overall_status"], "WARN")
            self.assertIn("SAFE", risks)
            self.assertIn("create_derived_media", operations)


if __name__ == "__main__":
    unittest.main()
