"""Deterministic replay of LUCIDA overlay JSON records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .overlay import OVERLAY_VIEW_SCHEMA_VERSION, validate_overlay_update
from .overlay_consumer import OverlayConsumer, OverlayConsumerError


class OverlayReplayError(ValueError):
    """Raised when an overlay replay envelope cannot be consumed safely."""


def replay_overlay_json(source: str | bytes | bytearray | Mapping[str, Any]) -> dict[str, Any]:
    """Replay an overlay envelope from JSON text or an already parsed mapping."""

    if isinstance(source, Mapping):
        envelope = source
    elif isinstance(source, (str, bytes, bytearray)):
        try:
            envelope = json.loads(source)
        except (TypeError, json.JSONDecodeError) as exc:
            raise OverlayReplayError("overlay replay input must be valid JSON.") from exc
    else:
        raise OverlayReplayError("overlay replay input must be JSON text or a mapping.")
    return replay_overlay_records(envelope)


def replay_overlay_path(path: str | Path) -> dict[str, Any]:
    """Replay one local JSON file without opening a transport or host."""

    replay_path = Path(path).expanduser().resolve()
    if not replay_path.is_file():
        raise OverlayReplayError(f"overlay replay file does not exist: {replay_path}")
    try:
        source = replay_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise OverlayReplayError(f"overlay replay file cannot be read: {replay_path}") from exc
    return replay_overlay_json(source)


def replay_overlay_records(envelope: Mapping[str, Any]) -> dict[str, Any]:
    """Replay snapshot, delta, and atomic update records safely."""

    records = _validated_envelope(envelope)
    consumer = OverlayConsumer()
    operations: list[dict[str, Any]] = []
    snapshot_count = 0
    delta_count = 0
    update_count = 0

    for index, record in enumerate(records):
        kind = record.get("kind")
        try:
            if kind == "snapshot":
                if index != 0 and record["recovery"] is not True:
                    raise OverlayReplayError(
                        "non-initial snapshots require recovery=true."
                    )
                consumer.accept_snapshot(
                    record["view"],
                    record["cursor"],
                    recovery=record["recovery"],
                )
                snapshot_count += 1
                change_count = 0
            elif kind == "delta":
                if not consumer.state.initialized:
                    raise OverlayReplayError("the first replay record must be a snapshot.")
                consumer.apply_delta(record["changes"], record["cursor"])
                delta_count += 1
                change_count = len(record["changes"])
            else:
                if not consumer.state.initialized:
                    raise OverlayReplayError("the first replay record must be a snapshot.")
                consumer.apply_update(record["update"])
                update_count += 1
                change_count = len(record["update"]["changes"])
        except OverlayReplayError:
            raise
        except (OverlayConsumerError, KeyError, TypeError, ValueError) as exc:
            raise OverlayReplayError(f"record {index} cannot be applied: {exc}") from exc
        current_cursor = consumer.cursor
        operations.append(
            {
                "index": index,
                "kind": kind,
                "sequence": current_cursor["sequence"],
                "change_count": change_count,
                "last_operation": consumer.state.last_operation,
            }
        )

    if not consumer.state.initialized:
        raise OverlayReplayError("overlay replay needs at least one snapshot.")
    return {
        "contract_type": "LucidaOverlayReplayReport",
        "schema_version": OVERLAY_VIEW_SCHEMA_VERSION,
        "status": "PASS",
        "record_count": len(records),
        "snapshot_count": snapshot_count,
        "delta_count": delta_count,
        "update_count": update_count,
        "applied_delta_count": consumer.state.applied_delta_count,
        "operations": operations,
        "final_view": consumer.view,
        "final_cursor": consumer.cursor,
        "checkpoint": consumer.checkpoint(),
        "safety": {
            "replay_only": True,
            "proposal_only": True,
            "automatic_actions": False,
            "external_side_effects": False,
        },
    }


def _validated_envelope(envelope: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    if not isinstance(envelope, Mapping):
        raise OverlayReplayError("overlay replay envelope must be an object.")
    required = {"contract_type", "schema_version", "records"}
    if set(envelope) != required:
        raise OverlayReplayError("overlay replay envelope contains unsupported fields.")
    if envelope.get("contract_type") != "LucidaOverlayReplay":
        raise OverlayReplayError("overlay replay contract_type is invalid.")
    if envelope.get("schema_version") != OVERLAY_VIEW_SCHEMA_VERSION:
        raise OverlayReplayError("overlay replay schema_version is invalid.")
    records = envelope.get("records")
    if not isinstance(records, list) or not records:
        raise OverlayReplayError("overlay replay needs a non-empty records list.")
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            raise OverlayReplayError(f"record {index} must be an object.")
        kind = record.get("kind")
        if kind == "snapshot":
            if set(record) != {"kind", "view", "cursor", "recovery"}:
                raise OverlayReplayError(f"snapshot record {index} has unsupported fields.")
            if not isinstance(record.get("recovery"), bool):
                raise OverlayReplayError(f"snapshot record {index} recovery must be boolean.")
        elif kind == "delta":
            if set(record) != {"kind", "changes", "cursor"}:
                raise OverlayReplayError(f"delta record {index} has unsupported fields.")
            if not isinstance(record.get("changes"), list):
                raise OverlayReplayError(f"delta record {index} changes must be a list.")
        elif kind == "update":
            if set(record) != {"kind", "update"}:
                raise OverlayReplayError(f"update record {index} has unsupported fields.")
            try:
                validate_overlay_update(record["update"])
            except ValueError as exc:
                raise OverlayReplayError(f"update record {index} is invalid: {exc}") from exc
        else:
            raise OverlayReplayError(f"record {index} kind is invalid.")
    return records


__all__ = [
    "OverlayReplayError",
    "replay_overlay_json",
    "replay_overlay_path",
    "replay_overlay_records",
]
