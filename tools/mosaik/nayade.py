"""Read-only soundcheck planning and result recording for NAYADE."""

from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .media import MosaikError


SCHEMA_VERSION = "0.1"
RESULTS = ("planned", "running", "approved", "rejected", "review")
OPERATIONS = (
    "baseline",
    "flip_horizontal",
    "flip_vertical",
    "rotate_180",
    "pattern",
    "marquee",
)


class NayadeError(MosaikError):
    """Raised when a NAYADE soundcheck contract is invalid."""


def build_soundcheck_session(
    source: Mapping[str, Any],
    *,
    session_id: str,
    name: str,
    seed: int = 0,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Build a deterministic soundcheck plan from a mapping summary."""

    _text(session_id, "session_id")
    _text(name, "name")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise NayadeError("seed must be an integer.")
    if not isinstance(source, Mapping):
        raise NayadeError("source must be an object.")
    timestamp = created_at or _now()
    _timestamp(timestamp, "created_at")
    slices = _normalize_slices(source)
    groups = _input_groups(slices)
    planned_steps = _planned_steps(groups, seed)
    session = {
        "schema_version": SCHEMA_VERSION,
        "session_type": "NayadeSoundcheckSession",
        "session_id": session_id.strip(),
        "name": name.strip(),
        "created_at": timestamp,
        "updated_at": timestamp,
        "read_only_source": True,
        "source": {
            "source_type": str(source.get("source_type", "mapping_summary")),
            "slice_count": len(slices),
            "input_group_count": len(groups),
        },
        "composition": _safe_mapping(source.get("composition")),
        "seed": seed,
        "targets": {"slices": slices, "input_groups": groups},
        "planned_steps": planned_steps,
        "events": [],
        "limitations": [
            "NAYADE does not open ports or send processor commands.",
            "A result records operator evidence; it does not prove hardware state.",
            "Unknown processor and module fields remain explicit until confirmed.",
        ],
    }
    validate_session(session)
    return session


def load_session(path: str | Path) -> dict[str, Any]:
    session_path = Path(path).expanduser().resolve()
    if not session_path.is_file():
        raise NayadeError(f"NAYADE session does not exist: {session_path}")
    try:
        value = json.loads(session_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise NayadeError(f"NAYADE session cannot be read: {session_path}") from exc
    validate_session(value)
    return value


def write_session(session: Mapping[str, Any], path: str | Path) -> Path:
    validate_session(session)
    output = Path(path).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(session, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output


def next_step(session: Mapping[str, Any]) -> dict[str, Any] | None:
    """Return the first unresolved step in deterministic plan order."""

    validate_session(session)
    for step in session["planned_steps"]:
        if step["result"] in {"planned", "running"}:
            return copy.deepcopy(step)
    return None


def record_result(
    session: Mapping[str, Any],
    *,
    result: str,
    operation: str | None = None,
    scope: str | None = None,
    targets: list[str] | tuple[str, ...] | None = None,
    step_id: str | None = None,
    parameters: Mapping[str, Any] | None = None,
    notes: str = "",
    recorded_at: str | None = None,
) -> dict[str, Any]:
    """Record an explicit operator result without changing the source mapping."""

    validate_session(session)
    if result not in RESULTS:
        raise NayadeError(f"result must be one of: {', '.join(RESULTS)}")
    if operation is not None and operation not in OPERATIONS:
        raise NayadeError(f"unknown operation: {operation}")
    if scope is not None and not isinstance(scope, str):
        raise NayadeError("scope must be text.")
    target_list = _targets(targets)
    if parameters is not None and not isinstance(parameters, Mapping):
        raise NayadeError("parameters must be an object.")
    if not isinstance(notes, str):
        raise NayadeError("notes must be text.")

    updated = copy.deepcopy(dict(session))
    selected = _select_step(updated["planned_steps"], step_id, operation, scope, target_list)
    selected["result"] = result
    timestamp = recorded_at or _now()
    _timestamp(timestamp, "recorded_at")
    event = {
        "event_id": f"event-{len(updated['events']) + 1:03d}",
        "created_at": timestamp,
        "operation": selected["operation"],
        "scope": selected["scope"],
        "targets": target_list or list(selected["targets"]),
        "parameters": _safe_mapping(parameters),
        "result": result,
        "notes": notes,
        "planned_step_id": selected["step_id"],
    }
    updated["events"].append(event)
    updated["updated_at"] = timestamp
    validate_session(updated)
    return updated


def build_processor_observation(
    *,
    model: str | None = None,
    firmware: str | None = None,
    transport: str = "unknown",
    evidence: list[str] | tuple[str, ...] = (),
    confidence: str = "unknown",
    input_signal: Mapping[str, Any] | None = None,
    output_signal: Mapping[str, Any] | None = None,
    module_profile: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a passive processor observation; no device discovery is attempted."""

    if transport not in {"unknown", "usb", "serial", "ethernet", "hdmi", "manual"}:
        raise NayadeError("transport is not supported.")
    if confidence not in {"unknown", "low", "medium", "high"}:
        raise NayadeError("confidence is not supported.")
    for value, field_name in ((model, "model"), (firmware, "firmware")):
        if value is not None:
            _text(value, field_name)
    if not isinstance(evidence, (list, tuple)) or not all(isinstance(item, str) for item in evidence):
        raise NayadeError("evidence must be a list of text.")
    return {
        "schema_version": SCHEMA_VERSION,
        "observation_type": "NayadeProcessorObservation",
        "model": model,
        "firmware": firmware,
        "transport": transport,
        "confidence": confidence,
        "evidence": list(evidence),
        "input_signal": _safe_mapping(input_signal),
        "output_signal": _safe_mapping(output_signal),
        "module_profile": _safe_mapping(module_profile),
        "read_only": True,
        "commands_sent": False,
        "unknowns": [
            "Processor configuration is not confirmed by this observation alone.",
            "Module profile requires declared or measured venue evidence.",
        ],
    }


def validate_session(value: Mapping[str, Any]) -> None:
    """Validate the fields NAYADE writes and consumes."""

    if not isinstance(value, Mapping):
        raise NayadeError("session must be an object.")
    required = {
        "schema_version",
        "session_type",
        "session_id",
        "name",
        "created_at",
        "updated_at",
        "read_only_source",
        "source",
        "composition",
        "seed",
        "targets",
        "planned_steps",
        "events",
        "limitations",
    }
    if set(value) - required or required - set(value):
        raise NayadeError("session fields do not match the NAYADE contract.")
    if value["schema_version"] != SCHEMA_VERSION or value["session_type"] != "NayadeSoundcheckSession":
        raise NayadeError("session contract identity is invalid.")
    _text(value["session_id"], "session_id")
    _text(value["name"], "name")
    _timestamp(value["created_at"], "created_at")
    _timestamp(value["updated_at"], "updated_at")
    if value["read_only_source"] is not True:
        raise NayadeError("read_only_source must be true.")
    if not isinstance(value["source"], Mapping) or not isinstance(value["targets"], Mapping):
        raise NayadeError("source and targets must be objects.")
    if isinstance(value["seed"], bool) or not isinstance(value["seed"], int):
        raise NayadeError("seed must be an integer.")
    if not isinstance(value["planned_steps"], list) or not isinstance(value["events"], list):
        raise NayadeError("planned_steps and events must be lists.")
    if not isinstance(value["limitations"], list) or not all(isinstance(item, str) for item in value["limitations"]):
        raise NayadeError("limitations must be a list of text.")
    for step in value["planned_steps"]:
        if not isinstance(step, Mapping):
            raise NayadeError("each planned step must be an object.")
        if set(step) != {"step_id", "operation", "scope", "targets", "parameters", "expected_checks", "result"}:
            raise NayadeError("planned step fields are invalid.")
        _text(step["step_id"], "step_id")
        if step["operation"] not in OPERATIONS or step["result"] not in RESULTS:
            raise NayadeError("planned step operation or result is invalid.")
        _text(step["scope"], "scope")
        if not isinstance(step["targets"], list) or not all(isinstance(item, str) for item in step["targets"]):
            raise NayadeError("planned step targets must be a list of text.")
        if not isinstance(step["parameters"], Mapping) or not isinstance(step["expected_checks"], list):
            raise NayadeError("planned step parameters or expected_checks are invalid.")
    for event in value["events"]:
        if not isinstance(event, Mapping):
            raise NayadeError("each event must be an object.")
        required_event = {"event_id", "created_at", "operation", "scope", "targets", "parameters", "result", "notes", "planned_step_id"}
        if set(event) != required_event:
            raise NayadeError("event fields are invalid.")
        _text(event["event_id"], "event_id")
        _timestamp(event["created_at"], "event.created_at")
        if event["operation"] not in OPERATIONS or event["result"] not in RESULTS:
            raise NayadeError("event operation or result is invalid.")
        if not isinstance(event["targets"], list) or not isinstance(event["parameters"], Mapping):
            raise NayadeError("event targets or parameters are invalid.")
        if not isinstance(event["notes"], str):
            raise NayadeError("event notes must be text.")


def _normalize_slices(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw_slices = source.get("slices")
    if raw_slices is None and isinstance(source.get("targets"), Mapping):
        raw_slices = source["targets"].get("slices")
    if raw_slices is None:
        raw_slices = []
    if not isinstance(raw_slices, list):
        raise NayadeError("source slices must be a list.")
    result: list[dict[str, Any]] = []
    for index, raw_slice in enumerate(raw_slices, start=1):
        if not isinstance(raw_slice, Mapping):
            raise NayadeError("each source slice must be an object.")
        slice_id = str(raw_slice.get("slice_id", raw_slice.get("id", f"slice-{index:03d}")))
        group_id = str(raw_slice.get("input_group_id", raw_slice.get("inputGroupId", f"group-{index:03d}")))
        _text(slice_id, "slice_id")
        _text(group_id, "input_group_id")
        result.append({"slice_id": slice_id, "input_group_id": group_id})
    return result


def _input_groups(slices: list[dict[str, Any]]) -> list[str]:
    groups = sorted({item["input_group_id"] for item in slices})
    return groups or ["global"]


def _planned_steps(groups: list[str], seed: int) -> list[dict[str, Any]]:
    definitions = (
        ("baseline", "input_group", {}, ["Confirm signal lock and clean baseline."]),
        ("flip_horizontal", "input_group", {"axis": "horizontal"}, ["Check horizontal orientation and slice boundaries."]),
        ("flip_vertical", "input_group", {"axis": "vertical"}, ["Check vertical orientation and slice boundaries."]),
        ("rotate_180", "input_group", {"degrees": 180}, ["Check rotation without stretching or neighbor invasion."]),
        ("pattern", "input_group", {"mode": "color_grid", "seed": seed}, ["Check group identity, seams, and geometry."]),
        ("marquee", "input_group", {"axis": "horizontal", "wrap": True}, ["Check repeatability on extreme aspect ratios."]),
    )
    return [
        {
            "step_id": f"step-{index:03d}",
            "operation": operation,
            "scope": scope,
            "targets": list(groups),
            "parameters": parameters,
            "expected_checks": expected_checks,
            "result": "planned",
        }
        for index, (operation, scope, parameters, expected_checks) in enumerate(definitions, start=1)
    ]


def _select_step(
    steps: list[dict[str, Any]],
    step_id: str | None,
    operation: str | None,
    scope: str | None,
    targets: list[str],
) -> dict[str, Any]:
    candidates = [step for step in steps if step["result"] in {"planned", "running"}]
    if step_id is not None:
        candidates = [step for step in candidates if step["step_id"] == step_id]
    if operation is not None:
        candidates = [step for step in candidates if step["operation"] == operation]
    if scope is not None:
        candidates = [step for step in candidates if step["scope"] == scope]
    if targets:
        candidates = [step for step in candidates if set(targets).intersection(step["targets"])]
    if not candidates:
        raise NayadeError("no pending step matches the requested result.")
    return candidates[0]


def _targets(value: list[str] | tuple[str, ...] | None) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, (list, tuple)) or not all(isinstance(item, str) and item.strip() for item in value):
        raise NayadeError("targets must be a list of non-empty text.")
    return [item.strip() for item in value]


def _safe_mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise NayadeError("mapping values must be objects.")
    try:
        return json.loads(json.dumps(dict(value), ensure_ascii=True, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise NayadeError("mapping values must be JSON serializable.") from exc


def _text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise NayadeError(f"{field_name} must be non-empty text.")
    return value.strip()


def _timestamp(value: Any, field_name: str) -> str:
    text = _text(value, field_name)
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise NayadeError(f"{field_name} must be ISO-8601.") from exc
    return text


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


__all__ = [
    "NayadeError",
    "OPERATIONS",
    "RESULTS",
    "build_processor_observation",
    "build_soundcheck_session",
    "load_session",
    "next_step",
    "record_result",
    "validate_session",
    "write_session",
]
