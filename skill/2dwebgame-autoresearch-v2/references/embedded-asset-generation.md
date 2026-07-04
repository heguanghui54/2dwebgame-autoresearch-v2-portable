# Embedded Asset Generation

本文件不是一套新的、简化的地图/角色契约。它只是 `2dwebgame-autoresearch-v2` 的子功能路由规则。

真正的地图和角色生成经验来自已经内化进本 skill 的完整 `generate2dmap` / `generate2dsprite` skill 文件。外部 peer skill 可用时优先调用；不可用时，必须读取并执行本目录内置副本，不能临时发明一套缩水流程。

## 内置副本

v2 skill 已内置以下完整参考和脚本：

```text
references/embedded/generate2dmap-SKILL.md
references/embedded/generate2dmap-layered-map-contract.md
references/embedded/generate2dmap-map-strategies.md
references/embedded/generate2dmap-prop-pack-contract.md
references/embedded/generate2dsprite-SKILL.md
references/embedded/generate2dsprite-modes.md
references/embedded/generate2dsprite-prompt-rules.md
scripts/embedded_compose_layered_preview.py
scripts/embedded_extract_prop_pack.py
scripts/embedded_generate2dsprite.py
scripts/embedded_make_sprite_layout_guide.py
```

执行资产生成时：

1. 如果外部 `$generate2dmap` / `$generate2dsprite` 可用，优先调用外部 skill。
2. 如果外部 skill 不可用，必须读取本 skill 内置的 `references/embedded/generate2dmap-SKILL.md` 或 `references/embedded/generate2dsprite-SKILL.md` 全文。
3. 当内置 `SKILL.md` 引用自己的 `references/` 或 `scripts/` 时，映射到本 skill 的内置副本。
4. 执行时以这些内置原始 skill 文件为权威；本文件只负责路由和 Web 2D pipeline 集成。
5. 不允许因为外部 peer skill 缺失就降级成程序化最终美术。
6. 仍然必须使用真实图像生成或 approved high-resolution assets 作为最终可见资产来源。

## 路径映射

`generate2dmap` 内置映射：

```text
references/layered-map-contract.md -> references/embedded/generate2dmap-layered-map-contract.md
references/map-strategies.md -> references/embedded/generate2dmap-map-strategies.md
references/prop-pack-contract.md -> references/embedded/generate2dmap-prop-pack-contract.md
scripts/compose_layered_preview.py -> scripts/embedded_compose_layered_preview.py
scripts/extract_prop_pack.py -> scripts/embedded_extract_prop_pack.py
```

`generate2dsprite` 内置映射：

```text
references/modes.md -> references/embedded/generate2dsprite-modes.md
references/prompt-rules.md -> references/embedded/generate2dsprite-prompt-rules.md
scripts/generate2dsprite.py -> scripts/embedded_generate2dsprite.py
scripts/make_layout_guide.py -> scripts/embedded_make_sprite_layout_guide.py
```

## 地图子功能

地图子功能等价于内置 `generate2dmap`。执行前必须读取：

```text
references/embedded/generate2dmap-SKILL.md
```

然后按它的 `side_scroll_mode`、Image Generation First、Layer Separation Contract、Playable Stage Reference Rules、Post-Reference Object Production Gate 执行。

本 Web 2D pipeline 只额外要求：

- 地图产物必须进入 `visual_asset_source_gate`。
- 背景/中景/平台/门/机关/拾取物/危害物必须有 provenance、QC 和 runtime screenshot proof。
- 平台、门、机关、拾取物、危害物、检查点、出口是 runtime objects，不能烤进背景。

## 角色子功能

角色子功能等价于内置 `generate2dsprite`。执行前必须读取：

```text
references/embedded/generate2dsprite-SKILL.md
```

然后按它的 `hero_action_bundle`、per-action raw grid、body-only attack/cast sheet、separate FX、magenta cleanup、frame extraction、QC 和 atlas assembly 规则执行。

本 Web 2D pipeline 只额外要求：

- 主角、敌人、Boss、projectile、impact、slash、dash、parry FX 必须进入 `visual_asset_source_gate`。
- 每个角色动作必须有 contact sheet 或 GIF 证据。
- Runtime screenshot 必须证明 Phaser 真实加载了这些 sprite/FX，而不是用 Graphics API 画形状。

## 图像生成能力

内置子功能仍然优先使用 Codex 内置 `image_gen` 生成原始图像。用户提供的低清图只能作为风格参考，不能直接放大作为最终资产。

如果当前环境没有可用图像生成能力：

- 可以完成设计、manifest、关卡逻辑和 prototype。
- 必须标记 `prototype_only`。
- `visual_asset_source_gate` 必须 hard-fail。
- 不能宣称“高精度”“一线质量”“制作成功”。

## Benchmark 关联

内置资产流程必须和 benchmark 联动：

- 每个资产生成后立即产出 QC。
- 每个 layer 进入 runtime 前必须出现在 full-scale preview。
- 每个角色动作进入 runtime 前必须有 contact sheet/GIF。
- 如果 benchmark 发现 `asset_source=procedural_debug`、缺少 QC、缺少 provenance、截图未使用选中资产，必须回到内置 `generate2dmap` / `generate2dsprite` 子功能，而不是调 runtime 参数。
