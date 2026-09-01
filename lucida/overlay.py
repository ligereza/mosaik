"""Bounded read-only view for the future LUCIDA overlay surface."""

from __future__ import annotations

from typing import Any, Mapping

from adapters.vj.contracts import VJProposal

from .contracts import CAPABILITY_NAMES, LucidaState


OVERLAY_VIEW_SCHEMA_VERSION = "0.1"
_DEFAULT_CAPABILITY_LIMIT = 3
_DEFAULT_PROPOSAL_LIMIT = 8
_DEFAULT_UNKNOWNS_LIMIT = 8
_RISK_ORDER = {"high": 0, "medium": 1, "low": 2}
_SAFE_STATE_KEYS = (
    "status",
    "media_status",
    "signal_status",
    "show_status",
    "recovery_status",
)


def build_overlay_view(
    state: LucidaState | Mapping[str, Any],
    *,
    max_capabilities: int = _DEFAULT_CAPABILITY_LIMIT,
    max_proposals: int = _DEFAULT_PROPOSAL_LIMIT,
    max_unknowns: int = _DEFAULT_UNKNOWNS_LIMIT,
) -> dict[str, Any]:
    """Project internal state into bounded data for a read-only overlay.

    The projection deliberately omits event payloads, arbitrary metadata,
    filesystem paths, credentials, and host execution details.
    """

    current = state if isinstance(state, LucidaState) else LucidaState.from_dict(state)
    limits = (
        (max_capabilities, "max_capabilities"),
        (max_proposals, "max_proposals"),
        (max_unknowns, "max_unknowns"),
    )
    for limit, name in limits:
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
            raise ValueError(f"{name} must be a non-negative integer")

    capability_order = {name: index for index, name in enumerate(CAPABILITY_NAMES)}
    reports = sorted(
        current.capabilities,
        key=lambda report: (capability_order.get(report.capability, len(CAPABILITY_NAMES)), report.capability),
    )[:max_capabilities]
    capability_views = [
        {
            "capability": report.capability,
            "state": _safe_state(report.state),
            "observed_count": len(report.observed),
            "expected_result_count": len(report.expected_results),
            "unknowns": sorted(set(report.unknowns))[:max_unknowns],
        }
        for report in reports
    ]

    pending_ids = set(current.vj_state.pending_proposal_ids)
    proposals = [
        proposal
        for proposal in current.proposals
        if proposal.proposal_id in pending_ids
    ]
    proposals.sort(
        key=lambda proposal: (
            _RISK_ORDER.get(proposal.risk, len(_RISK_ORDER)),
            proposal.phase,
            proposal.operation,
            proposal.proposal_id,
        )
    )
    proposal_views = [_proposal_view(proposal) for proposal in proposals[:max_proposals]]

    unknowns = sorted(
        {
            unknown
            for report in current.capabilities
            for unknown in report.unknowns
            if isinstance(unknown, str) and unknown.strip()
        }
    )[:max_unknowns]
    next_attention = _next_attention(proposal_views, unknowns, current.vj_state.phase)

    return {
        "contract_type": "LucidaOverlayView",
        "schema_version": OVERLAY_VIEW_SCHEMA_VERSION,
        "surface": "LUCIDA",
        "mode": "read_only",
        "session_id": current.session_id,
        "phase": current.vj_state.phase,
        "status": current.vj_state.status,
        "overlay_status": current.overlay_status,
        "capabilities": capability_views,
        "pending_proposals": proposal_views,
        "unknowns": unknowns,
        "next_attention": next_attention,
        "safety": {
            "proposal_only": True,
            "automatic_actions": False,
            "external_side_effects": False,
        },
    }


def _safe_state(value: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        return {}
    safe: dict[str, Any] = {}
    for key in _SAFE_STATE_KEYS:
        item = value.get(key)
        if isinstance(item, (str, int, float, bool)) or item is None:
            safe[key] = item
    return safe


def _proposal_view(proposal: VJProposal) -> dict[str, Any]:
    return {
        "proposal_id": proposal.proposal_id,
        "event_id": proposal.event_id,
        "phase": proposal.phase,
        "operation": proposal.operation,
        "reason": proposal.reason,
        "risk": proposal.risk,
        "requires_explicit_approval": True,
        "reversible": True,
        "execution_mode": "proposal_only",
    }


def _next_attention(
    proposals: list[dict[str, Any]],
    unknowns: list[str],
    phase: str,
) -> dict[str, Any]:
    if proposals:
        proposal = proposals[0]
        return {
            "kind": "proposal",
            "id": proposal["proposal_id"],
            "reason": proposal["reason"],
        }
    if unknowns:
        return {"kind": "unknown", "id": "unknown-001", "reason": unknowns[0]}
    return {"kind": "phase", "id": f"phase-{phase}", "reason": "Awaiting the next event."}


__all__ = ["OVERLAY_VIEW_SCHEMA_VERSION", "build_overlay_view"]
