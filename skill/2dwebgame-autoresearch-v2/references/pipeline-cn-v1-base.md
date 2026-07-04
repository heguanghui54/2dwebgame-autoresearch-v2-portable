# 2DWebGame AutoResearch v1 中文 Pipeline

本文件是执行版流程。目标是让用户给一句角色/环境描述或角色、背景参考图后，自动完成“设计方案 -> 设计评审 -> 资产生成 -> Web 2D 游戏集成 -> benchmark -> 截图/视频评估 -> 迭代修复 -> 交付”的闭环。

## 0. 总原则

- 先设计，后生成。任何地图、角色、Seedance、Phaser 代码之前，必须先通过 `game_design_plan` 和 critic gate。
- 先配置 public benchmark，再进入正式自动迭代。每个项目都必须生成 `.game_scientist/benchmarks.json` 和 `.game_scientist/benchmark_bootstrap_report.json`。
- 先执行 public benchmark，再宣称 public benchmark 参与迭代。Runner READY 只是环境可用，不是评估完成；必须准备输入包、运行 READY runner、记录结果或失败。
- 先生成真实图像资产，再做正式 runtime。外部或内置 `generate2dmap` / `generate2dsprite` 是高质量地图、平台、角色、敌人、Boss、FX 的默认入口。
- 先验证，再宣称成功。构建、截图、玩法、视觉、用户反馈都要有证据。
- 不追求一次命中。像 AI Scientist v2 一样，把候选设计和每轮修改当作节点，记录失败原因，选择最强节点继续。
- 不伪造外部资产。Seedance 没有真实调用或没有真实下载结果，就不能把本地合成物冒充动态背景。
- 不把 benchmark 当遮羞布。benchmark 要捕捉真实观感问题，不能为了过关放宽错误规则。
- 不把程序化占位图当最终美术。Canvas/SVG/HTML/CSS/Phaser Graphics/几何形状/脚本绘图只允许做 layout、debug、collision preview 或 prototype，不得作为“高精度成品”通过。

## 1. 输入与运行目录

用户可以提供：

- 角色描述。
- 场景/环境描述。
- 游戏创意。
- 一张或多张角色/背景/氛围参考图。

每次运行创建目录：

```text
public/assets/web-pipeline/<run-slug>/
  references/
  design/
  generated/
  runtime/
  screenshots/
  benchmarks/
  provenance/
```

必须复制参考图，不直接依赖临时剪贴板路径。

## 1.5 Public Benchmark Bootstrap 节点

每次 run 在参考图分析和设计之前，必须先配置 benchmark runner：

```bash
python <skill_dir>/scripts/bootstrap_public_benchmarks.py \
  --project <project_root> \
  --workspace-root <workspace_root>
```

正式 final selection 前必须 strict 复查：

```bash
python <skill_dir>/scripts/bootstrap_public_benchmarks.py \
  --project <project_root> \
  --workspace-root <workspace_root> \
  --strict
```

必须输出：

```text
<project_root>/.game_scientist/benchmarks.json
<project_root>/.game_scientist/benchmark_bootstrap_report.json
```

`ready_public_runner_count == 0` 时：

- 记录 `benchmark_infrastructure_missing`。
- 不能把本轮标为 final high-quality success。
- 可以继续生成设计、资产或 prototype，但最终交付必须写明 public benchmark 阻断。
- 下一轮搜索优先扩展 `benchmark_infrastructure` 节点，配置 VBench / T2I-CompBench / DoveNet runner 或 wrapper。

## 1.6 Public Benchmark 输入包与执行节点

当至少一个 public runner READY 后，必须在最终候选进入 handoff 前准备输入包：

```bash
python <skill_dir>/scripts/prepare_public_benchmark_inputs.py \
  --project <project_root> \
  --prompt "<short scene prompt>" \
  --runtime-screenshot <runtime_start.png> \
  --layer-preview <full_scene.png> \
  --runtime-video <camera_sweep.mp4> \
  --dovenet-composite <runtime_full.png> \
  --dovenet-mask <mask.png>
```

标准输出：

```text
benchmark/results/public_benchmarks/inputs/t2i/input_manifest.json
benchmark/results/public_benchmarks/inputs/vbench/video_manifest.json
benchmark/results/public_benchmarks/inputs/dovenet/input_manifest.json
benchmark/results/public_benchmarks/inputs/public_benchmark_input_pack_report.json
benchmark/results/public_benchmarks/public_benchmark_execution_report.json
```

