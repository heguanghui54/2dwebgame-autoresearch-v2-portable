# 2DWebGame AutoResearch v2 Portable

这是 `2dwebgame-autoresearch-v2` 的可迁移发布包。它把 Web 2D 游戏自动生成 skill、安装脚本、依赖检查脚本和一个最小 Phaser/Vite 模板放在同一个仓库里，目标是让另一台机器或其他用户可以安装后复用这套流程。

## 能做什么

- 从角色描述、环境描述、游戏创意或一张/多张参考图开始。
- 先生成完整游戏设计方案，再用 critic 和 benchmark 反馈迭代。
- 面向 Phaser/Vite Web 2D 横版游戏，不默认进入 Unity。
- 正式高质量游戏必须使用真实图像资产：地图/平台/中景默认走 `generate2dmap` 或等价图像生成流程，角色/敌人/Boss/FX 默认走 `generate2dsprite` 或等价 sprite 生成流程。
- 程序化 SVG、Canvas、CSS、Phaser Graphics、几何形状、噪声图和 debug rectangle 只能用于 layout/debug/prototype，不能作为最终美术通过 benchmark。
- 支持背景、中景、gameplay 层级契约，避免中景变成半透明背景或模糊贴图。
- 支持真实 Seedance 动态背景流程；没有真实 task id 和下载文件时不会伪造动态，直接退回静态背景。
- 支持本地 OpenGame-style BH/VU/IA 检查，以及 progressive full-scale layer benchmarking。
- 公共 benchmark 缺失时记录 `SKIPPED_NO_SCORE`，不伪造官方分数。

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

缺失可选能力时，skill 仍可执行设计、规划、脚本生成和本地复刻检查；对应外部 benchmark 或视频生成会记录为 `SKIPPED_NO_SCORE` 或 disabled，不会伪造结果。

但如果缺少 `generate2dmap`、`generate2dsprite`、内置/外部图像生成能力或 approved high-resolution assets，pipeline 只能交付设计方案、技术脚手架或明确标注的 playable prototype。`visual_asset_source_gate` 必须阻止它被报告为“一线高精度成品”。

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
│       └── references/
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
