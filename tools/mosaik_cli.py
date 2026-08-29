"""Punto de entrada inicial para el núcleo de MOSAIK."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

from mosaik.diagnose import diagnose_file, text_report
from mosaik.dxv import convert_to_dxv
from mosaik.instar import run_instar, text_report as instar_text_report, write_report
from mosaik.media import MosaikError
from mosaik.resolume import run_resolume_audit, text_report as resolume_text_report, write_report as write_resolume_report


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

    instar = commands.add_parser("instar", help="Ejecuta el preflight de media de una carpeta.")
    instar.add_argument("media_root", help="Carpeta raíz con los videos del show.")
    instar.add_argument("--report", help="Ruta opcional para guardar el informe JSON.")
    instar.add_argument("--target-fps", type=float, help="FPS de la composición o salida objetivo.")
    instar.add_argument("--target-resolution", type=_resolution, help="Resolución objetivo, por ejemplo 1920x1080.")
    instar.add_argument("--target-codec", help="Codec objetivo opcional, por ejemplo dxv.")
    instar.add_argument("--deep", action="store_true", help="Además del preflight, ejecuta el diagnóstico visual/luminancia.")
    instar.add_argument("--gpu", action="store_true", help="Analiza frames con NVDEC/CUDA; no hace fallback silencioso a CPU.")
    instar.add_argument("--gpu-max-frames", type=int, default=900, help="Máximo de frames para el análisis GPU por archivo.")
    instar.add_argument("--gpu-batch-size", type=int, default=16, help="Cantidad de frames por lote en el decoder GPU.")
    instar.add_argument("--max-samples", type=int, default=300, help="Máximo de muestras de luminancia en modo --deep.")
    instar.add_argument("--sidecars-dir", help="Carpeta opcional para escribir un .mosaik.json por visual.")
    instar.add_argument("--ffmpeg", default="ffmpeg", help="Ruta o nombre de FFmpeg.")
    instar.add_argument("--ffprobe", default="ffprobe", help="Ruta o nombre de FFprobe.")

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

    resolume = commands.add_parser(
        "resolume-audit",
        help="Audita una composición .avc en modo lectura y genera un plan de optimización.",
    )
    resolume.add_argument("composition", help="Archivo .avc de Resolume.")
    resolume.add_argument("--report", help="Ruta opcional para guardar el informe JSON.")
    resolume.add_argument("--target-fps", type=float, help="FPS de la composición o salida objetivo.")
    resolume.add_argument("--target-resolution", type=_resolution, help="Resolución objetivo, por ejemplo 1920x1080.")
    resolume.add_argument("--max-samples", type=int, default=300, help="Máximo de muestras de luminancia por archivo.")
    resolume.add_argument("--skip-media", action="store_true", help="Lee la composición sin ejecutar FFprobe sobre los medios.")
    resolume.add_argument("--ffmpeg", default="ffmpeg", help="Ruta o nombre de FFmpeg.")
    resolume.add_argument("--ffprobe", default="ffprobe", help="Ruta o nombre de FFprobe.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "instar":
            width = height = None
            if args.target_resolution:
                width, height = args.target_resolution
            report = run_instar(
                args.media_root,
                ffmpeg=args.ffmpeg,
                ffprobe=args.ffprobe,
                target_fps=args.target_fps,
                target_width=width,
                target_height=height,
                max_samples=args.max_samples,
                target_codec=args.target_codec,
                deep=args.deep,
                sidecars_dir=args.sidecars_dir,
                gpu=args.gpu,
                gpu_max_frames=args.gpu_max_frames,
                gpu_batch_size=args.gpu_batch_size,
            )
            print(instar_text_report(report))
            if args.report:
                report_path = write_report(report, args.report)
                print(f"\nInforme JSON: {report_path}")
            return 1 if report["overall_status"] == "FAIL" else 0

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

        if args.command == "resolume-audit":
            width = height = None
            if args.target_resolution:
                width, height = args.target_resolution
            report = run_resolume_audit(
                args.composition,
                ffmpeg=args.ffmpeg,
                ffprobe=args.ffprobe,
                target_fps=args.target_fps,
                target_width=width,
                target_height=height,
                max_samples=args.max_samples,
                skip_media=args.skip_media,
            )
            print(resolume_text_report(report))
            if args.report:
                report_path = write_resolume_report(report, args.report)
                print(f"\nInforme JSON: {report_path}")
            return 1 if report["overall_status"] == "FAIL" else 0
    except MosaikError as exc:
        print(f"MOSAIK ERROR: {exc}", file=sys.stderr)
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