执行规则：

- T2I prompt 文件名只能用短 slug，完整 prompt 写 JSON，防止长 prompt 文件名失败。
- VBench 必须有真实 MP4/WebM。没有 Seedance 视频时录制 runtime camera sweep；没有视频不能写 VBench 分数。
- DoveNet/iHarmony 必须有 composite + mask；没有 same-camera target 时只做 diagnostic/advisory，不写严格官方分数。
- READY runner + 输入存在时必须执行；`PENDING_NOT_EXECUTED` 不能进入 final high-quality handoff。
- 自定义游戏截图/视频默认 `leaderboard_comparable: false`，除非完全使用官方数据集、官方 prompt suite、官方协议和官方入口。
- 失败要记录命令、退出码、stdout/stderr tail，并作为 `public_benchmark_execution` 或 `benchmark_input_protocol` 节点继续迭代。

## 2. 参考图分析节点

输出：

- `references/reference_art_analysis.json`
- `references/reference_prompt_contract.md`
- `references/reference_contact_sheet.png`

分析：

- 主色、强调色、禁用色。
- 构图、空间深度、可读焦点。
- 背景是否完整，是否适合做两屏宽动态远景。
- 可选中景应出现什么具体物体。
- 可动线索：光束、雾、雨丝、水、粒子、灯光、水晶辉光。
- 禁止项：角色、UI、平台、碰撞物不能烤进纯背景。

展示给用户或保存证据时，至少要有参考图 contact sheet。

## 3. 游戏设计候选节点

如果用户没有给明确游戏创意，生成 3 个候选创意；如果用户给了创意，把它作为主方向，但仍补全设计。

每个候选必须写：

- 核心幻想。
- 玩家 30-90 秒循环。
- 角色动作与能力。
- 地图流程。
- 能力门和胜利条件。
- 敌人/陷阱/精英或 Boss。
- 背景、中景、gameplay 层级规则。
- 相机、视差、攻击推近镜头规则。
- 资产清单。
- 真实图像资产来源计划：哪些走 `generate2dmap`，哪些走 `generate2dsprite`，哪些走 Seedance，哪些使用用户高精度资产或 approved existing asset。
- benchmark 清单。
- public benchmark 输入包与执行计划：哪些截图、视频、mask、prompt 会给哪个 runner，哪些 runner 必须实际执行。
- 风险。

输出：

- `design/game_design_candidates.json`
- `design/game_design_plan.md`
- `design/game_design_plan.json`

## 4. 设计 Critic Gate

调用独立 subagent 或隔离 critic pass。critic 只评审设计，不生成资产、不改代码。

评分项：

- 用户意图一致性。
- 核心幻想清晰度。
- 玩法闭环。
- 关卡流程。
- 能力/敌人设计。
- 视觉识别度。
- 资产可行性。
- 相机/视差可行性。
- benchmark 可验证性。
- 生产风险。

最多 3 轮。通过条件：

- 平均分 >= 8。
- 单项 >= 7。
- 无 hard-fail。
- benchmark 都可执行。
- public benchmark 不能停在 bootstrap；输入包和执行计划可执行。

输出：

- `design/design_critic_round_1.md`
- `design/design_critic_round_2.md`
- `design/design_critic_round_3.md`
- `design/design_decision_log.md`

hard-fail 示例：

- 没有可通关流程。
- 终局门不能验证在世界最右端。
- 中景只是半透明背景或灰度通道图。
- Seedance 要求无法追溯 provenance。
- 角色动作没有脚底基准和动作连续性规则。
- 用户反馈无法转成截图或 benchmark。
- critic 或审核建议无法转成搜索节点。
- public runner READY 但没有输入包或执行计划。
- 背景、平台、中景、角色、敌人、Boss 或 FX 计划使用程序化图形作为最终高精度资产。
- 没有真实图像生成或 approved asset provenance，却宣称能达到高质量成品。

## 4.5 真实图像资产来源 Gate

这是正式制作的硬门槛。它必须在地图/角色资产进入 Phaser runtime 之前运行。

每个 final visible asset 必须在 `asset_manifest.json` 中声明：

