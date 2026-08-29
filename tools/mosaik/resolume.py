"""Auditor de composiciones Resolume en modo lectura."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from .diagnose import diagnose_file
from .media import MosaikError


def _int_attribute(element: ElementTree.Element | None, name: str) -> int | None:
    if element is None:
        return None
    try:
        return int(element.attrib[name])
    except (KeyError, TypeError, ValueError):
        return None


def _path_key(value: str) -> str:
    return value.replace("/", "\\").casefold()


def _clip_media(clip: ElementTree.Element) -> list[tuple[str, str]]:
    """Devuelve (tipo, ruta) de las fuentes de archivo de un clip."""

    sources: list[tuple[str, str]] = []
    for source in clip.iter("VideoFormatReaderSource"):
        value = source.attrib.get("fileName")
        if value:
            sources.append(("video", value))

    if not sources:
        for video_file in clip.iter("VideoFile"):
            value = video_file.attrib.get("value")
            if value:
                sources.append(("video", value))

    for source in clip.iter("AudioFileSource"):
        value = source.attrib.get("FileName") or source.attrib.get("filename")
        if value:
            sources.append(("audio", value))

    return sources


def _composition_metadata(root: ElementTree.Element) -> dict[str, Any]:
    info = root.find("CompositionInfo")
    version = root.find("versionInfo")
    return {
        "name": (info.attrib.get("name") if info is not None else None) or root.attrib.get("name"),
        "description": info.attrib.get("description") if info is not None else None,
        "width": _int_attribute(info, "width"),
        "height": _int_attribute(info, "height"),
        "version": {
            "product": version.attrib.get("name") if version is not None else None,
            "major": _int_attribute(version, "majorVersion"),
            "minor": _int_attribute(version, "minorVersion"),
            "micro": _int_attribute(version, "microVersion"),
            "revision": _int_attribute(version, "revision"),
        },
        "declared": {
            "decks": _int_attribute(root, "numDecks"),
            "layers": _int_attribute(root, "numLayers"),
            "columns": _int_attribute(root, "numColumns"),
            "current_deck_index": _int_attribute(root, "currentDeckIndex"),
        },
    }


def _extract_media(root: ElementTree.Element) -> tuple[list[dict[str, Any]], int]:
    by_key: dict[str, dict[str, Any]] = {}
    capture_sources = 0
    for clip in root.iter("Clip"):
        layer = _int_attribute(clip, "layerIndex")
        column = _int_attribute(clip, "columnIndex")
        for media_type, raw_path in _clip_media(clip):
            key = _path_key(raw_path)
            item = by_key.setdefault(
                key,
                {
                    "path": raw_path,
                    "media_type": media_type,
                    "occurrences": 0,
                    "locations": [],
                },
            )
            item["occurrences"] += 1
            item["locations"].append({"layer": layer, "column": column})

        for source in clip.iter("VideoSource"):
            if source.attrib.get("type") == "CaptureDeviceVideoSource":
                capture_sources += 1

    return list(by_key.values()), capture_sources


def _action_plan(media: list[dict[str, Any]], capture_sources: int) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for index, item in enumerate(media, start=1):
        diagnosis = item.get("diagnosis") or {}
        if not item["exists"]:
            actions.append(
                {
                    "action_id": f"missing-media-{index:03d}",
                    "risk": "REVIEW",
                    "operation": "relocate_or_restore_media",
                    "target": item["path"],
                    "reason": "La composición referencia un archivo que no está disponible en su ruta guardada.",
                    "requires_confirmation": True,
                    "reversible": True,
                }
            )
            continue

        video = diagnosis.get("video", {})
        if str(video.get("codec") or "").lower() != "dxv":
            actions.append(
                {
                    "action_id": f"prepare-dxv-{index:03d}",
                    "risk": "SAFE",
                    "operation": "create_derived_media",
                    "target": item["path"],
                    "reason": "El host objetivo es Resolume y el medio no está en DXV.",
                    "parameters": {"codec_profile": "resolume-dxv3-normal"},
                    "requires_confirmation": False,
                    "reversible": True,
                }
            )

        if diagnosis.get("overall_status") == "WARN":
            actions.append(
                {
                    "action_id": f"review-media-{index:03d}",
                    "risk": "REVIEW",
                    "operation": "review_media_warnings",
                    "target": item["path"],
                    "reason": "El diagnóstico de media contiene advertencias que pueden afectar la reproducción.",
                    "requires_confirmation": True,
                    "reversible": True,
                }
            )

    if capture_sources:
        actions.append(
            {
                "action_id": "live-inputs-001",
                "risk": "BLOCKED",
                "operation": "offline_media_preparation",
                "target": "capture-devices",
                "reason": "Las entradas de captura no pueden diagnosticarse como archivos ni pre-renderizarse offline.",
                "requires_confirmation": False,
                "reversible": False,
            }
        )
    return actions


def run_resolume_audit(
    composition_path: str | Path,
    *,
    ffmpeg: str = "ffmpeg",
    ffprobe: str = "ffprobe",
    target_fps: float | None = None,
    target_width: int | None = None,
    target_height: int | None = None,
    max_samples: int = 300,
    skip_media: bool = False,
) -> dict[str, Any]:
    """Audita un .avc sin modificarlo ni modificar Resolume."""

    path = Path(composition_path).expanduser().resolve()
    if not path.is_file():
        raise MosaikError(f"No se encontró la composición Resolume: {path}")

    try:
        root = ElementTree.parse(path).getroot()
    except ElementTree.ParseError as exc:
        raise MosaikError(f"La composición no es XML válido: {path}") from exc

    if root.tag != "Composition":
        raise MosaikError(f"El archivo no parece una composición Resolume (.avc): raíz {root.tag!r}")

    media, capture_sources = _extract_media(root)
    statuses: Counter[str] = Counter()
    for item in media:
        item_path = Path(item["path"]).expanduser()
        item["exists"] = item_path.is_file()
        if not item["exists"]:
            item["status"] = "FAIL"
            item["error"] = "Archivo no encontrado en la ruta guardada."
            statuses["FAIL"] += 1
            continue
        if skip_media:
            item["status"] = "NOT_ANALYZED"
            statuses["NOT_ANALYZED"] += 1
            continue

        try:
            diagnosis = diagnose_file(
                item_path,
                ffmpeg=ffmpeg,
                ffprobe=ffprobe,
                target_fps=target_fps,
                target_width=target_width,
                target_height=target_height,
                max_samples=max_samples,
            )
        except MosaikError as exc:
            item["status"] = "FAIL"
            item["error"] = str(exc)
            statuses["FAIL"] += 1
            continue

        item["status"] = diagnosis.get("overall_status", "WARN")
        item["diagnosis"] = diagnosis
        statuses[item["status"]] += 1

    if statuses["FAIL"]:
        overall_status = "FAIL"
    elif statuses["WARN"]:
        overall_status = "WARN"
    elif statuses["NOT_ANALYZED"]:
        overall_status = "WARN"
    else:
        overall_status = "PASS"

    return {
        "schema_version": "0.1",
        "tool": "MOSAIK Resolume Audit",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input": str(path),
        "read_only": True,
        "composition": _composition_metadata(root),
        "statistics": {
            "clips": sum(1 for _ in root.iter("Clip")),
            "media_files": len(media),
            "capture_sources": capture_sources,
            "status_counts": dict(statuses),
        },
        "target": {
            "fps": target_fps,
            "width": target_width,
            "height": target_height,
        },
        "overall_status": overall_status,
        "media": media,
        "action_plan": _action_plan(media, capture_sources),
        "limitations": [
            "El auditor lee el archivo .avc; no observa por sí solo Advanced Output ni el procesador LED.",
            "La ruta guardada puede ser válida sólo en el equipo donde se creó la composición.",
            "El diagnóstico de media no confirma problemas de PWM, cableado, tearing o frecuencia de pantalla.",
        ],
    }


def text_report(report: dict[str, Any]) -> str:
    """Convierte el informe a una salida breve para PowerShell."""

    composition = report["composition"]
    lines = [
        "MOSAIK RESOLUME AUDIT",
        "=====================",
        f"Composición: {report['input']}",
        f"Nombre: {composition.get('name') or 'desconocido'}",
        f"Canvas: {composition.get('width')} × {composition.get('height')}",
        f"Estado: {report['overall_status']}",
        f"Clips: {report['statistics']['clips']}",
        f"Archivos únicos: {report['statistics']['media_files']}",
        f"Capturas: {report['statistics']['capture_sources']}",
        "",
        "Media:",
    ]
    for item in report["media"]:
        detail = item.get("error") or (item.get("diagnosis", {}).get("video", {}).get("codec") if item.get("diagnosis") else "no analizado")
        lines.append(f"  [{item['status']}] {Path(item['path']).name}: {detail} ({item['occurrences']} uso(s))")
    lines.extend(["", "Plan:"])
    for action in report["action_plan"]:
        lines.append(f"  [{action['risk']}] {action['operation']}: {action['target']}")
    return "\n".join(lines)


def write_report(report: dict[str, Any], path: str | Path) -> Path:
    report_path = Path(path).expanduser().resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report_path
