---
name: 2dwebgame-autoresearch-v2
description: Use when the user wants a Chinese AI-Scientist-style end-to-end pipeline for Phaser/Vite Web 2D game generation from a game idea, character/environment description, or one/more reference images. The skill creates and critic-iterates a structured design plan, generates layered 2.5D scene assets and sprites, uses real Seedance dynamic backgrounds when authorized, runs progressive full-scale layer benchmarks before runtime integration, performs local OpenGame-style BH/VU/IA playability checks, records public benchmark adapters as official/faithful/strict/SKIPPED_NO_SCORE, and iteratively modifies only failed game nodes from benchmark feedback until a high-quality playable Web game is verified.
---

# 2DWebGame AutoResearch v2

## 定位

这个 skill 是 `2dwebgame-autoresearch-v1` 的 v2 版本，用 AI Scientist v1/v2 的“模板契约 -> 创意生成 -> 设计评审 -> 实验/实现 -> benchmark -> 反馈搜索 -> 证据归档”模式，自动制作和迭代 Phaser/Vite Web 2D 横版游戏。

v2 的核心变化是：benchmark 不只是最终验收，而是进入资产生成、层级合成、运行时集成、玩法通关和用户反馈修复的每一轮决策。每次修改都必须来自具体失败项、截图证据、用户反馈或明确的改进信号；没有内容失败时，不要为了“看起来有改动”破坏已经通过的版本。

默认目标是 Web 游戏，不进入 Unity。若外部计划写了 Unity runtime import，本 skill 中对应为 Phaser runtime import。

## 与 v1 的关系

v1 已经包含 benchmark 反馈迭代：`evaluation node -> revision node`、BH/VU/IA、本地 OpenGame-style 检查、按失败节点回退、SABG 搜索策略等都来自 v1。v2 不否定 v1，而是把这些机制变成更严格、更可执行的工程闭环。

v2 在 v1 基础上新增或强化：

- 在 Phaser runtime 之前加入 progressive full-scale layer benchmark。
- 把每一层和每一步合成图作为独立证据，而不是只看运行时截图。
- 增加 strict/advisory policy，区分正式选择和本地预览。
- 要求公共 benchmark 记录 `official_score`、`implementation_mode`、`leaderboard_comparable`、`SKIPPED_NO_SCORE` 和 skip reason。
- 明确公共 runner 缺失是 benchmark infrastructure failure，不是内容失败。
- 把 failure signatures 映射成具体修改节点，形成 `run benchmark -> read failures -> patch node -> rerun -> accept/rollback` 的闭环。

## 内置规则

本 skill 必须独立运行，不能依赖 v1 目录。v1 的四份基础参考已经复制到 v2 自己的 `references/` 目录：

- `references/ai-scientist-foundations.md`
- `references/game-design-template.md`
- `references/iteration-search-strategy.md`
- `references/pipeline-cn-v1-base.md`

执行完整任务时优先读本 `SKILL.md`。需要更细的模板或流程时，再读取上述 v2 本地参考文件，不要读取 v1 路径。

内置核心规则如下：

- AI Scientist v1 迁移到游戏时，模板不是固定游戏内容，而是固定产物契约：设计计划、manifest、runtime scaffold、benchmark、截图、证据目录。
- AI Scientist v2 迁移到游戏时，要从高层主题或参考图生成结构化设计方案，再通过 critic 和阶段化树搜索推进，不要一个 prompt 直接生成资产。
- 任何地图、角色、Seedance、Phaser 集成之前，必须先有 `game_design_plan.md`、`game_design_plan.json`、critic 记录和 design decision log。
- 游戏设计至少包含核心幻想、30-90 秒循环、移动/跳跃/攻击/技能、能力门、敌人或 Boss、右端终点、胜利、`R` 重开。
- 每个候选设计必须能被 benchmark：Build Health、Visual Usability、Intent Alignment、playfield fit、parallax depth、grounded foot contact、playthrough、restart。
- 迭代策略使用 SABG：设计和资产方向用有界 best-first 图搜索；相机、视差、碰撞、速度、跳跃、播放速率用局部坐标搜索。
- 每个节点必须记录 parent、改动原因、prompt/patch、benchmark、截图/视频、用户反馈、回归项、pass/fail 和下一步。
- 只从当前最佳通过节点继续；如果新节点修复一个指标但破坏 hard gate 或用户意图，必须回滚。
- v2 额外加入 progressive full-scale layer benchmarking、strict/advisory policy、public benchmark `SKIPPED_NO_SCORE` 规则和 benchmark-feedback iteration 控制器。