```json
{
  "asset_id": "hero_run",
  "asset_role": "hero",
  "asset_source": "generate2dsprite",
  "source_prompt_or_reference": "...",
  "raw_asset_path": "...",
  "processed_asset_path": "...",
  "qc_report_path": "...",
  "used_in_runtime_screenshot": false
}
```

允许的正式来源：

- `generate2dmap`
- `generate2dsprite`
- `image_gen`
- `user_highres_asset`
- `approved_existing_asset`
- `seedance_video`

`procedural_debug` 只能用于 debug overlay、collision guide、layout sketch 或 playable prototype。只要它出现在 final selected visual stack 中，节点必须 hard-fail。

角色和地图的默认约束：

- 背景、中景、平台、门、机关、拾取物、危害物：默认使用 `generate2dmap side_scroll_mode` 或等价图像生成流程。
- 主角、敌人、Boss、projectile、impact、slash、dash、parry FX：默认使用 `generate2dsprite hero_action_bundle` 或等价 sprite 生成流程。

benchmark 必须检查：

- source/provenance/QC 路径存在。
- layer preview 和 runtime screenshot 中真正使用了该资产。
- 资产不是黑图、纯色块、噪声墙、几何图、低精度放大图或 Phaser Graphics 形状。
- 如果 benchmark 曾让上述错误通过，记录 `benchmark_false_positive_placeholder_pass`，先修 benchmark，再继续制作。

## 5. 地图与层级资产节点

默认层级：

```text
动态/静态完整背景 -> 可选 alpha 中景物体 -> gameplay 平台/角色/敌人/FX/HUD
```

不要把背景拆成多层模糊图。背景是一张完整远景；中景是在背景和 gameplay 之间增加的具体物体，不是第二张满屏背景。

地图资产必须优先调用外部 `generate2dmap side_scroll_mode`。如果外部 skill 不存在，必须读取并执行 v2 内置副本：

```text
references/embedded/generate2dmap-SKILL.md
```

该内置副本是完整 `generate2dmap` 子功能，不是简化契约。不能用脚本画几何背景、噪声背景、SVG 平台、矩形门、圆形拾取物来冒充最终美术。

中景规则：

- 必须是真 alpha 抠像。
- 必须是具体物体，如岩石、树根、藤蔓、塔、灯、废墟。
- 空洞显示背景，不靠整体透明度。
- 颜色与背景协调，但色度/亮度可略高于背景，黑白对比低于前景。
- 底部物体要接到画面底部，不能悬浮。
- 边缘虚实结合：岩石/建筑硬，雾边/光晕/细藤软。
- 不要灰成通道图，不要紫边污染。

每个资产节点都要产出可查看图片：

- 背景静帧。
- Seedance 视频首帧/中帧/尾帧。
- 中景 alpha 预览和棋盘格预览。
- 平台/机关/门/拾取物 atlas。
- 角色动作 sprite sheet 或 contact sheet。
- 集成后的关键截图。
- provenance/QC JSON，说明资产来自 `generate2dmap`、`generate2dsprite`、image generation、用户高精度资产或 approved existing asset。

## 6. Seedance 动态背景节点

Volcengine/Seedance 或其他视频生成服务只作为可选增强。只有用户愿意开通、登录并授权外部生成时才调用。

如果用户没有视频生成服务、当前机器无法调用、额度不足、登录失败或下载失败，跳过本节点，使用静态完整背景继续制作游戏。静态背景仍然要经过尺寸、视差、playfield fit、画面融洽度和 runtime screenshot 检查。

调用方式：

- 使用 `volcengine:volcengine` 能力或 `chrome:control-chrome` 打开火山引擎页面。
- 使用参考图或重新生成的长背景图作为 image-to-video 输入。
- prompt 必须写清楚 4K、约 5 秒、无缝循环、两屏宽、略高于视口、无角色/UI/平台/黑边/模糊条。
- prompt 必须要求上中下都有动态：光束呼吸、雾带滚动、水晶/灯光脉冲、雨丝/粒子漂移、水面反光。

必须记录：

```text
provenance/seedance_request.json
provenance/seedance_prompt.md
provenance/seedance_task_id.txt
generated/background_dynamic.mp4
generated/background_dynamic.webm
generated/background_dynamic.gif
```

检查：

