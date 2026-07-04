# 2DWebGame AutoResearch v2 Portable

这是 `2dwebgame-autoresearch-v2` 的可迁移发布包。它把 Web 2D 游戏自动生成 skill、安装脚本、依赖检查脚本和一个最小 Phaser/Vite 模板放在同一个仓库里，目标是让另一台机器或其他用户可以安装后复用这套流程。

## 能做什么

- 从角色描述、环境描述、游戏创意或一张/多张参考图开始。
- 先生成完整游戏设计方案，再用 critic 和 benchmark 反馈迭代。
- 面向 Phaser/Vite Web 2D 横版游戏，不默认进入 Unity。
- 正式高质量游戏必须使用真实图像资产：地图/平台/中景默认走内置或外部 `generate2dmap` 子功能，角色/敌人/Boss/FX 默认走内置或外部 `generate2dsprite` 子功能。
- portable 包已内化 `generate2dmap` / `generate2dsprite` 的核心 skill 文件、references 和处理脚本；外部 peer skill 可用时优先调用，不可用时使用内置副本。
- 程序化 SVG、Canvas、CSS、Phaser Graphics、几何形状、噪声图和 debug rectangle 只能用于 layout/debug/prototype，不能作为最终美术通过 benchmark。
- 支持背景、中景、gameplay 层级契约，避免中景变成半透明背景或模糊贴图。
- 支持真实 Seedance 动态背景流程；没有真实 task id 和下载文件时不会伪造动态，直接退回静态背景。
- 支持本地 OpenGame-style BH/VU/IA 检查，以及 progressive full-scale layer benchmarking。
- 先自动配置 public benchmark runner，再进入正式自动迭代。公共 benchmark 缺失时记录 `SKIPPED_NO_SCORE`，不伪造官方分数；如果全部 skipped，不能宣称 final high-quality success。

## 安装

```bash
git clone https://github.com/heguanghui54/2dwebgame-autoresearch-v2-portable.git
cd 2dwebgame-autoresearch-v2-portable
bash scripts/doctor.sh
bash scripts/install.sh
```

安装后在 Codex 中调用：

```text
$2dwebgame-autoresearch-v2
根据这些参考图和游戏想法，自动设计、生成、benchmark、迭代并交付一个 Phaser/Vite Web 2D 横版游戏。
```

默认安装位置是：

```text
~/.codex/skills/2dwebgame-autoresearch-v2
```

可以用环境变量覆盖：

```bash
CODEX_SKILLS_DIR=/custom/codex/skills bash scripts/install.sh
```

## 依赖层级

最低可用依赖：

- Codex 支持本地 skills。
- `bash`
- `git`
- `node`
- `npm`
- `python3`

推荐依赖：

- `ffmpeg` / `ffprobe`
- `rg`
- `gh`
- Playwright browser runtime

可选能力：

- `generate2dmap`
- `generate2dsprite`
- `game-studio:phaser-2d-game`
- `game-studio:game-playtest`
- `volcengine:volcengine`
- `chrome:control-chrome`
- T2I-CompBench、GenEval、DoveNet/iHarmony、VBench、GameCraft、VideoGameQA

缺失外部 `generate2dmap` / `generate2dsprite` 时，skill 会使用包内的内置副本继续执行地图和角色子功能。缺失外部视频生成服务时，动态背景降级为静态背景。缺失 public benchmark 环境时，会先尝试自动配置，仍无法配置时记录为 `benchmark_infrastructure_missing` / `SKIPPED_NO_SCORE`，不会伪造结果。

但如果缺少内置/外部图像生成能力或 approved high-resolution assets，pipeline 只能交付设计方案、技术脚手架或明确标注的 playable prototype。`visual_asset_source_gate` 必须阻止它被报告为“一线高精度成品”。

## Public Benchmark 环境配置

skill 会在每个项目启动时自动运行：

```bash
python ~/.codex/skills/2dwebgame-autoresearch-v2/scripts/bootstrap_public_benchmarks.py \
  --project <your-game-project> \
  --workspace-root <your-workspace>
```

正式交付前会用 strict 模式复查：

```bash
python ~/.codex/skills/2dwebgame-autoresearch-v2/scripts/bootstrap_public_benchmarks.py \
  --project <your-game-project> \
  --workspace-root <your-workspace> \
  --strict
```

它会在项目内生成：

```text
<your-game-project>/.game_scientist/benchmarks.json
<your-game-project>/.game_scientist/benchmark_bootstrap_report.json
```

自动发现的推荐目录结构：

```text
<your-workspace>/
├── GameScientistBenchmarks/
│   ├── VBench/
│   ├── T2I-CompBench/
│   ├── Image-Harmonization-Dataset-iHarmony4/
│   │   └── DoveNet/
│   └── checkpoints/
│       └── dovenet/
│           └── latest_net_G.pth
└── scripts/
    ├── run_remote_vbench.py
    ├── run_remote_t2i_clipscore.py
    └── run_remote_dovenet.py
```

