import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from tools.mosaik.media import MosaikError
from tools.mosaik.protocol import build_soundcheck_protocol


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schemas" / "nayade-soundcheck-protocol.schema.json"


def _validate(report):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(report)) == []


def test_protocol_has_safe_baseline_without_evidence():
    report = build_soundcheck_protocol()

    assert report["status"] == "READY"
    assert report["source_documents"] == []
    assert report["steps"][0]["pattern"] == "blackout"
    assert report["summary"]["step_count"] == len(report["steps"])
    assert report["safety"]["patterns_emitted"] is False
    _validate(report)


def test_protocol_promotes_checks_from_chain_evidence():
    report = build_soundcheck_protocol(
        reconciliation={
            "status": "FAIL",
            "conflicts": [
                {"id": "range_mismatch", "severity": "high"},
                {"id": "resolution_mismatch_signal_source_mapping_composition", "severity": "review"},
            ],
            "calculations": [{"id": "processor_scaling", "value": True}],
            "facts": [
                {"subject": "gpu.output", "property": "color_range", "value": "unknown"},
            ],
        },
        mapping={"mapping_distortion_risk": True, "validation": {"status": "FAIL"}},
    )

    by_pattern = {step["pattern"]: step for step in report["steps"]}
    assert report["status"] == "REVIEW"
    assert {"range_mismatch", "processor_scaling", "mapping_distortion_risk"}.issubset(report["evidence_ids"])
    assert by_pattern["pluge_near_black"]["priority"] == "required"
    assert "range_mismatch" in by_pattern["pluge_near_black"]["triggered_by"]
    assert by_pattern["resolution_scaling"]["priority"] == "required"
    assert by_pattern["geometry_grid"]["priority"] == "required"
    assert all(step["execution_mode"] == "plan_only" for step in report["steps"])
    _validate(report)


def test_protocol_rejects_non_object_documents():
    with pytest.raises(MosaikError, match="debe ser un objeto"):
        build_soundcheck_protocol(reconciliation=["not-an-object"])


def test_protocol_does_not_copy_source_paths():
    report = build_soundcheck_protocol(
        case_report={"findings": [{"id": "raised_black_level", "detail": "C:\\private\\case.json"}]},
        reconciliation={"conflicts": []},
    )

    serialized = json.dumps(report, ensure_ascii=False)
    assert "private" not in serialized
    assert report["safety"]["source_paths_exposed"] is False
