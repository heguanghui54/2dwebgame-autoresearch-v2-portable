#!/usr/bin/env python3
"""Prepare portable public-benchmark input manifests for Web 2D game runs.

This helper does not run VBench, T2I-CompBench, or DoveNet. It packages the
runtime evidence those runners need and records missing inputs explicitly so the
pipeline can create a benchmark_input_protocol node instead of silently
skipping execution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def slugify_prompt(prompt: str, max_len: int = 64) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", prompt.strip().lower()).strip("-")
    if not text:
        text = "web-2d-game-scene"
    digest = hashlib.sha1(prompt.encode("utf-8")).hexdigest()[:8]
    keep = max(8, max_len - len(digest) - 1)
    return f"{text[:keep].strip('-')}-{digest}"


def existing_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value).expanduser().resolve()
    return path if path.exists() else None


def copy_input(src: Path | None, dst_dir: Path, fallback_name: str) -> dict[str, Any]:
    if src is None:
        return {
            "status": "MISSING",
            "source_path": None,
            "packaged_path": None,
            "reason": "input file was not provided or does not exist",
        }
    dst_dir.mkdir(parents=True, exist_ok=True)
    suffix = src.suffix or Path(fallback_name).suffix
    stem = Path(fallback_name).stem
    dst = dst_dir / f"{stem}{suffix}"
    if src.resolve() != dst.resolve():
        shutil.copy2(src, dst)
    return {
        "status": "READY",
        "source_path": str(src),
        "packaged_path": str(dst),
        "bytes": dst.stat().st_size,
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Project root.")
    parser.add_argument("--out", help="Output input package directory.")
    parser.add_argument("--prompt", default="High quality 2.5D side-scrolling Web 2D game scene.")
    parser.add_argument("--runtime-screenshot")
    parser.add_argument("--layer-preview", action="append", default=[])
    parser.add_argument("--runtime-video", action="append", default=[])
    parser.add_argument("--dovenet-composite")
    parser.add_argument("--dovenet-mask")
    parser.add_argument("--dovenet-target")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    out = Path(args.out).expanduser().resolve() if args.out else project / "benchmark/results/public_benchmarks/inputs"
    prompt_slug = slugify_prompt(args.prompt)
    now = datetime.now(timezone.utc).isoformat()

    runtime_screenshot = copy_input(existing_path(args.runtime_screenshot), out / "t2i", f"{prompt_slug}_runtime.png")
    layer_previews = [
        copy_input(existing_path(item), out / "t2i/layer_previews", f"{prompt_slug}_layer_{index:02d}.png")
        for index, item in enumerate(args.layer_preview, start=1)
    ]
    t2i_ready = runtime_screenshot["status"] == "READY" or any(item["status"] == "READY" for item in layer_previews)
    t2i_manifest = {
        "created_at": now,
        "benchmark_source": "T2I-CompBench",
        "prompt": args.prompt,
        "prompt_slug": prompt_slug,
        "runner_filename_rule": "Use prompt_slug for filenames; keep full prompt in JSON only.",
        "runtime_screenshot": runtime_screenshot,
        "layer_previews": layer_previews,
        "status": "READY" if t2i_ready else "MISSING_INPUT",
        "skip_reason": "" if t2i_ready else "missing runtime screenshot and layer previews",
    }
    write_json(out / "t2i/input_manifest.json", t2i_manifest)

    videos = [
        copy_input(existing_path(item), out / "vbench/videos", f"runtime_video_{index:02d}.mp4")
        for index, item in enumerate(args.runtime_video, start=1)
    ]
    vbench_ready = any(item["status"] == "READY" for item in videos)
    vbench_manifest = {
        "created_at": now,
        "benchmark_source": "VBench",
        "videos": videos,
        "status": "READY" if vbench_ready else "MISSING_INPUT",
        "skip_reason": "" if vbench_ready else "missing MP4/WebM video input",
    }
    write_json(out / "vbench/video_manifest.json", vbench_manifest)

    composite = copy_input(existing_path(args.dovenet_composite), out / "dovenet", "composite.png")
    mask = copy_input(existing_path(args.dovenet_mask), out / "dovenet", "mask.png")
    target = copy_input(existing_path(args.dovenet_target), out / "dovenet", "target.png")
    dovenet_ready = composite["status"] == "READY" and mask["status"] == "READY"
    has_strict_target = target["status"] == "READY"
    dovenet_manifest = {
        "created_at": now,
        "benchmark_source": "DoveNet/iHarmony",
        "composite": composite,
        "mask": mask,
        "target": target,
        "status": "READY" if dovenet_ready else "MISSING_INPUT",
        "strict_score_allowed": bool(dovenet_ready and has_strict_target),
        "diagnostic_only": bool(dovenet_ready and not has_strict_target),
        "skip_reason": "" if dovenet_ready else "missing composite image or valid mask",
    }
    write_json(out / "dovenet/input_manifest.json", dovenet_manifest)

    report = {
        "created_at": now,
        "project": str(project),
        "out": str(out),
        "prompt_slug": prompt_slug,
        "inputs": {
            "t2i": t2i_manifest["status"],
            "vbench": vbench_manifest["status"],
            "dovenet": dovenet_manifest["status"],
        },
        "ready_runner_inputs": [
            name
            for name, status in {
                "t2i": t2i_manifest["status"],
                "vbench": vbench_manifest["status"],
                "dovenet": dovenet_manifest["status"],
            }.items()
            if status == "READY"
        ],
        "blocking_failures": [
            f"{name}:{status}"
            for name, status in {
                "t2i": t2i_manifest["status"],
                "vbench": vbench_manifest["status"],
                "dovenet": dovenet_manifest["status"],
            }.items()
            if status != "READY"
        ],
    }
    write_json(out / "public_benchmark_input_pack_report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
