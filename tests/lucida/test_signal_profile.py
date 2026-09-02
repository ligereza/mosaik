import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from lucida.signals import SignalProfileError, validate_signal_profile


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
