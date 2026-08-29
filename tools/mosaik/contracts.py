"""Contratos y perfiles reutilizables de INSTAR.

El perfil de clip es la salida estable que pueden consumir NAYADE e IMAGO.
Contiene hechos técnicos, observaciones, eventos y riesgos sin acoplarlos a un
decodificador concreto.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ANALYZER_VERSION = "0.2"
FINGERPRINT_CHUNK_SIZE = 1024 * 1024


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def fingerprint_file(path: str | Path) -> dict[str, Any]:
    """Crea una huella rápida sin leer completo un archivo de video.

    Se combinan tamaño, mtime y los extremos del archivo. Esto invalida la
    caché cuando cambia el medio sin imponer el coste de hashear varios GB.
    """

    media_path = Path(path).expanduser().resolve()
    stat = media_path.stat()
    digest = hashlib.sha256()
    digest.update(str(stat.st_size).encode("ascii"))
    digest.update(str(stat.st_mtime_ns).encode("ascii"))
    with media_path.open("rb") as handle:
        first = handle.read(FINGERPRINT_CHUNK_SIZE)
        digest.update(first)
        if stat.st_size > FINGERPRINT_CHUNK_SIZE:
            handle.seek(max(0, stat.st_size - FINGERPRINT_CHUNK_SIZE))
            digest.update(handle.read(FINGERPRINT_CHUNK_SIZE))
    return {
        "algorithm": "sha256-head-tail",
        "value": digest.hexdigest(),
        "size_bytes": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
    }


def _mean(items: list[dict[str, Any]], key: str, default: float = 0.0) -> float:
    values = [float(item[key]) for item in items if item.get(key) is not None]
    return sum(values) / len(values) if values else default


def _mean_rgb(items: list[dict[str, Any]]) -> list[float]:
    values = [item.get("mean_rgb") for item in items if isinstance(item.get("mean_rgb"), list)]
    if not values:
        return [0.0, 0.0, 0.0]
    return [sum(float(value[index]) for value in values) / len(values) for index in range(3)]


def _distance_rgb(left: list[float], right: list[float]) -> float:
    if len(left) < 3 or len(right) < 3:
        return 1.0
    return min(1.0, math.sqrt(sum((float(left[i]) - float(right[i])) ** 2 for i in range(3))) / 441.6729559)


def derive_loop_profile(analysis: dict[str, Any]) -> dict[str, Any]:
    """Estima continuidad entre el comienzo y el final de una muestra.

    Es una señal de selección, no una prueba de loop perfecto. La decisión
    usa luminancia, RGB y movimiento para evitar confiar en un solo frame.
    """

    samples = analysis.get("samples") or []
    if len(samples) < 8:
        return {
            "status": "unknown",
            "confidence": 0.0,
            "seam_luma_delta": None,
            "seam_rgb_distance": None,
            "reason": "No hubo suficientes muestras visuales para estimar continuidad.",
        }

    window = max(2, min(30, len(samples) // 10))
    start = samples[:window]
    end = samples[-window:]
    start_luma = _mean(start, "mean_luma") / 255.0
    end_luma = _mean(end, "mean_luma") / 255.0
    seam_luma_delta = abs(end_luma - start_luma)
    seam_rgb_distance = _distance_rgb(
        _mean_rgb(start),
        _mean_rgb(end),
    )
    start_motion = _mean(start, "delta") / 255.0
    end_motion = _mean(end, "delta") / 255.0
    motion_delta = min(1.0, abs(end_motion - start_motion))
    continuity = max(
        0.0,
        min(1.0, 1.0 - (0.45 * min(1.0, seam_luma_delta * 4.0) + 0.4 * seam_rgb_distance + 0.15 * motion_delta)),
    )
    if continuity >= 0.78:
        status = "candidate"
    elif continuity >= 0.55:
        status = "review"
    else:
        status = "weak"
    return {
        "status": status,
        "confidence": round(continuity, 6),
        "seam_luma_delta": round(seam_luma_delta, 6),
        "seam_rgb_distance": round(seam_rgb_distance, 6),
        "motion_delta": round(motion_delta, 6),
        "sample_window": window,
        "basis": "sampled_luminance_rgb_motion_continuity",
    }


def _temporal_series(analysis: dict[str, Any]) -> dict[str, Any] | None:
    samples = analysis.get("samples") or []
    if not samples:
        return None
    return {
        "timestamps_s": [item.get("time_s") for item in samples],
        "luminance": [round(float(item.get("mean_luma", 0.0)) / 255.0, 6) for item in samples],
        "motion": [
            round(float(item.get("delta", 0.0) or 0.0) / 255.0, 6)
            for item in samples
        ],
        "saturation": [round(float(item.get("saturation", 0.0)), 6) for item in samples],
        "sample_count": len(samples),
        "sample_rate_hz": analysis.get("sample_rate_hz"),
        "resolution": "per_sample",
    }


def build_clip_profile(
    report: dict[str, Any],
    fingerprint: dict[str, Any] | None = None,
    *,
    source_path: str | Path | None = None,
) -> dict[str, Any]:
    """Construye el contrato de clip a partir del informe actual de INSTAR."""

    input_path = Path(str(source_path or report.get("input", "media"))).expanduser().resolve()
    video = report.get("video") or {}
    analysis = report.get("analysis") or {}
    flash = analysis.get("flash_screening") or {}
    profile = {
        "schema_version": "0.1",
        "profile_type": "ClipProfile",
        "profile_id": (fingerprint or {}).get("value") or input_path.name,
        "generated_at": utc_now(),
        "analyzer": {
            "name": "INSTAR",
            "version": ANALYZER_VERSION,
            "mode": report.get("mode") or analysis.get("backend") or "technical",
            "backend": analysis.get("backend") or "ffprobe",
        },
        "source": {
            "path": str(input_path),
            "filename": input_path.name,
            "extension": input_path.suffix.lower(),
            "fingerprint": fingerprint,
        },
        "technical": {
            "container": report.get("container"),
            "video": video,
            "audio": report.get("audio"),
            "alpha": report.get("alpha"),
        },
        "visual": {
            "status": analysis.get("status", "not_run"),
            "resolution": analysis.get("analysis_resolution"),
            "luminance": analysis.get("luminance"),
            "color": analysis.get("color"),
            "motion": analysis.get("motion"),
            "visual_energy": analysis.get("visual_energy"),
            "periodicity": analysis.get("periodicity"),
            "loop": derive_loop_profile(analysis),
        },
        "events": {
            "flash_candidates": flash.get("candidates", [])[:50],
            "visual_peaks": (analysis.get("visual_peaks") or [])[:50],
        },
        "temporal_series": _temporal_series(analysis),
        "compatibility": {
            "status": report.get("overall_status"),
            "checks": report.get("checks", []),
            "recommendations": report.get("recommendations", []),
        },
        "limitations": report.get("limitations", []),
    }
    return profile


def analysis_cache_key(
    *,
    mode: str,
    target_fps: float | None,
    target_width: int | None,
    target_height: int | None,
    target_codec: str | None,
    max_samples: int,
    gpu_max_frames: int,
    gpu_batch_size: int,
    show_profile_id: str | None,
) -> str:
    payload = {
        "mode": mode,
        "target_fps": target_fps,
        "target_width": target_width,
        "target_height": target_height,
        "target_codec": target_codec,
        "max_samples": max_samples,
        "gpu_max_frames": gpu_max_frames,
        "gpu_batch_size": gpu_batch_size,
        "show_profile_id": show_profile_id,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))