```bash
ffprobe -v error -show_entries stream=width,height,duration -of json generated/background_dynamic.mp4
ffmpeg -i generated/background_dynamic.mp4 -vf "select='eq(n,0)+eq(n,75)+eq(n,149)',scale=480:-1,tile=3x1" screenshots/seedance_frames.png
```

如果没有真实 task id 或真实下载文件，runtime 必须关闭 dynamic video，并在交付报告中写明本轮使用静态背景。

## 7. 角色与动作节点

优先用外部 `generate2dsprite`。如果外部 skill 不存在，必须读取并执行 v2 内置副本：

```text
references/embedded/generate2dsprite-SKILL.md
```

该内置副本是完整 `generate2dsprite` 子功能，不是简化契约。至少动作：

```text
idle, walk, run, jump, dash, light_attack, heavy_attack, parry, skill_cast, hurt, death
```

规则：

- 角色风格与背景协调，但颜色要能在背景中凸显。
- 动作符合人体运动规律。
- 左右脚不能在连续帧中混乱。
- 每个动作独立生成、抠底、切帧、QC。
- 所有站立/跑步/攻击帧脚底基准一致。
- 刀光、残影、弹道、命中特效是独立 FX。
- 不允许用 Phaser Graphics 圆形、矩形、线段、CSS/SVG 小人或 procedural sprite 作为最终角色。

输出：

- `generated/hero/hero_actions_contact_sheet.png`
- `generated/hero/hero_manifest.json`
- `generated/fx/fx_manifest.json`
- `benchmarks/hero_action_qc.json`

## 8. Phaser 集成节点

使用 manifest 驱动，不硬编码某一套素材。

必须实现：

- 移动、跳跃、dash、轻攻击、重攻击、parry、skill_cast。
- 胜利或死亡后 `R` 重开。
- 起点、平台挑战、首次战斗、技能获得、能力门、精英/Boss、右端终局门。
- `window.__GAME_DEBUG__.snapshot()`。
- `teleportTo()`、`grantDash()` 等自动测试辅助。

相机规则：

- 横向：gameplay 世界最快，中景中等，背景最慢。
- 横向端点：角色到世界最右端时，背景和中景也显示到资产最右端。
- 跳跃纵向：gameplay 基本稳定，背景向下最多，中景向下更小，接近前景稳定。
- 攻击推近：用 Phaser camera zoom/easing，不整体缩放 canvas。
- 回拉不能抖动；背景/中景/前景要像同一镜头空间里的不同深度，而不是互相滑动。

碰撞规则：

- 站立线按石块/实体接触面，不按草花最高 alpha。
- 透视横条上，脚可落在石块上半部或中部。
- benchmark 要检查脚底与 stone contact plane，而不是图片最高边。

## 9. Benchmark 与截图评价节点

本地 OpenGame-style，不冒充官方 OpenGame-Bench。

BH Build Health：

```bash
npm run build
npm run validate:pipeline
npm run dev -- --port 5173 --strictPort
curl -I http://127.0.0.1:5173/
```

VU Visual Usability：

```bash
npm run benchmark:playfield-fit
npm run benchmark:visual-usability
npm run benchmark:parallax-depth
npm run benchmark:grounded-foot-contact
```

IA Intent Alignment：

```bash
npm run benchmark:playthrough
npm run benchmark:combat-progression
npm run benchmark:restart-after-victory
```

如果 repo 没有这些脚本，创建等价脚本。最小检查包括：

- 页面 HTTP 200。
- 浏览器无 fatal console/request error。
- 截图非空。
- 背景尺寸和 playfield 融合。
- 横向端点正确。
- 跳跃纵向视差方向和幅度正确。
- 动态背景 provenance 真实。
- 可见资产来源 gate 通过，且截图中能看到 selected assets。
- 没有程序化占位图、debug rectangle、黑图、纯色块、噪声墙、SVG 几何图冒充最终资产。
- 中景真 alpha，且不是灰度通道图。
- 角色动作可读。
- 脚底接触面正确。
- 自动路线能到右端终局门并胜利。
- `R` 能重开。

可选外部 benchmark：

- VBench：视频质量和运动一致性。
- GenEval / T2I-CompBench：图像组合与提示一致性。
- GameCraft / VideoGameQA：游戏画面和玩法问答。

外部工具不可用时记录：

