import json
from pathlib import Path

import pytest

from tools.mosaik.nayade import (
    NayadeError,
    build_processor_observation,
    build_soundcheck_session,
    next_step,
    record_result,
    validate_session,
    write_session,
)


def _source():
    return {
        "source_type": "fictional_mapping",
        "composition": {"width": 1920, "height": 1080},
        "slices": [
            {"slice_id": "slice-001", "input_group_id": "group-a"},
            {"slice_id": "slice-002", "input_group_id": "group-a"},
            {"slice_id": "slice-003", "input_group_id": "group-b"},
        ],
        "private_payload": "must-not-be-copied",
    }


def test_build_soundcheck_session_is_deterministic_and_grouped():
    first = build_soundcheck_session(
        _source(),
        session_id="session-nayade",
        name="Soundcheck",
        seed=42,
        created_at="2026-01-10T20:00:00Z",
    )
    second = build_soundcheck_session(
        _source(),
        session_id="session-nayade",
        name="Soundcheck",
        seed=42,
        created_at="2026-01-10T20:00:00Z",
    )

    assert first == second
    assert first["targets"]["input_groups"] == ["group-a", "group-b"]
    assert len(first["planned_steps"]) == 6
    assert first["planned_steps"][4]["parameters"]["seed"] == 42
    assert "private_payload" not in json.dumps(first)


def test_record_result_matches_step_and_returns_next_step():
    session = build_soundcheck_session(
        _source(),
        session_id="session-nayade",
        name="Soundcheck",
        created_at="2026-01-10T20:00:00Z",
    )
    updated = record_result(
        session,
        step_id="step-001",
        result="approved",
        targets=["group-a"],
        parameters={"signal_lock": True},
        notes="Baseline is stable.",
        recorded_at="2026-01-10T20:01:00Z",
    )

    assert updated["planned_steps"][0]["result"] == "approved"
    assert updated["events"][0]["planned_step_id"] == "step-001"
    assert next_step(updated)["step_id"] == "step-002"
    assert session["events"] == []


def test_nayade_rejects_ambiguous_or_invalid_result():
    session = build_soundcheck_session(
        _source(),
        session_id="session-nayade",
        name="Soundcheck",
        created_at="2026-01-10T20:00:00Z",
    )
    with pytest.raises(NayadeError, match="result must be one"):
        record_result(session, result="execute", step_id="step-001")
    with pytest.raises(NayadeError, match="no pending step"):
        record_result(session, result="approved", step_id="missing")


def test_processor_observation_is_passive_and_explicit_about_unknowns():
    observation = build_processor_observation(
        model="VX600",
        firmware="1.3.0",
        transport="manual",
        confidence="medium",
        evidence=["operator_label", "software_screenshot"],
        input_signal={"resolution": "1920x1080", "range": "unknown"},
    )

    assert observation["read_only"] is True
    assert observation["commands_sent"] is False
    assert observation["model"] == "VX600"
    assert observation["unknowns"]


def test_session_can_be_written_and_validated_without_private_source_data(tmp_path):
    session = build_soundcheck_session(
        _source(),
        session_id="session-nayade",
        name="Soundcheck",
        created_at="2026-01-10T20:00:00Z",
    )
    output = write_session(session, tmp_path / "session.json")
    loaded = json.loads(Path(output).read_text(encoding="utf-8"))
    validate_session(loaded)
    assert loaded["source"]["slice_count"] == 3
    assert "private_payload" not in json.dumps(loaded)


def test_nayade_schemas_match_the_generated_contracts():
    repository_root = Path(__file__).parents[2]
    session_schema = json.loads(
        (repository_root / "schemas" / "nayade-soundcheck-session.schema.json").read_text(encoding="utf-8")
    )
    processor_schema = json.loads(
        (repository_root / "schemas" / "nayade-processor-observation.schema.json").read_text(encoding="utf-8")
    )
    session = build_soundcheck_session(
        _source(),
        session_id="session-nayade",
        name="Soundcheck",
        created_at="2026-01-10T20:00:00Z",
    )
    observation = build_processor_observation()

    assert set(session_schema["required"]) == set(session)
    assert session_schema["properties"]["read_only_source"]["const"] is True
    assert set(processor_schema["required"]) == set(observation)
    assert processor_schema["properties"]["commands_sent"]["const"] is False
