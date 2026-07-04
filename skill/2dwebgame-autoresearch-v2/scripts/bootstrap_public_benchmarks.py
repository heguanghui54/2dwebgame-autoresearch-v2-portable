#!/usr/bin/env python3
"""Bootstrap public benchmark configuration for a Web 2D game project.

The script is intentionally conservative: it discovers local public benchmark
repos/wrappers and writes a project-local .game_scientist/benchmarks.json.
It never fabricates scores. If no public runner is available in strict mode,
it exits non-zero so the pipeline treats the issue as benchmark infrastructure
work instead of silently finishing without evaluation.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any


def resolve(path: str | Path | None) -> Path | None:
    if not path:
        return None
    return Path(path).expanduser().resolve()


def exists(path: Path | None) -> bool:
    return bool(path and path.exists())


def choose_python() -> str:
    return shutil.which("python3") or shutil.which("python") or "python3"


def candidate_roots(project: Path, explicit: Path | None) -> list[Path]:
    roots: list[Path] = []
    for item in [explicit, resolve(os.environ.get("GAMESCIENTIST_WORKSPACE_ROOT")), project, project.parent, Path.cwd(), Path.cwd().parent]:
        if item and item not in roots:
            roots.append(item)
    return roots


def find_first(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.exists():
            return path.resolve()
    return None


def find_benchmark_root(project: Path, roots: list[Path]) -> Path | None:
    env_root = resolve(os.environ.get("GAMESCIENTIST_BENCHMARK_ROOT"))
    if exists(env_root):
        return env_root
    return find_first([root / "GameScientistBenchmarks" for root in roots])


def find_workspace_script(roots: list[Path], name: str) -> Path | None:
    return find_first([root / "scripts" / name for root in roots])


def ready_item(benchmark_id: str, source: str, ready: bool, config: dict[str, Any], skip_reason: str) -> dict[str, Any]:
    return {
        "benchmark_id": benchmark_id,
        "benchmark_source": source,
        "status": "READY" if ready else "SKIPPED_NO_SCORE",
        "official_runner_available": ready,
        "leaderboard_comparable": False,
        "config": config,
        "skip_reason": "" if ready else skip_reason,
    }


def build_config(project: Path, workspace_root: Path | None) -> tuple[dict[str, Any], dict[str, Any]]:
    roots = candidate_roots(project, workspace_root)
    bench_root = find_benchmark_root(project, roots)
    python = choose_python()

    vbench_wrapper = find_workspace_script(roots, "run_remote_vbench.py")
    t2i_wrapper = find_workspace_script(roots, "run_remote_t2i_clipscore.py")
    dovenet_wrapper = find_workspace_script(roots, "run_remote_dovenet.py")

    vbench_repo = resolve(os.environ.get("VBENCH_REPO")) or (bench_root / "VBench" if bench_root else None)
    t2i_repo = resolve(os.environ.get("T2I_COMPBENCH_REPO")) or (bench_root / "T2I-CompBench" if bench_root else None)
    dovenet_repo = resolve(os.environ.get("DOVENET_REPO")) or (
        bench_root / "Image-Harmonization-Dataset-iHarmony4" / "DoveNet" if bench_root else None
    )
    dovenet_checkpoint = resolve(os.environ.get("DOVENET_CHECKPOINT")) or (
        bench_root / "checkpoints" / "dovenet" / "latest_net_G.pth" if bench_root else None
    )

    config: dict[str, Any] = {
        "schema_version": "2dwebgame-benchmark-config-v1",
        "policy": "configure public runners first; missing public runners are benchmark_infrastructure_missing, not content pass",
        "input_protocol": {
            "runtime_screenshots": "screenshots/runtime_start.png, runtime_mid.png, runtime_victory.png",
            "runtime_video": "5-10 second camera sweep or gameplay clip for VBench when available",
            "layer_previews": "full_scale_layer_previews/far.png, far_mid.png, full_scene.png",
            "dovenet_inputs": "composite runtime image plus valid playfield/foreground mask; score only with same-camera target",
            "t2i_inputs": "runtime screenshot plus design prompt/reference contract",
        },
    }

    if exists(vbench_wrapper):
        config["vbench"] = {
            "command": str(vbench_wrapper),
            "dimensions": ["background_consistency", "motion_smoothness", "aesthetic_quality", "imaging_quality"],
            "input_protocol": "Run on runtime videos, Seedance background clips, or generated animation previews.",
        }
    elif exists(vbench_repo / "evaluate.py" if vbench_repo else None):
        config["vbench"] = {
            "repo": str(vbench_repo),
            "python": python,
            "dimensions": ["background_consistency", "motion_smoothness", "aesthetic_quality", "imaging_quality"],
            "input_protocol": "Run official evaluate.py in custom_input mode on video clips.",
        }

    if exists(t2i_wrapper):
        config["t2i_compbench"] = {
            "repo": str(t2i_repo) if exists(t2i_repo) else "",
            "python": python,
            "command": str(t2i_wrapper),
            "input_protocol": "Run CLIPScore/T2I alignment on runtime screenshots and full-scale layer previews.",
        }
    elif exists(t2i_repo):
        config["t2i_compbench"] = {
            "repo": str(t2i_repo),
            "python": python,
            "input_protocol": "Use official BLIP-VQA/CLIPScore/UniDet scripts when dependencies are installed.",
        }

    if exists(dovenet_wrapper):
        config["dovenet_iharmony"] = {
            "repo": str(dovenet_repo) if exists(dovenet_repo) else "",
            "python": python,
            "checkpoint": str(dovenet_checkpoint) if exists(dovenet_checkpoint) else "",
            "command": str(dovenet_wrapper),
            "fmse_max": 450,
            "input_protocol": "Run on a composite screenshot plus playfield/midground mask; score only when valid target evidence exists.",
        }
    elif exists(dovenet_repo / "test.py" if dovenet_repo else None):
        config["dovenet_iharmony"] = {
            "repo": str(dovenet_repo),
            "python": python,
            "checkpoint": str(dovenet_checkpoint) if exists(dovenet_checkpoint) else "",
            "fmse_max": 450,
            "input_protocol": "Run official DoveNet with checkpoint, composite image, mask, and optional harmonized target.",
        }

    doctor_items: list[dict[str, Any]] = []
    doctor_items.append(
        ready_item(
            "vbench",
            "VBench",
            "vbench" in config,
            config.get("vbench", {}),
            "VBench repo/evaluate.py or run_remote_vbench.py was not found.",
        )
    )
    doctor_items.append(
        ready_item(
            "t2i_compbench",
            "T2I-CompBench",
            "t2i_compbench" in config,
            config.get("t2i_compbench", {}),
            "T2I-CompBench repo or run_remote_t2i_clipscore.py was not found.",
        )
    )
    doctor_items.append(
        ready_item(
            "dovenet_iharmony",
            "DoveNet / iHarmony4",
            "dovenet_iharmony" in config and bool(config.get("dovenet_iharmony", {}).get("checkpoint") or config.get("dovenet_iharmony", {}).get("command")),
            config.get("dovenet_iharmony", {}),
            "DoveNet repo/wrapper or checkpoint was not found.",
        )
    )

    ready_count = len([item for item in doctor_items if item["status"] == "READY"])
    doctor = {
        "schema_version": "2dwebgame-benchmark-bootstrap-report-v1",
        "project": str(project),
        "workspace_roots_checked": [str(root) for root in roots],
        "benchmark_root": str(bench_root) if bench_root else "",
        "config_path": str(project / ".game_scientist" / "benchmarks.json"),
        "ready_public_runner_count": ready_count,
        "selection_blocked_if_all_public_skipped": ready_count == 0,
        "benchmarks": doctor_items,
        "next_actions_if_blocked": [
            "Set GAMESCIENTIST_BENCHMARK_ROOT to a folder containing VBench, T2I-CompBench, and iHarmony/DoveNet.",
            "Or install wrapper scripts run_remote_vbench.py, run_remote_t2i_clipscore.py, and run_remote_dovenet.py under a workspace scripts/ folder.",
            "Then rerun this bootstrap script before asset/runtime iteration.",
        ],
    }
    return config, doctor


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".", help="Project root that will receive .game_scientist/benchmarks.json")
    parser.add_argument("--workspace-root", default="", help="Optional workspace root to search for benchmark repos and wrappers")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when no public runner is ready")
    args = parser.parse_args(argv)

    project = Path(args.project).expanduser().resolve()
    project.mkdir(parents=True, exist_ok=True)
    workspace_root = resolve(args.workspace_root)
    config, doctor = build_config(project, workspace_root)

    config_dir = project / ".game_scientist"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "benchmarks.json"
    doctor_path = config_dir / "benchmark_bootstrap_report.json"
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    doctor_path.write_text(json.dumps(doctor, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({"config": str(config_path), "doctor": str(doctor_path), "ready_public_runner_count": doctor["ready_public_runner_count"]}, indent=2))
    if args.strict and doctor["ready_public_runner_count"] == 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