```text
SKIPPED_NO_SCORE
```

不得伪造官方分数。

但如果所有 public runners 都是 `SKIPPED_NO_SCORE`，这是 benchmark infrastructure failure，不是正常通过。正式节点必须阻断，并回到 `Public Benchmark Bootstrap` 节点配置 runner 或 wrapper。

如果有 public runner READY：

- 先生成 `public_benchmark_input_pack_report.json`。
- 再执行 READY runner 或 wrapper。
- 每个结果都写 `implementation_mode`、`runner_status`、`official_score`、`leaderboard_comparable`、`score`、`skip_reason`、`diagnostics`。
- 不能用 `READY`、`PENDING_NOT_EXECUTED`、`input_missing` 替代真实执行结果。
- 如果执行失败，先修输入包或 runner，不要把 benchmark 基础设施失败误当成画面失败。

## 10. 迭代搜索节点

使用 `references/iteration-search-strategy.md` 的 `SABG` 策略：阶段化自适应最佳优先图搜索 + 局部贪心修复。

策略选择：

- 设计候选、核心美术方向、中景/角色/背景这类离散问题，用有界 best-first 图搜索。
- 相机比例、背景裁切、视频速度、跳跃高度、碰撞线这类连续或低成本参数，用局部贪心/坐标搜索。
- 用户反馈先分类，再决定回到哪个节点。
- 每个被接受节点都保存截图、benchmark、manifest 和 provenance，防止后续回退。
- 每条审核建议都必须进入 `review_action_queue`，变成候选节点后测试、接受、回滚或延期。

按失败节点回退：

- 设计失败：重写设计，不生成资产。
- 可见资产来源失败：回到 `generate2dmap` / `generate2dsprite` / image generation / approved asset 节点，不能继续调 runtime 参数来掩盖。
- public benchmark 全部 skipped：回到 `Public Benchmark Bootstrap` 节点，不能把 all-skipped 当作 final success。
- public runner READY 但没执行：回到 `public_benchmark_input_pack` 和 `public_benchmark_execution`。
- public runner 因长 prompt 文件名失败：改短 slug 文件名，完整 prompt 留在 manifest，再重跑。
- benchmark 放过占位图：先修 benchmark 规则，再重跑，不要继续声明成功。
- 背景失败：重写背景 prompt 或重做 Seedance。
- 中景失败：重做抠像/颜色/位置，不改玩法。
- 角色失败：重做动作或脚底基准，不改地图。
- 相机失败：调 depth ratio、easing、端点映射。
- 玩法失败：调碰撞、能力门、敌人、路线。
- 用户反馈失败：把反馈转成新 benchmark 或截图检查。
- 审核建议未处理：转成 SABG 节点，不要只写报告。
- 旧 prototype/SVG/contact sheet/manifest 误导评审：清理到 `discarded/` 或从 selected manifest 移除，再重跑 source gate。

默认预算：

- 设计候选 3 个。
- 设计 critic 3 轮。
- 资产重生成 3 轮。
- 集成修复 5 轮。

## 11. 最终交付

必须给用户：

- 本地 URL。
- 资产目录。
- manifest 路径。
- Seedance 是否真实调用，task id 和输出路径。
- benchmark 结果。
- 关键截图和视频路径。
- 每个重要节点的图像预览路径。
- 剩余风险和下一阶段计划。

只有以下条件都满足才算成功：

- 从开始能玩到胜利。
- hard gates 全通过。
- 用户能打开本地 URL。
- 截图/视频证明当前游戏使用的是选中资产。
- `asset_manifest.json` 证明 final visible assets 不来自 `procedural_debug`。
- 背景/平台/中景等地图资产有 `generate2dmap` 或等价图像生成 provenance。
- 主角/敌人/Boss/FX 有 `generate2dsprite` 或等价 sprite 生成 provenance。
- `.game_scientist/benchmark_bootstrap_report.json` 证明至少一个 public runner READY；否则只能标记 prototype/advisory。
- READY public runner 已经实际执行，或报告给出明确阻断原因并把本轮标为 prototype/advisory。
- 用户反馈的问题已经修复或转成可复测 benchmark。
- critic/review 建议已经实施、回滚或明确延期。
- 旧的程序化/SVG/debug/prototype 资产没有留在 selected asset 目录中制造假证据。
