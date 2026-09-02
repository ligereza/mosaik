"""Punto de entrada inicial para el núcleo de MOSAIK."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

from mosaik.diagnose import diagnose_file, text_report
from mosaik.dxv import convert_to_dxv
from mosaik.imago import (
    build_show_session,
    load_session as load_imago_session,
    next_proposal,
    record_event,
    record_result as record_imago_result,
    write_session as write_imago_session,
)
from mosaik.media import MosaikError


def _resolution(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.lower().split("x", 1)
        width, height = int(width_text), int(height_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("La resolución debe tener el formato ANCHOxALTO.") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("La resolución debe ser positiva.")
    return width, height


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mosaik", description="Herramientas MOSAIK para flujo VJ.")
    commands = parser.add_subparsers(dest="command", required=True)

    diagnose = commands.add_parser("diagnose", help="Analiza un archivo de video y genera recomendaciones.")
    diagnose.add_argument("input", help="Archivo de video a analizar.")
    diagnose.add_argument("--report", help="Ruta opcional para guardar el informe JSON.")
    diagnose.add_argument("--target-fps", type=float, help="FPS de la composición o salida objetivo.")
    diagnose.add_argument("--target-resolution", type=_resolution, help="Resolución objetivo, por ejemplo 1920x1080.")
    diagnose.add_argument("--max-samples", type=int, default=300, help="Máximo de muestras de luminancia (default: 300).")
    diagnose.add_argument("--ffmpeg", default="ffmpeg", help="Ruta o nombre de FFmpeg.")
    diagnose.add_argument("--ffprobe", default="ffprobe", help="Ruta o nombre de FFprobe.")

    dxv = commands.add_parser("dxv", help="Convierte y valida un archivo usando el encoder DXV disponible.")
    dxv.add_argument("input", help="Archivo de video de entrada.")
    dxv.add_argument("-o", "--output", help="Archivo .mov de salida.")
    dxv.add_argument("--fps", type=float, help="FPS constante de salida; omitir conserva el timeline de entrada.")
    dxv.add_argument("--resolution", type=_resolution, help="Resolución de salida, por ejemplo 1920x1080.")
    dxv.add_argument("--alpha", action="store_true", help="Solicita formato DXV con alpha si el encoder lo soporta.")
    dxv.add_argument("--overwrite", action="store_true", help="Permite reemplazar la salida existente.")
    dxv.add_argument("--dry-run", action="store_true", help="Muestra la operación sin convertir.")
    dxv.add_argument("--ffmpeg", default="ffmpeg", help="Ruta o nombre de FFmpeg.")
    dxv.add_argument("--ffprobe", default="ffprobe", help="Ruta o nombre de FFprobe.")

    imago = commands.add_parser("imago-session", help="Registra observaciones proposal-only del show.")
    imago_commands = imago.add_subparsers(dest="imago_command", required=True)
    imago_init = imago_commands.add_parser("init", help="Crea una sesion de show.")
    imago_init.add_argument("-o", "--output", required=True)
    imago_init.add_argument("--session-id", default="imago-session")
    imago_init.add_argument("--name", default="IMAGO Show")
    imago_init.add_argument("--created-at")
    imago_event = imago_commands.add_parser("event", help="Registra un evento observado.")
    imago_event.add_argument("session")
    imago_event.add_argument("--event-type", required=True, choices=("show_started", "cue_fired", "incident_detected", "recovery_started", "recovery_verified", "show_closed"))
    imago_event.add_argument("--payload", default="{}")
    imago_event.add_argument("--recorded-at")
    imago_result = imago_commands.add_parser("result", help="Registra un resultado de propuesta.")
    imago_result.add_argument("session")
    imago_result.add_argument("--proposal-id", required=True)
    imago_result.add_argument("--result", required=True, choices=("accepted", "rejected", "review"))
    imago_result.add_argument("--notes", default="")
    imago_result.add_argument("--recorded-at")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "diagnose":
            width = height = None
            if args.target_resolution:
                width, height = args.target_resolution
            report = diagnose_file(
                args.input,
                ffmpeg=args.ffmpeg,
                ffprobe=args.ffprobe,
                target_fps=args.target_fps,
                target_width=width,
                target_height=height,
                max_samples=args.max_samples,
            )
            print(text_report(report))
            if args.report:
                report_path = Path(args.report).expanduser().resolve()
                report_path.parent.mkdir(parents=True, exist_ok=True)
                report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"\nInforme JSON: {report_path}")
            return 0

        if args.command == "dxv":
            width = height = None
            if args.resolution:
                width, height = args.resolution
            result = convert_to_dxv(
                args.input,
                args.output,
                ffmpeg=args.ffmpeg,
                ffprobe=args.ffprobe,
                fps=args.fps,
                width=width,
                height=height,
                alpha=args.alpha,
                overwrite=args.overwrite,
                dry_run=args.dry_run,
            )
            if result.get("dry_run"):
                print("MOSAIK DXV ASSISTANT — dry run")
                print(shlex.join(result["command"]))
            else:
                print("MOSAIK DXV ASSISTANT")
                print(f"Estado: {result['status']}")
                print(f"Entrada: {result['input']}")
                print(f"Salida: {result['output']}")
                print(f"Codec: {result['video'].get('codec')}")
                print(f"Resolución: {result['video'].get('width')} × {result['video'].get('height')}")
                print(f"FPS: {result['video'].get('average_fps')}")
            return 0

        if args.command == "imago-session":
            if args.imago_command == "init":
                session = build_show_session(
                    session_id=args.session_id,
                    name=args.name,
                    created_at=args.created_at,
                )
                output = write_imago_session(session, args.output)
                print(json.dumps({"status": "created", "output": str(output), "next": next_proposal(session)}, ensure_ascii=False, indent=2))
                return 0
            if args.imago_command == "event":
                session = load_imago_session(args.session)
                try:
                    payload = json.loads(args.payload)
                except json.JSONDecodeError as exc:
                    raise MosaikError("--payload must be valid JSON.") from exc
                updated = record_event(session, event_type=args.event_type, payload=payload, recorded_at=args.recorded_at)
                output = write_imago_session(updated, args.session)
                print(json.dumps({"status": "recorded", "output": str(output), "next": next_proposal(updated)}, ensure_ascii=False, indent=2))
                return 0
            if args.imago_command == "result":
                session = load_imago_session(args.session)
                updated = record_imago_result(session, proposal_id=args.proposal_id, result=args.result, notes=args.notes, recorded_at=args.recorded_at)
                output = write_imago_session(updated, args.session)
                print(json.dumps({"status": "recorded", "output": str(output), "next": next_proposal(updated)}, ensure_ascii=False, indent=2))
                return 0
    except MosaikError as exc:
        print(f"MOSAIK ERROR: {exc}", file=sys.stderr)
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
