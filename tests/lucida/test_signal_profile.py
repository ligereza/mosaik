import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from lucida import LucidaOrchestrator
from lucida.signals import (
    SignalProfileError,
    compare_signal_profiles,
    validate_signal_profile,
)


def _fact(value, origin="observed", confidence=0.9):
    return {"value": value, "origin": origin, "confidence": confidence, "source": "test"}


def _profile():
    return {
        "schema_version": "0.1",
        "profile_id": "profile-001",
        "stage": "NAYADE",
        "generated_at": "2026-01-10T20:00:00Z",
        "source": {
            "resolution": _fact("1920x1080"),
            "fps": _fact(60),
            "color_model": _fact("RGB"),
            "range": _fact("full", "declared", 1.0),
            "transfer": _fact("sRGB"),
            "primaries": _fact("BT.709"),
            "bit_depth": _fact(8),
        },
        "capture": {
            "resolution": _fact("1920x1080"),
            "refresh_hz": _fact(60),
            "format": _fact("RGB8"),
            "lock": _fact(True),
        },
        "house": {
            "input": _fact("HDMI-1", "declared", 0.7),
            "bus": _fact("main"),
            "destinations": _fact(["LED-A"]),
            "outputs": _fact(["screen-1"]),
        },
        "processor": {
            "vendor": _fact("unknown", "unknown", 0.0),
            "model": _fact("unknown", "unknown", 0.0),
            "read_only": True,
            "capabilities": {"supports_read_only_query": "unknown"},
        },
        "recommendation": {
            "range_transform": "identity",
            "gamma_transform": "identity",
            "deband": False,
            "deflicker": False,
        },
        "evidence": [{"kind": "capture-lock", "status": "PASS", "detail": "Signal locked."}],
    }


def test_signal_profile_roundtrip_is_canonical_and_detached():
    profile = _profile()

    validated = validate_signal_profile(profile)

    assert validated == profile
    assert validated is not profile
    assert validated["source"] is not profile["source"]
    profile["source"]["fps"]["value"] = 30
    assert validated["source"]["fps"]["value"] == 60


def test_signal_profile_omits_optional_empty_evidence_and_sorts_capabilities():
    profile = _profile()
    profile.pop("evidence")
    profile["processor"]["capabilities"] = {"zeta": "no", "alpha": "yes"}

    validated = validate_signal_profile(profile)

    assert "evidence" not in validated
    assert list(validated["processor"]["capabilities"]) == ["alpha", "zeta"]


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("source", "fps", "confidence"), 1.1),
        (("source", "fps", "origin"), "guessed"),
        (("processor", "capabilities", "query"), "maybe"),
        (("recommendation", "deflicker"), "no"),
    ],
)
def test_signal_profile_rejects_invalid_facts_and_recommendations(path, value):
    profile = copy.deepcopy(_profile())
    target = profile
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value

    with pytest.raises(SignalProfileError):
        validate_signal_profile(profile)


def test_signal_profile_rejects_unknown_fields_and_timezone_free_timestamp():
    profile = _profile()
    profile["unexpected"] = True
    with pytest.raises(SignalProfileError, match="unsupported or missing"):
        validate_signal_profile(profile)

    profile = _profile()
    profile["generated_at"] = "2026-01-10T20:00:00"
    with pytest.raises(SignalProfileError, match="timezone"):
        validate_signal_profile(profile)


def test_signal_profile_matches_public_schema():
    schema_path = Path(__file__).parents[2] / "schemas" / "signal-profile.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    instance = validate_signal_profile(_profile())

    errors = list(Draft202012Validator(schema).iter_errors(instance))

    assert errors == []


def test_nayade_projects_only_safe_signal_profile_metrics():
    state = LucidaOrchestrator().initial_state("session-001")
    state = LucidaOrchestrator().propose(
        {
            "event_id": "evt-soundcheck",
            "timestamp": "2026-01-10T20:00:00Z",
            "phase": "preparation",
            "event_type": "soundcheck.profile",
            "payload": {
                "signal_status": "stable",
                "processor_status": "observed",
                "signal_profile": _profile(),
            },
        },
        state,
    )

    overlay = LucidaOrchestrator().read_overlay(state)
    nayade = next(item for item in overlay["capabilities"] if item["capability"] == "NAYADE")

    assert nayade["state"]["profile_status"] == "valid"
    assert nayade["state"]["profile_stage"] == "NAYADE"
    assert nayade["state"]["profile_unknown_count"] == 2
    assert nayade["state"]["profile_inferred_count"] == 0
    assert nayade["state"]["profile_min_confidence"] == 0.0
    assert nayade["state"]["processor_read_only"] is True
    assert "1920x1080" not in json.dumps(overlay)


