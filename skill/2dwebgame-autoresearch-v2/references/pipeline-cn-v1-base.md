# 2DWebGame AutoResearch v1 中文 Pipeline

本文件是执行版流程。目标是让用户给一句角色/环境描述或角色、背景参考图后，自动完成“设计方案 -> 设计评审 -> 资产生成 -> Web 2D 游戏集成 -> benchmark -> 截图/视频评估 -> 迭代修复 -> 交付”的闭环。

## 0. 总原则

- 先设计，后生成。任何地图、角色、Seedance、Phaser 代码之前，必须先通过 `game_design_plan` 和 critic gate。
- 先验证，再宣称成功。构建、截图、玩法、视觉、用户反馈都要有证据。
- 不追求一次命中。像 AI Scientist v2 一样，把候选设计和每轮修改当作节点，记录失败原因，选择最强节点继续。
- 不伪造外部资产。Seedance 没有真实调用或没有真实下载结果，就不能把本地合成物冒充动态背景。
- 不把 benchmark 当遮羞布。benchmark 要捕捉真实观感问题，不能为了过关放宽错误规则。

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
- benchmark 清单。
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

## 5. 地图与层级资产节点

默认层级：

```text
动态/静态完整背景 -> 可选 alpha 中景物体 -> gameplay 平台/角色/敌人/FX/HUD
```

不要把背景拆成多层模糊图。背景是一张完整远景；中景是在背景和 gameplay 之间增加的具体物体，不是第二张满屏背景。

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

优先用 `generate2dsprite` 或等价流程。至少动作：

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

## 10. 迭代搜索节点

使用 `references/iteration-search-strategy.md` 的 `SABG` 策略：阶段化自适应最佳优先图搜索 + 局部贪心修复。

策略选择：

- 设计候选、核心美术方向、中景/角色/背景这类离散问题，用有界 best-first 图搜索。
- 相机比例、背景裁切、视频速度、跳跃高度、碰撞线这类连续或低成本参数，用局部贪心/坐标搜索。
- 用户反馈先分类，再决定回到哪个节点。
- 每个被接受节点都保存截图、benchmark、manifest 和 provenance，防止后续回退。

按失败节点回退：

- 设计失败：重写设计，不生成资产。
- 背景失败：重写背景 prompt 或重做 Seedance。
- 中景失败：重做抠像/颜色/位置，不改玩法。
- 角色失败：重做动作或脚底基准，不改地图。
- 相机失败：调 depth ratio、easing、端点映射。
- 玩法失败：调碰撞、能力门、敌人、路线。
- 用户反馈失败：把反馈转成新 benchmark 或截图检查。

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
- 用户反馈的问题已经修复或转成可复测 benchmark。
