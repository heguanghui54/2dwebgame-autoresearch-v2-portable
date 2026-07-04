# Public Benchmark Bootstrap

本文件定义 v2 skill 的 public benchmark 自动配置规则。目标不是伪造官方分数，而是让每个 Web 2D 游戏项目先尽力配置真实 runner，再用 benchmark 反馈驱动迭代。

## 为什么必须 bootstrap

如果没有 public benchmark runner，pipeline 只能做本地复刻检查。这样可以避免假分数，但不能充分支撑自动搜索和自动迭代。

因此每次 run 的 `repo_preflight` 必须先执行 public benchmark bootstrap：

```bash
python <skill_dir>/scripts/bootstrap_public_benchmarks.py \
  --project <project_root> \
  --workspace-root <workspace_root>
```

正式 final selection 前必须用 strict 模式复查：

```bash
python <skill_dir>/scripts/bootstrap_public_benchmarks.py \
  --project <project_root> \
  --workspace-root <workspace_root> \
  --strict
```

## 生成文件

每个项目必须生成：

```text
<project_root>/.game_scientist/benchmarks.json
<project_root>/.game_scientist/benchmark_bootstrap_report.json
```

`benchmarks.json` 写入已发现的 runner、repo、python、checkpoint、wrapper command 和输入协议。

`benchmark_bootstrap_report.json` 写入：

- 搜索过的 workspace roots。
- benchmark root。
- 每个 public runner 的 READY / SKIPPED_NO_SCORE 状态。
- `ready_public_runner_count`。
- `selection_blocked_if_all_public_skipped`。
- 修复建议。

## 自动发现顺序

优先读取环境变量：

- `GAMESCIENTIST_BENCHMARK_ROOT`
- `GAMESCIENTIST_WORKSPACE_ROOT`
- `VBENCH_REPO`
- `VBENCH_PYTHON`
- `VBENCH_COMMAND`
- `T2I_COMPBENCH_REPO`
- `T2I_COMPBENCH_PYTHON`
- `T2I_COMPBENCH_COMMAND`
- `DOVENET_REPO`
- `DOVENET_PYTHON`
- `DOVENET_CHECKPOINT`
- `DOVENET_COMMAND`

然后在 workspace 下自动寻找：

```text
GameScientistBenchmarks/VBench
GameScientistBenchmarks/T2I-CompBench
GameScientistBenchmarks/Image-Harmonization-Dataset-iHarmony4/DoveNet
GameScientistBenchmarks/checkpoints/dovenet/latest_net_G.pth
scripts/run_remote_vbench.py
scripts/run_remote_t2i_clipscore.py
scripts/run_remote_dovenet.py
```

发现 wrapper command 时优先使用 wrapper，因为它可以把本地 Web 项目的截图/视频送到远程 GPU 或已配置环境中执行官方 runner。

## 输入协议

每个 Web 2D 游戏项目必须为 benchmark 准备标准输入：

- VBench：
  - Seedance 背景视频、runtime camera sweep、角色动作预览短视频。
  - 推荐维度：`background_consistency`、`motion_smoothness`、`aesthetic_quality`、`imaging_quality`。
- T2I-CompBench：
  - runtime screenshot、full-scale layer preview、设计 prompt/reference contract。
  - 用于图文一致性、物体逻辑、空间关系、场景角色适配。
- DoveNet / iHarmony：
  - composite runtime image。
  - playfield / midground / foreground mask。
  - 有 same-camera harmonized target 时才产生严格数值分；否则输出诊断图，不伪造分数。
- OpenGame-style 本地复刻：
  - Build Health。
  - Visual Usability。
  - Intent Alignment。
  - Playwright 自动通关。

## 失败处理

- 如果某个 public runner 缺失，记录 `SKIPPED_NO_SCORE` 和具体 skip reason。
- 如果所有 public runners 都是 `SKIPPED_NO_SCORE`，这是 `benchmark_infrastructure_missing`，不能算 final selection 通过。
- 如果 public runner 可用但输入缺失，这是 `benchmark_input_protocol_missing`，回到截图/视频/mask 生成节点。
- 如果 public runner 失败，记录 stdout/stderr tail，并创建 `benchmark_rule` 或 `benchmark_infrastructure` 节点修复。
- 只有在至少一个 public runner READY 且本地 BH/VU/IA hard gates 通过时，节点才可进入最终候选。

## Portable 说明

Portable 包不能自带大型模型权重和所有第三方依赖，但必须自带：

- bootstrap 脚本。
- 配置 schema。
- 输入协议。
- fallback/skip 规则。
- all-skipped 阻断规则。

其他用户安装后，若没有本地 benchmark repo，可以：

1. 设置 `GAMESCIENTIST_BENCHMARK_ROOT` 指向自己的 benchmark 目录。
2. 或安装 VBench、T2I-CompBench、iHarmony/DoveNet 后重新运行 bootstrap。
3. 或配置远程 wrapper command。

在这些完成前，pipeline 可以继续做设计和 prototype，但不能宣称完成自动 benchmark 迭代或一线高质量成品。