## 输入契约

用户可以提供：

- 角色描述。
- 环境或关卡描述。
- 游戏设计创意。
- 一张或多张角色、背景、氛围参考图。
- 用户反馈，例如“中景太灰”“门不在最右边”“脚悬空”“背景动效太快”。

如果没有游戏创意，自动生成 3 个候选游戏设计，再用 critic 评分选出一版。不要从一句 prompt 直接生成资产。

## 工具能力

优先使用：

- `generate2dmap`：side-scroll 地图、runtime objects、分层契约。
- `generate2dsprite`：角色动作、透明帧、动作一致性 QC。
- `game-studio:phaser-2d-game`：Phaser/Vite 场景、输入、HUD、相机。
- `game-studio:game-playtest`：可玩性与通关测试。
- `volcengine:volcengine` / `chrome:control-chrome`：用户授权后调用火山引擎 Seedance。
- `playwright`：截图、控制浏览器、自动通关、console/request 检查。
- `ffmpeg` / `ffprobe`：视频尺寸、时长、首尾帧、GIF/WebM/MP4 转换。
- 可选公共 benchmark：VBench、GenEval、T2I-CompBench、DoveNet/iHarmony、GameCraft、VideoGameQA。

公共 benchmark 不可用时必须写 `SKIPPED_NO_SCORE`，不能用弱代理分数冒充官方或 leaderboard 可比结果。

## 总流程

每次 run 按节点执行：

1. `repo_preflight`：检查项目、脚本、服务、已有 manifest 和 benchmark。
2. `reference_analysis`：复制参考图，分析风格、色彩、空间、动态线索、禁止项。
3. `idea_design_search`：生成或补全设计方案，critic 最多 3 轮。
4. `asset_generation`：背景、中景、平台、角色、FX、Seedance 动态背景。
5. `progressive_layer_composition_benchmark`：资产进入 Phaser 前，做全尺寸逐层合成与评测。
6. `phaser_runtime_integration`：manifest 驱动加载、输入、碰撞、相机、HUD、debug API。
7. `runtime_benchmark`：构建、服务、截图、视频、通关、动作、相机、层级、用户反馈。
8. `benchmark_feedback_iteration`：按失败项只修改对应节点，复测，接受或回滚。
9. `handoff`：交付 URL、图片/视频/JSON 证据、得分、剩余风险。

## 设计 Gate

资产生成前必须形成：

- `game_design_candidates.json`
- `game_design_plan.md`
- `game_design_plan.json`
- `design_critic_round_*.md`
- `design_decision_log.md`

设计必须覆盖：

- 核心幻想和 30-90 秒核心循环。
- 起点、移动、跳跃、攻击、技能、拾取、能力门、敌人/Boss、终点胜利、`R` 重开。
- 背景、中景、gameplay 层级契约。
- Seedance 动态背景 prompt 和 provenance。
- 角色动作、脚底基准、动作连续性、独立 FX。
- 相机横向端点、纵向跳跃视差、攻击推近镜头。
- benchmark 清单和截图验收点。

critic hard-fail：

- 没有从开始到胜利的可玩流程。
- 背景/中景/gameplay 层级不清。
- 中景是半透明背景、灰度通道图或漂浮物。
- 终局门和世界最右端无法验证。
- 角色动作、碰撞、相机规则不可测试。
- Seedance provenance 不可追溯。
- 用户反馈无法转成 benchmark 或截图检查。

## 层级与资产规则

默认层级：

```text
完整远景动态/静态背景 -> 可选 alpha 中景物体 -> gameplay 平台/角色/敌人/FX/HUD
```

不要把背景拆成多个模糊层。背景是一张完整远景；中景是在背景和 gameplay 之间增加的具体物体，不是铺满画面的第二背景。

中景要求：

