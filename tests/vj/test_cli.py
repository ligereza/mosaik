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


def test_vj_project_replay_cli_replays_a_manifest(tmp_path, capsys):
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    records = []
    for index, source in enumerate(fixture["records"]):
        input_path = tmp_path / f"report-{index}.json"
        input_path.write_text(json.dumps(source["data"]), encoding="utf-8")
        record = {
            "stage": source["stage"],
            "event_id": source["event_id"],
            "sequence": source["sequence"],
            "input": input_path.name,
        }
        if "processor_observation" in source:
            observation_path = tmp_path / f"observation-{index}.json"
            observation_path.write_text(json.dumps(source["processor_observation"]), encoding="utf-8")
            record["processor_observation"] = observation_path.name
        records.append(record)
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "replay_type": "MosaikVJProjectReplay",
                "schema_version": "0.1",
                "session_id": "cli-project-session",
                "records": records,
            }
        ),
        encoding="utf-8",
    )
    report_path = tmp_path / "replay.json"

    exit_code = main(["vj-project-replay", str(manifest_path), "--report", str(report_path)])

    assert exit_code == 0
    assert json.loads(report_path.read_text(encoding="utf-8"))["status"] == "PASS"
    assert '"source_paths_exposed": false' in capsys.readouterr().out
