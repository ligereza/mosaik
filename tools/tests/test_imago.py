import json
from pathlib import Path

import pytest

from tools.mosaik.imago import (
    ImagoError,
    build_show_session,
    next_proposal,
    record_event,
    record_result,
    validate_session,
    write_session,
)


def test_imago_records_show_incident_recovery_and_closure():
    session = build_show_session(
        {"profile_id": "profile-01", "private_payload": "must-not-copy"},
        session_id="show-01",
        name="Fictional Show",
        created_at="2026-01-10T22:00:00Z",
    )
    session = record_event(session, event_type="show_started", recorded_at="2026-01-10T22:00:00Z")
    session = record_result(
        session,
        proposal_id="proposal-event-001-observe_show",
        result="accepted",
        recorded_at="2026-01-10T22:01:00Z",
    )
    session = record_event(
        session,
        event_type="incident_detected",
        payload={"category": "signal_review", "private_payload": "drop"},
        recorded_at="2026-01-10T22:15:00Z",
    )
    assert session["status"] == "incident"
    assert session["open_incidents"]
    session = record_event(session, event_type="recovery_started", recorded_at="2026-01-10T22:16:00Z")
    session = record_event(session, event_type="recovery_verified", recorded_at="2026-01-10T22:17:00Z")
    session = record_event(session, event_type="show_closed", recorded_at="2026-01-10T23:00:00Z")

    assert session["status"] == "closed"
    assert session["open_incidents"] == []
    assert session["sequence"] == 5
    assert "private_payload" not in json.dumps(session)


def test_imago_rejects_invalid_transition_and_requires_pending_result():
    session = build_show_session(session_id="show-01", name="Show", created_at="2026-01-10T22:00:00Z")
    with pytest.raises(ImagoError, match="transition not allowed"):
        record_event(session, event_type="cue_fired", recorded_at="2026-01-10T22:00:00Z")
    session = record_event(session, event_type="show_started", recorded_at="2026-01-10T22:00:00Z")
    proposal = next_proposal(session)
    with pytest.raises(ImagoError, match="not pending"):
        record_result(session, proposal_id="missing", result="accepted", recorded_at="2026-01-10T22:01:00Z")
    assert proposal["execution_mode"] == "proposal_only"


def test_imago_result_and_checkpoint_are_serializable(tmp_path):
    session = build_show_session(session_id="show-01", name="Show", created_at="2026-01-10T22:00:00Z")
    output = write_session(session, tmp_path / "imago.json")
    loaded = json.loads(Path(output).read_text(encoding="utf-8"))
    validate_session(loaded)
    assert loaded["read_only"] is True
    assert loaded["commands_sent"] is False


def test_imago_schema_matches_generated_session():
    root = Path(__file__).parents[2]
    schema = json.loads((root / "schemas" / "imago-show-session.schema.json").read_text(encoding="utf-8"))
    session = build_show_session(session_id="show-01", name="Show", created_at="2026-01-10T22:00:00Z")
    assert set(schema["required"]) == set(session)
    assert schema["properties"]["commands_sent"]["const"] is False