- 必须是真 alpha 抠像。
- 必须是具体物体，如岩石、树根、藤蔓、塔、灯、废墟。
- 空洞显示背景，不能靠整体透明度假装露背景。
- 色彩与背景同调，色度/亮度可高于背景，但黑白对比低于前景。
- 底部要接到画面底部，不能悬浮。
- 边缘虚实结合：岩石/建筑硬，雾边/光晕/细藤软。
- 不要灰成通道图，不要紫边污染。

平台、门、敌人、拾取物、碰撞体必须是 runtime 数据，不烤进背景。

## Seedance 动态背景

Volcengine / Seedance / 其他视频生成服务都是可选增强，不是硬依赖。只有用户明确表示愿意开通、登录并授权外部视频生成时，才调用 Seedance 或等价服务。

如果用户没有视频生成服务、当前机器无法调用、额度不足、登录失败或下载失败，跳过动态视频生成，直接使用静态背景继续完成游戏。静态背景仍然必须通过尺寸、视差、playfield fit、画面融洽度和 runtime screenshot 检查。

真实调用时必须记录：

- prompt
- source image
- model
- task id
- request body
- 下载的 MP4/WebM/GIF
- provenance JSON
- QC 报告

Seedance prompt 必须要求：

- 4K、约 5 秒、无缝循环。
- 超宽横版，约两屏宽，高度略高于视口。
- 保持参考图整体色调，不换成新场景。
- 不加角色、敌人、UI、平台、黑边、白边、上下模糊条、镜像填充、人工补边。
- 上中下都有环境动态：光束呼吸/漂移、雾带滚动、水晶/灯光脉冲、雨丝/粒子漂移、水面/反光流动。
- 首尾帧视觉连续，循环无接缝。

如果没有真实 task id 或真实下载文件，不要做假动态视频，runtime 必须关闭 dynamic video，并在报告中说明本轮使用静态背景。

## Progressive Full-Scale Layer Benchmark

v2 新增硬性阶段：资产生成后、Phaser runtime 集成前，必须做全尺寸逐层合成验证。运行时截图仍然必须做，但不能替代全尺寸层级验证。

建议 CLI：

```bash
npm run layers:preview
npm run layers:benchmark
npm run layers:benchmark:advisory
```

若项目没有这些脚本，创建等价命令：

```bash
layers preview --project <path> --manifest <asset_manifest.json> --out <dir>
layers benchmark --project <path> --manifest <asset_manifest.json> --out <dir> --policy strict|advisory
```

必须生成：

```text
layer_contract_report.json
full_scale_layer_previews/far.png
full_scale_layer_previews/far_mid.png
full_scale_layer_previews/far_mid_near.png
full_scale_layer_previews/full_scene.png
progressive_layer_benchmark_report.json
progressive_layer_benchmark_report.strict.json
progressive_layer_benchmark_report.advisory.json
```

层级顺序默认：

```text
far_background -> midground_objects -> near/atmospheric overlays -> gameplay runtime objects
```

层级数量可灵活，但每一步都要有全尺寸预览和 provenance。两层场景允许存在，但必须解释为什么没有中景或近景。

### 独立层检查

每个 layer 独立检查：

- 文件存在、尺寸符合 contract。
- provenance/source-set 存在。
- 非空、非 placeholder、非模糊色块。
- 中景 alpha coverage 合理，不是满屏背景。
- 中景左右/底部接地，不漂浮。
- 无 key color / 紫边 / 白边 / 黑边泄漏。
- 背景是完整场景，不缺上中下内容。

可用公共 benchmark：

- T2I-CompBench：内容逻辑、prompt alignment、尺度/透视关系、world-role suitability。
- GenEval：仅在对象属于 detector 支持类别时使用；游戏特定对象不支持时写 `SKIPPED_NO_SCORE`。

### 逐层合成检查

按远到近逐步合成：

1. `far.png`
2. `far_mid.png`
3. `far_mid_near.png`
4. `full_scene.png`

每加入一层都检查：

- 新层是否真的改变画面。
- 新层是否遮挡不该遮挡的背景。
- 中景/前景是否嵌入同一世界，而不是贴纸。
- 遮罩是否有效。
- 画面是否仍然有深度、空间、可玩区域。
- gameplay runtime objects 是否跨完整世界宽度，终点是否到视觉最右端。

