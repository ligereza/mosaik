import json
import sys
from pathlib import Path

TOOLS_ROOT = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS_ROOT))

from mosaik_cli import main


FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "adapters"
    / "vj"
    / "replay"
    / "fixtures"
    / "plugin-bridges-fictional.json"
)


def test_vj_replay_cli_prints_and_writes_a_report(tmp_path, capsys):
    report_path = tmp_path / "vj-replay.json"

    exit_code = main(["vj-replay", str(FIXTURE), "--report", str(report_path)])

    assert exit_code == 0
    output = capsys.readouterr().out
    assert '"status": "PASS"' in output
    saved = json.loads(report_path.read_text(encoding="utf-8"))
    assert saved["phase_order"][-1] == "closure"


def test_vj_replay_cli_returns_a_clean_error_for_invalid_fixture(tmp_path, capsys):
    invalid = tmp_path / "invalid.json"
    invalid.write_text('{"replay_type":"wrong"}\n', encoding="utf-8")

    exit_code = main(["vj-replay", str(invalid)])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "MOSAIK ERROR" in captured.err
    assert "identity" in captured.err


def test_vj_project_cli_projects_a_real_stage_report(tmp_path, capsys):
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    input_path = tmp_path / "instar-report.json"
    output_path = tmp_path / "projection.json"
    input_path.write_text(json.dumps(fixture["records"][0]["data"]), encoding="utf-8")

    exit_code = main(
        [
            "vj-project",
            "instar",
            str(input_path),
            "--event-id",
            "instar-001",
            "--sequence",
            "1",
            "--mode",
            "projection",
            "--output",
            str(output_path),
        ]
    )

    assert exit_code == 0
    assert json.loads(output_path.read_text(encoding="utf-8"))["show_phase"] == "preflight"
    assert "preflight" in capsys.readouterr().out
