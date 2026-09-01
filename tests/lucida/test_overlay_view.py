import json

import pytest

from lucida import LucidaOrchestrator
from lucida.overlay import build_overlay_view


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