也可以用环境变量显式配置：

```bash
export GAMESCIENTIST_BENCHMARK_ROOT="/path/to/GameScientistBenchmarks"
export VBENCH_REPO="/path/to/VBench"
export VBENCH_PYTHON="python3"
export VBENCH_COMMAND="/path/to/run_remote_vbench.py"
export T2I_COMPBENCH_REPO="/path/to/T2I-CompBench"
export T2I_COMPBENCH_PYTHON="python3"
export T2I_COMPBENCH_COMMAND="/path/to/run_remote_t2i_clipscore.py"
export DOVENET_REPO="/path/to/Image-Harmonization-Dataset-iHarmony4/DoveNet"
export DOVENET_PYTHON="python3"
export DOVENET_CHECKPOINT="/path/to/latest_net_G.pth"
export DOVENET_COMMAND="/path/to/run_remote_dovenet.py"
```

Benchmark 输入协议：

- VBench：Seedance 背景视频、runtime camera sweep、角色动作预览短视频。
- T2I-CompBench：runtime screenshot、full-scale layer preview、设计 prompt/reference contract。
- DoveNet/iHarmony：composite runtime image、playfield/midground/foreground mask、可选 same-camera target。
- 本地 OpenGame-style：Playwright 截图、route trace、controls trace、console/request logs。

如果 `benchmark_bootstrap_report.json` 中 `ready_public_runner_count` 为 0，pipeline 可以继续做设计或 prototype，但不能宣称完成了 public benchmark 自动迭代，也不能作为 final high-quality game 交付。

## 真实资产 Gate

正式节点进入 Phaser runtime 前，必须为每个最终可见资产记录：

- `asset_id`
- `asset_role`
- `asset_source`
- `source_prompt_or_reference`
- `raw_asset_path`
- `processed_asset_path`
- `qc_report_path`
- `used_in_runtime_screenshot`

允许的正式来源包括 `generate2dmap`、`generate2dsprite`、`image_gen`、`user_highres_asset`、`approved_existing_asset` 和真实 `seedance_video`。

`procedural_debug` 只允许出现在 debug overlay、collision preview、layout sketch 或 prototype 中。只要它进入 final selected visual stack，benchmark 必须 hard-fail，并生成 `procedural_placeholder_art_used` 或 `visual_asset_source_missing`。

## 视频生成服务策略

Volcengine / Seedance / 其他视频生成服务都是可选增强，不是硬依赖。

- 用户愿意开通、登录并授权火山引擎时，pipeline 可以调用 Seedance 生成 4K、约 5 秒、无缝循环的动态背景。
- 用户没有开通视频生成服务、当前机器无法调用、额度不足、登录失败或下载失败时，不阻塞游戏制作。
- 没有真实视频生成结果时，pipeline 必须使用静态背景继续完成游戏。
- 静态背景仍然需要通过尺寸、视差、画面融洽度、playfield fit 和 runtime screenshot 检查。
- 不允许用本地假动效、伪 task id、伪 provenance 冒充 Seedance 或其他视频生成服务。

## 目录结构

```text
2dwebgame-autoresearch-v2-portable/
├── skill/
│   └── 2dwebgame-autoresearch-v2/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
│       │   └── embedded/
│       └── scripts/
├── scripts/
│   ├── doctor.sh
│   ├── install.sh
│   └── package.sh
├── templates/
│   └── phaser-vite/
├── PORTABLE_MANIFEST.json
├── README.md
└── LICENSE
```

## 打包

```bash
bash scripts/package.sh
```

输出：

```text
dist/2dwebgame-autoresearch-v2-portable-<date>.tar.gz
dist/2dwebgame-autoresearch-v2-portable-<date>.tar.gz.sha256
```

## GitHub 发布

如果本机已经登录 GitHub CLI：

```bash
gh auth status
gh repo create 2dwebgame-autoresearch-v2-portable --public --source . --remote origin --push
```

如果已经有远程仓库：

```bash
git remote add origin git@github.com:<owner>/2dwebgame-autoresearch-v2-portable.git
git push -u origin main
```

## 验收标准

发布包至少应满足：

- `bash scripts/doctor.sh` 能给出清晰依赖状态。
- `bash scripts/install.sh` 能把 skill 安装到 Codex skills 目录。
- `skill/2dwebgame-autoresearch-v2/SKILL.md` 的 frontmatter 名称与目录一致。
- 包内没有本机绝对路径。
- 缺少外部生成或公共 benchmark 时，流程必须降级为记录 `SKIPPED_NO_SCORE`，不能伪造分数或动态视频。
- `visual_asset_source_gate` 能阻止程序化占位美术、黑图、纯色块、噪声墙、SVG 几何图和低精度放大图进入最终交付。
