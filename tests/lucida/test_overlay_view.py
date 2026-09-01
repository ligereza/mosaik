import json
from dataclasses import replace
from pathlib import Path

import pytest

from adapters.vj.contracts import VJState
from lucida import LucidaOrchestrator
from lucida.contracts import LucidaContractError, LucidaState
from lucida.overlay import (
    MAX_DIFF_CHANGES,
    OverlayDiffError,
    build_overlay_view,
    diff_overlay_view,
)


def _state():
    orchestrator = LucidaOrchestrator()
    state = orchestrator.initial_state("session-overlay")
    return orchestrator, orchestrator.propose(
        {
            "event_id": "evt-overlay",
            "timestamp": "2026-01-10T20:00:00Z",
            "phase": "preflight",
            "event_type": "phase.completed",
            "payload": {
                "status": "pass",
                "secret_raw_payload": "must-not-leak",
            },
        },
        state,
    )


def test_overlay_view_is_bounded_redacted_and_proposal_only():
    orchestrator, state = _state()
    view = orchestrator.read_overlay_view(state)
    serialized = json.dumps(view, ensure_ascii=False, sort_keys=True)

    assert view["contract_type"] == "LucidaOverlayView"
    assert view["surface"] == "LUCIDA"
    assert view["mode"] == "read_only"
    assert view["pending_proposals"]
    assert view["next_attention"]["kind"] == "proposal"
    assert view["safety"]["proposal_only"] is True
    assert "secret_raw_payload" not in serialized
    assert "metadata" not in view
    assert all("payload" not in proposal for proposal in view["pending_proposals"])


def test_overlay_view_has_deterministic_capability_and_proposal_order():
    _, state = _state()
    first = build_overlay_view(state)
    second = build_overlay_view(state.to_dict())

    assert first == second
    assert [item["capability"] for item in first["capabilities"]] == [
        "INSTAR",
        "NAYADE",
        "IMAGO",
    ]
    proposal_ids = [item["proposal_id"] for item in first["pending_proposals"]]
    assert len(proposal_ids) == len(set(proposal_ids))
    assert [item["risk"] for item in first["pending_proposals"]] == sorted(
        item["risk"] for item in first["pending_proposals"]
    )


def test_overlay_view_limits_are_explicit_and_empty_state_is_safe():
    orchestrator = LucidaOrchestrator()
    state = orchestrator.initial_state("session-empty")
    view = build_overlay_view(state, max_capabilities=1, max_proposals=0, max_unknowns=1)

    assert len(view["capabilities"]) == 1
    assert view["pending_proposals"] == []
    assert len(view["unknowns"]) == 1
    assert view["next_attention"]["kind"] == "unknown"

    with pytest.raises(ValueError, match="non-negative integer"):
        build_overlay_view(state, max_proposals=-1)


def test_overlay_view_empty_state_has_one_deterministic_phase_attention_item():
    state = LucidaState(
        session_id="session-empty",
        vj_state=VJState(session_id="session-empty"),
    )

    view = build_overlay_view(state)

    assert view["capabilities"] == []
    assert view["pending_proposals"] == []
    assert view["unknowns"] == []
    assert view["next_attention"] == {
        "kind": "phase",
        "id": "phase-preflight",
        "reason": "Awaiting the next event.",
    }


def test_overlay_diff_is_stable_and_reports_proposal_and_attention_changes():
    _, state = _state()
    previous = build_overlay_view(state)
    current = json.loads(json.dumps(previous, sort_keys=True))
    current["pending_proposals"][0]["reason"] = "Review the updated proposal."
    current["next_attention"] = {
        "kind": "unknown",
        "id": "unknown-001",
        "reason": "A safe operator review is still required.",
    }

    first = diff_overlay_view(previous, current)
    second = diff_overlay_view(previous, current)

    assert first == second
    assert [item["field"] for item in first] == ["pending_proposals", "next_attention"]
    assert first[0]["after"][0]["reason"] == "Review the updated proposal."
    assert first[1]["after"]["kind"] == "unknown"
    assert diff_overlay_view(previous, previous) == []


def test_overlay_diff_compares_only_safe_fields_and_enforces_bounds():
    _, state = _state()
    previous = build_overlay_view(state)
    current = json.loads(json.dumps(previous, sort_keys=True))
    current["session_id"] = "other-session"
    current["phase"] = "show"
    current["status"] = "changed"
    current["overlay_status"] = "changed"
    current["unknowns"] = ["Unknown change."]
    current["next_attention"] = {
        "kind": "unknown",
        "id": "unknown-001",
        "reason": "Unknown change.",
    }
    current["safety"] = dict(current["safety"])

    changes = diff_overlay_view(previous, current, max_changes=1)

    assert len(changes) == 1
    assert len(diff_overlay_view(previous, current)) <= MAX_DIFF_CHANGES
    assert changes[0]["field"] == "status"


