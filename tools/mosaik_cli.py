"""Punto de entrada inicial para el núcleo de MOSAIK."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

from mosaik.diagnose import diagnose_file, text_report
from mosaik.dxv import convert_to_dxv
from mosaik.media import MosaikError
from mosaik.nayade import (
    build_soundcheck_session,
    load_session,
    next_step,
    record_result,
    write_session,
)


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

    nayade = commands.add_parser("nayade-session", help="Planifica y registra un soundcheck NAYADE.")
    nayade_commands = nayade.add_subparsers(dest="nayade_command", required=True)

    nayade_init = nayade_commands.add_parser("init", help="Crea una sesion desde un resumen de mapping JSON.")
    nayade_init.add_argument("source", help="JSON de mapping o tarjeta de prueba.")
    nayade_init.add_argument("-o", "--output", required=True, help="Ruta de salida de la sesion.")
    nayade_init.add_argument("--session-id", default="nayade-session", help="Identificador de la sesion.")
    nayade_init.add_argument("--name", default="NAYADE Soundcheck", help="Nombre de la sesion.")
    nayade_init.add_argument("--seed", type=int, default=0, help="Semilla determinista de la matriz.")

    nayade_record = nayade_commands.add_parser("record", help="Registra el resultado de un paso.")
    nayade_record.add_argument("session", help="Sesion JSON existente.")
    nayade_record.add_argument("--result", required=True, choices=("planned", "running", "approved", "rejected", "review"))
    nayade_record.add_argument("--operation", choices=("baseline", "flip_horizontal", "flip_vertical", "rotate_180", "pattern", "marquee"))
    nayade_record.add_argument("--scope")
    nayade_record.add_argument("--target", action="append", default=[])
    nayade_record.add_argument("--step-id")
    nayade_record.add_argument("--parameters", default="{}", help="Parametros JSON del experimento.")
    nayade_record.add_argument("--notes", default="")
    nayade_record.add_argument("--recorded-at")

    nayade_next = nayade_commands.add_parser("next", help="Muestra el siguiente paso pendiente.")
    nayade_next.add_argument("session", help="Sesion JSON existente.")
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

        if args.command == "nayade-session":
            if args.nayade_command == "init":
                source_path = Path(args.source).expanduser().resolve()
                if not source_path.is_file():
                    raise MosaikError(f"No se encontro el mapping fuente: {source_path}")
                try:
                    source = json.loads(source_path.read_text(encoding="utf-8"))
                except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                    raise MosaikError(f"No se pudo leer el mapping fuente: {source_path}") from exc
                session = build_soundcheck_session(
                    source,
                    session_id=args.session_id,
                    name=args.name,
                    seed=args.seed,
                )
                output = write_session(session, args.output)
                print(json.dumps({"status": "created", "output": str(output), "next": next_step(session)}, ensure_ascii=False, indent=2))
                return 0
            if args.nayade_command == "record":
                session = load_session(args.session)
                try:
                    parameters = json.loads(args.parameters)
                except json.JSONDecodeError as exc:
                    raise MosaikError("--parameters must be valid JSON.") from exc
                updated = record_result(
                    session,
                    result=args.result,
                    operation=args.operation,
                    scope=args.scope,
                    targets=args.target,
                    step_id=args.step_id,
                    parameters=parameters,
                    notes=args.notes,
                    recorded_at=args.recorded_at,
                )
                output = write_session(updated, args.session)
                print(json.dumps({"status": "recorded", "output": str(output), "next": next_step(updated)}, ensure_ascii=False, indent=2))
                return 0
            if args.nayade_command == "next":
                print(json.dumps(next_step(load_session(args.session)), ensure_ascii=False, indent=2))
                return 0
    except MosaikError as exc:
        print(f"MOSAIK ERROR: {exc}", file=sys.stderr)
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