可用公共 benchmark：

- DoveNet/iHarmony：当有有效 mask/target 时做 harmonization；没有有效证据时写 `SKIPPED_NO_SCORE`。
- T2I-CompBench：对每一步合成生成 world-integration questions。

每条 benchmark 记录必须包含：

```json
{
  "benchmark_source": "T2I-CompBench | GenEval | DoveNet/iHarmony | local-open-game-style",
  "implementation_mode": "official_runner | faithful_metric_port | strict_protocol_replication | adapter_question_generation_only | skipped",
  "official_score": null,
  "leaderboard_comparable": false,
  "score": "SKIPPED_NO_SCORE",
  "diagnostics": [],
  "skip_reason": ""
}
```

只有真正官方 runner 才能写 `leaderboard_comparable: true`。本地复刻和 faithful metric port 也不能冒充 leaderboard 分数。

### strict/advisory 选择规则

- `strict`：2.5D scene node 默认使用。若所有 full-scale layer-fit 公共 benchmark 都是 `SKIPPED_NO_SCORE`，该节点不能自动进入 runtime selection。
- `advisory`：允许继续本地开发和截图预览，但报告必须保留 warning。
- 不要把公共 runner 缺失误报成内容失败。例如 `public_layer_fit_benchmarks_skipped` 是 benchmark infrastructure failure，不是 `layer_harmonization_fail`。
- 内容 hard gate 失败必须阻断，不允许用 advisory 放行。

## Runtime Benchmark

Phaser runtime 必须证明选中的全尺寸 layer stack 确实被导入并可见。

必须检查：

- `npm run build`
- 本地服务 HTTP 200。
- 浏览器无 fatal console/request error。
- 初始截图非空。
- 动态背景启用状态诚实。
- 实际截图使用选中的背景、中景、角色、平台、门。
- 相机横向移动时远景慢、中景中等、gameplay 快。
- 角色跳跃时远景下移最多，中景下移更少，gameplay 稳定。
- 攻击技能 camera zoom/easing 自然，回拉不抖。
- 终局门在世界/视觉最右端。
- `R` 能重开。

推荐脚本：

```bash
npm run validate:pipeline
npm run benchmark:playfield-fit
npm run benchmark:visual-usability
npm run benchmark:parallax-depth
npm run benchmark:grounded-foot-contact
npm run benchmark:playthrough
npm run benchmark:restart-after-victory
npm test
```

如果项目没有这些脚本，创建等价 Playwright/Node 脚本。

## OpenGame-Style BH / VU / IA

不要声称官方 OpenGame-Bench，除非真的运行官方工具。默认是本地严格复刻。

### BH Build Health

- TypeScript/build 成功。
- 本地服务启动。
- HTTP 200。
- 浏览器非空白。
- 无 fatal console/request error。
- 资源请求无关键失败。

### VU Visual Usability

- 截图非空、熵/像素变化合理。
- 背景、中景、gameplay 层次清楚。
- 全尺寸 layer previews 与 runtime screenshots 一致。
- 动态背景尺寸、裁切、首尾循环、播放速率、动效区域符合 contract。
- 横向视差深度正确。
- 纵向跳跃视差正确：远景位移 > 中景位移 > gameplay 稳定。
- 中景真 alpha，非灰度通道图，非半透明贴纸。
- 平台脚底接触面正确，不按草花最高 alpha。
- 角色颜色在背景中突出，动作可读。
- 攻击/技能推近镜头自然，回拉不抖。
- 终点门与视觉最右端对齐。

### IA Intent Alignment

Playwright 自动验证：

- 左右移动。
- 跳跃。
- dash。
- 轻攻击、重攻击、parry、skill_cast。
- 拾取能力。
- 打开能力门。
- 击败敌人或 Boss。
- 到最右端终局门。
- 胜利。
- `R` 重开。

## Benchmark Feedback Iteration

v2 必须把 benchmark 结果转成修改策略。不要只生成报告后停止。

推荐命令：

```bash
npm run iterate:scene
```

若没有该脚本，创建等价控制器：