def test_overlay_diff_rejects_non_projected_or_unsafe_inputs():
    _, state = _state()
    view = build_overlay_view(state)

    with pytest.raises(OverlayDiffError, match="mapping"):
        diff_overlay_view([], view)

    invalid_contract = dict(view)
    invalid_contract["contract_type"] = "RawState"
    with pytest.raises(OverlayDiffError, match="contract_type"):
        diff_overlay_view(view, invalid_contract)

    invalid_schema = dict(view)
    invalid_schema["schema_version"] = "9.9"
    with pytest.raises(OverlayDiffError, match="schema_version"):
        diff_overlay_view(view, invalid_schema)

    unsafe = dict(view)
    unsafe["payload"] = {"secret": "must-not-display"}
    with pytest.raises(OverlayDiffError, match="unsupported fields"):
        diff_overlay_view(view, unsafe)

    nested_unsafe = json.loads(json.dumps(view, sort_keys=True))
    nested_unsafe["pending_proposals"][0]["payload"] = {"secret": "must-not-display"}
    with pytest.raises(OverlayDiffError, match="pending_proposals"):
        diff_overlay_view(view, nested_unsafe)

    unsafe_safety = json.loads(json.dumps(view, sort_keys=True))
    unsafe_safety["safety"]["execute"] = "must-not-run"
    with pytest.raises(OverlayDiffError, match="safety"):
        diff_overlay_view(view, unsafe_safety)


def test_orchestrator_diff_projects_states_and_returns_bounded_changes():
    orchestrator, state = _state()
    equivalent = LucidaState.from_dict(state.to_dict())
    assert orchestrator.diff_overlay_view(state, equivalent) == []

    changed_proposal = replace(state.proposals[0], reason="Review the changed proposal.")
    changed = replace(state, proposals=(changed_proposal, *state.proposals[1:]))
    changes = orchestrator.diff_overlay_view(state, changed, max_changes=1)

    assert len(changes) == 1
    assert changes[0]["field"] == "pending_proposals"
    assert changes[0]["after"][0]["reason"] == "Review the changed proposal."


def test_orchestrator_diff_redacts_internal_metadata_and_payload_state():
    orchestrator, state = _state()
    private_report = replace(
        state.capabilities[0],
        state={
            **state.capabilities[0].state,
            "payload": {"secret": "must-not-leak"},
        },
    )
    private_state = replace(
        state,
        capabilities=(private_report, *state.capabilities[1:]),
        metadata={"private_path": "C:\\private", "credential": "secret"},
    )

    changes = orchestrator.diff_overlay_view(state, private_state)
    serialized = json.dumps(changes, ensure_ascii=False, sort_keys=True)

    assert changes == []
    assert "must-not-leak" not in serialized
    assert "private_path" not in serialized
    assert "credential" not in serialized


def test_orchestrator_diff_rejects_invalid_state_through_existing_contracts():
    orchestrator, state = _state()

    with pytest.raises(LucidaContractError, match="session_id"):
        orchestrator.diff_overlay_view({}, state)

    invalid_current = state.to_dict()
    invalid_current["vj_state"]["phase"] = "not-a-phase"
    with pytest.raises(ValueError, match="phase"):
        orchestrator.diff_overlay_view(state, invalid_current)


def test_overlay_contract_schemas_match_the_safe_runtime_surface():
    contracts_dir = Path(__file__).parents[2] / "lucida" / "overlay" / "contracts"
    view_schema = json.loads(
        (contracts_dir / "overlay-view.schema.json").read_text(encoding="utf-8")
    )
    diff_schema = json.loads(
        (contracts_dir / "overlay-diff.schema.json").read_text(encoding="utf-8")
    )
    _, state = _state()
    view = build_overlay_view(state)
    diff = diff_overlay_view(view, {**view, "status": "changed"})

    assert view_schema["additionalProperties"] is False
    assert set(view_schema["required"]) == set(view)
    assert diff_schema["maxItems"] == MAX_DIFF_CHANGES
    assert set(diff_schema["items"]["required"]) == {"field", "before", "after"}
    assert all(item["field"] in diff_schema["items"]["properties"]["field"]["enum"] for item in diff)


def test_overlay_contract_schemas_represent_proposal_only_safety():
    contracts_dir = Path(__file__).parents[2] / "lucida" / "overlay" / "contracts"
    view_schema = json.loads(
        (contracts_dir / "overlay-view.schema.json").read_text(encoding="utf-8")
    )
    safety = view_schema["properties"]["safety"]["properties"]
    proposal = view_schema["properties"]["pending_proposals"]["items"]["properties"]

    assert safety["proposal_only"]["const"] is True
    assert safety["automatic_actions"]["const"] is False
    assert safety["external_side_effects"]["const"] is False
    assert proposal["requires_explicit_approval"]["const"] is True
    assert proposal["reversible"]["const"] is True
    assert proposal["execution_mode"]["const"] == "proposal_only"
