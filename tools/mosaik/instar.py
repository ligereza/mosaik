"""Preflight de media para la etapa INSTAR."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .diagnose import diagnose_file
from .gpu import GpuUnavailable, analyze_visual_gpu
from .media import MosaikError
from .preflight import preflight_file, write_sidecar


MEDIA_EXTENSIONS = frozenset(
    {
        ".avi",
        ".dxv",
        ".mkv",
        ".mov",
        ".mp4",
        ".mxf",
        ".webm",
    }
)


def discover_media_files(root: str | Path) -> list[Path]:
    """Encuentra medios compatibles dentro de una carpeta, de forma estable."""

    media_root = Path(root).expanduser().resolve()
    if not media_root.is_dir():
        raise MosaikError(f"No se encontró la carpeta de media: {media_root}")

    return sorted(
        path
        for path in media_root.rglob("*")
        if path.is_file() and path.suffix.lower() in MEDIA_EXTENSIONS
    )


def run_instar(
    root: str | Path,
    *,
    ffmpeg: str = "ffmpeg",
    ffprobe: str = "ffprobe",
    target_fps: float | None = None,
    target_width: int | None = None,
    target_height: int | None = None,
    max_samples: int = 300,
    target_codec: str | None = None,
    deep: bool = False,
    sidecars_dir: str | Path | None = None,
    gpu: bool = False,
    gpu_max_frames: int = 900,
    gpu_batch_size: int = 16,
) -> dict[str, Any]:
    """Ejecuta el preflight de INSTAR sobre todos los medios de una carpeta.

    El modo normal inspecciona sólo metadata técnica. ``deep=True`` conserva
    el diagnóstico anterior, que además decodifica una muestra de luminancia.
    ``gpu=True`` usa NVDEC/CUDA y no hace fallback silencioso a CPU.
    """

    media_root = Path(root).expanduser().resolve()
    files = discover_media_files(media_root)
    if not files:
        raise MosaikError(f"No se encontraron videos compatibles en: {media_root}")

    items: list[dict[str, Any]] = []
    for media_path in files:
        try:
            if gpu:
                report = preflight_file(
                    media_path,
                    ffprobe=ffprobe,
                    target_fps=target_fps,
                    target_width=target_width,
                    target_height=target_height,
                    target_codec=target_codec,
                )
                try:
                    visual_analysis = analyze_visual_gpu(
                        media_path,
                        max_frames=gpu_max_frames,
                        batch_size=gpu_batch_size,
                    )
                    report["analysis"] = visual_analysis
                    candidate_count = visual_analysis["flash_screening"]["candidate_count"]
                    if candidate_count:
                        report["checks"].append(
                            {
                                "name": "Flash visual",
                                "status": "WARN",
                                "detail": f"Se detectaron {candidate_count} cambios globales de luminancia que requieren revisión.",
                            }
                        )
                        report["overall_status"] = "WARN"
                        report["recommendations"].append(
                            "Revisar los candidatos de flash; movimiento y cortes también pueden producir esta señal."
                        )
                    else:
                        report["checks"].append(
                            {
                                "name": "Análisis GPU",
                                "status": "PASS",
                                "detail": "NVDEC/CUDA procesó la muestra visual sin candidatos de flash global.",
                            }
                        )
                except GpuUnavailable as exc:
                    report["analysis"] = {
                        "status": "GPU_UNAVAILABLE",
                        "backend": "cuda_nvdec_cupy",
                        "error": str(exc),
                    }
                    report["checks"].append(
                        {
                            "name": "Análisis GPU",
                            "status": "WARN",
                            "detail": str(exc),
                        }
                    )
                    report["recommendations"].append(
                        "No se aplicó fallback CPU; usar un codec compatible con NVDEC o analizarlo manualmente."
                    )
                    report["overall_status"] = "WARN"
            elif deep:
                report = diagnose_file(
                    media_path,
                    ffmpeg=ffmpeg,
                    ffprobe=ffprobe,
                    target_fps=target_fps,
                    target_width=target_width,
                    target_height=target_height,
                    max_samples=max_samples,
                )
            else:
                report = preflight_file(
                    media_path,
                    ffprobe=ffprobe,
                    target_fps=target_fps,
                    target_width=target_width,
                    target_height=target_height,
                    target_codec=target_codec,
                )
        except MosaikError as exc:
            items.append(
                {
                    "path": str(media_path),
                    "status": "FAIL",
                    "error": str(exc),
                }
            )
            continue

        sidecar_path = None
        if sidecars_dir is not None:
            relative_parent = media_path.parent.relative_to(media_root)
            sidecar_path = write_sidecar(report, Path(sidecars_dir) / relative_parent)

        item = {
            "path": str(media_path),
            "status": report.get("overall_status", "WARN"),
            "report": report,
        }
        if sidecar_path is not None:
            item["sidecar"] = str(sidecar_path)
        items.append(
            item
        )

    statuses = {item["status"] for item in items}
    if "FAIL" in statuses:
        overall_status = "FAIL"
    elif "WARN" in statuses:
        overall_status = "WARN"
    else:
        overall_status = "PASS"

    return {
        "schema_version": "0.1",
        "tool": "INSTAR",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "media_root": str(media_root),
        "files_found": len(files),
        "mode": "gpu" if gpu else ("deep" if deep else "technical"),
        "overall_status": overall_status,
        "items": items,
    }


def text_report(report: dict[str, Any]) -> str:
    """Convierte un informe INSTAR en una salida breve para PowerShell."""

    lines = [
        "INSTAR",
        "======",
        f"Carpeta: {report['media_root']}",
        f"Modo: {report.get('mode', 'technical')}",
        f"Estado: {report['overall_status']}",
        f"Archivos: {report['files_found']}",
        "",
        "Resultados:",
    ]
    for item in report["items"]:
        path = Path(item["path"])
        if item["status"] == "FAIL":
            lines.append(f"  [FAIL] {path.name}: {item['error']}")
            continue

        video = item["report"].get("video", {})
        codec = video.get("codec") or "desconocido"
        resolution = f"{video.get('width')} × {video.get('height')}"
        alpha = item["report"].get("alpha", {}).get("status", "n/a")
        analysis = item["report"].get("analysis", {})
        analysis_status = analysis.get("status")
        analysis_label = f", GPU {analysis_status}" if report.get("mode") == "gpu" else ""
        lines.append(
            f"  [{item['status']}] {path.name}: {codec}, {resolution}, "
            f"FPS {video.get('average_fps') or 'desconocido'}, alpha {alpha}{analysis_label}"
        )
    return "\n".join(lines)


def write_report(report: dict[str, Any], path: str | Path) -> Path:
    """Guarda el informe JSON, creando sólo la carpeta de salida indicada."""

    report_path = Path(path).expanduser().resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report_path