1. 运行 layer benchmark。
2. 运行 playfield-fit。
3. 运行全量 BH/VU/IA。
4. 读取 JSON 报告。
5. 分类失败项。
6. 生成修改动作。
7. 只修改失败节点。
8. 重新 build 和 benchmark。
9. 接受更优节点或回滚。
10. 保存 iteration report。

必须保存：

```text
benchmark/results/iteration/latest_iteration_report.json
benchmark/results/iteration/latest_iteration_report.md
```

### 失败签名到修改节点

- `far_layer_content_logic_fail`：回到背景 prompt / 背景资产生成。
- `mid_layer_style_or_depth_mismatch`：重做中景抠像、色彩、边缘、接地。
- `layer_harmonization_fail`：修中景/前景与背景的光色融合；只有公共或 faithful harmonization 真的失败时使用。
- `foreground_not_embedded_in_world`：修 gameplay 平台、门、角色接触、尺度。
- `full_scale_composition_mismatch`：修 layer scale、anchor、stack order、世界宽度。
- `playfield_background_fit_fail`：调背景裁切、高度、横向 parallax、纵向 travel。
- `dynamic_background_motion_fail`：回到 Seedance prompt/source image，不能假动态。
- `parallax_depth_fail`：调背景/中景 scroll factor。
- `jump_y_parallax_fail`：调纵向 parallax 公式，防止方向反或中景位移过大。
- `foot_contact_fail`：调 collision/contact plane，不重画角色。
- `hero_action_readability_fail`：调角色颜色、动作帧、脚底基准、FX 分离。
- `playthrough_fail`：调关卡路线、跳跃高度、门位置、敌人/拾取物。
- `restart_fail`：修状态重置。
- `public_layer_fit_benchmarks_skipped`：这是 benchmark infrastructure failure，不允许因此修改游戏内容；配置公共 runner 或保留 advisory warning。

### 接受/回滚规则

接受节点必须同时满足：

- hard gates 不退化。
- 修复目标失败项。
- 截图/视频证明新资产或新参数实际生效。
- 用户关键反馈没有回退。
- 没有把 `SKIPPED_NO_SCORE` 当成内容分数。

如果修改修了一个指标但破坏更高优先级用户意图，必须回滚到上一个 passing node。

## 搜索策略

使用 SABG：Stage-gated Adaptive Best-first Graph search。

- 设计、核心资产方向、中景/角色/背景：有界 best-first 图搜索。
- 相机、视差、碰撞、速度、跳跃、播放速率：局部贪心/坐标搜索。
- 公开 benchmark 配置缺失：基础设施节点，不修改游戏内容。
- 用户反馈：先转成 benchmark，再修对应节点。

默认预算：

- 设计候选 3 个。
- 设计 critic 最多 3 轮。
- 资产重生成最多 3 轮。
- 集成修复最多 5 轮。
- 数值/相机局部搜索每轮只改一个参数簇。

## 交付清单

最终中文交付必须包含：

- 本地 URL。
- 资产目录。
- manifest 路径。
- Seedance 是否真实调用、task id、输出路径。
- progressive layer previews 路径。
- strict/advisory benchmark 报告路径。
- BH/VU/IA 分数。
- 关键截图路径。
- 迭代报告路径。
- 哪些失败项触发了哪些修改。
- 哪些公共 benchmark 是 `SKIPPED_NO_SCORE`，原因是什么。
- 剩余风险和下一阶段建议。

## 常见错误

- 不要把背景拆成多个模糊层。
- 不要让中景成为第二张满屏背景。
- 不要用半透明中景假装 alpha 抠像。
- 不要把公共 benchmark 缺失误报成内容失败。
- 不要因为 `SKIPPED_NO_SCORE` 去乱改画面。
- 不要只看运行时截图，必须先看全尺寸 layer stack。
- 不要只看全尺寸预览，必须再看实际 Phaser runtime。
- 不要把 gameplay 平台、门、角色烤进背景。
- 不要让角色到终点时背景/中景还没滚到最右端。
- 不要把纵向跳跃视差写反。
- 不要按草花最高 alpha 设置站立线。
- 不要在未真实调用 Seedance 时伪造动态视频。
- 不要为了过 benchmark 放宽真实失败；应该改 benchmark 让它捕捉真实问题。