def test_nayade_marks_malformed_signal_profile_without_failing_the_event():
    profile = _profile()
    del profile["source"]["fps"]
    state = LucidaOrchestrator().initial_state("session-001")
    state = LucidaOrchestrator().propose(
        {
            "event_id": "evt-invalid-profile",
            "timestamp": "2026-01-10T20:00:00Z",
            "phase": "preparation",
            "event_type": "soundcheck.profile",
            "payload": {"signal_profile": profile},
        },
        state,
    )

    overlay = LucidaOrchestrator().read_overlay(state)
    nayade = next(item for item in overlay["capabilities"] if item["capability"] == "NAYADE")

    assert nayade["state"]["profile_status"] == "invalid"


def test_compare_signal_profiles_reports_drift_without_raw_values():
    expected = _profile()
    observed = copy.deepcopy(expected)
    observed["source"]["range"]["value"] = "limited"
    observed["source"]["range"]["confidence"] = 0.4
    observed["house"]["input"]["origin"] = "unknown"

    comparison = compare_signal_profiles(expected, observed)

    assert comparison["status"] == "changed"
    assert comparison["changed_fields"] == ["source.range"]
    assert comparison["confidence_drops"] == ["source.range"]
    assert comparison["origin_changes"] == ["house.input"]
    assert comparison["unknown_delta"] == 1
    assert "limited" not in json.dumps(comparison)


def test_nayade_projects_profile_drift_metrics():
    expected = _profile()
    observed = copy.deepcopy(expected)
    observed["capture"]["refresh_hz"]["value"] = 50
    state = LucidaOrchestrator().initial_state("session-001")
    state = LucidaOrchestrator().propose(
        {
            "event_id": "evt-profile-drift",
            "timestamp": "2026-01-10T20:00:00Z",
            "phase": "preparation",
            "event_type": "soundcheck.profile.compare",
            "payload": {
                "signal_profile": observed,
                "baseline_signal_profile": expected,
            },
        },
        state,
    )

    overlay = LucidaOrchestrator().read_overlay(state)
    nayade = next(item for item in overlay["capabilities"] if item["capability"] == "NAYADE")

    assert nayade["state"]["profile_comparison_status"] == "changed"
    assert nayade["state"]["profile_changed_count"] == 1
    assert nayade["state"]["profile_confidence_drop_count"] == 0
    assert nayade["state"]["profile_unknown_delta"] == 0


def test_imago_preserves_profile_drift_metrics_for_show():
    expected = _profile()
    observed = copy.deepcopy(expected)
    observed["source"]["range"]["value"] = "limited"
    state = LucidaOrchestrator().initial_state("session-001")
    state = LucidaOrchestrator().propose(
        {
            "event_id": "evt-preparation",
            "timestamp": "2026-01-10T21:00:00Z",
            "phase": "preparation",
            "event_type": "phase.completed",
            "payload": {"status": "pass"},
        },
        state,
    )
    state = LucidaOrchestrator().propose(
        {
            "event_id": "evt-show-profile-drift",
            "timestamp": "2026-01-10T22:00:00Z",
            "phase": "show",
            "event_type": "show.profile.observe",
            "payload": {
                "mode": "improvised",
                "signal_profile": observed,
                "baseline_signal_profile": expected,
            },
        },
        state,
    )

    overlay = LucidaOrchestrator().read_overlay(state)
    imago = next(item for item in overlay["capabilities"] if item["capability"] == "IMAGO")

    assert imago["state"]["profile_status"] == "valid"
    assert imago["state"]["profile_comparison_status"] == "changed"
    assert imago["state"]["profile_changed_count"] == 1
    assert "limited" not in json.dumps(overlay)
