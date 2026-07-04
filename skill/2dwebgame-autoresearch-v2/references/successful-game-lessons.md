# 成功游戏经验与反例复盘

本文件记录从前一轮成功 Web 2D 跳跃通关游戏中抽象出的硬规则，以及 `Gearfall Mender` 失败反例带来的 benchmark 修正。执行高质量游戏生成时必须读取。

## 成功经验

1. 先做真实图像资产，再做 runtime 集成。
   - 背景、平台、门、中景、拾取物、角色、敌人、FX 都应先成为独立可查看图像资产。
   - Phaser/Vite 只负责加载、组合、碰撞、相机和玩法，不应临时画最终美术。

2. 背景和 gameplay 的职责分离。
   - 背景是完整远景，不烤入平台、门、拾取物、敌人、主角或 UI。
   - 平台、门、机关、敌人、拾取物必须是 runtime objects，有独立图像或 atlas。

3. 中景是具体物体，不是第二张背景。
   - 中景应为真 alpha 抠像，空洞显示背景。
   - 中景物体来自背景风格想象，如树根、岩石、藤蔓、灯塔、齿轮、管道。
   - 底部要接地；边缘虚实结合；不要灰成通道图或紫边污染。

4. 角色必须走动作资产流程。
   - 主角至少有 idle、run、jump、dash、light_attack、heavy_attack、parry、skill_cast、hurt、death。
   - 每个动作要有独立帧、脚底基准、动作连续性 QC。
   - 攻击弧、技能弹、命中特效、冲刺残影是独立 FX，不烤进身体帧。

5. 视差和镜头要用空间规则调。
   - 横向滚动时，gameplay 最快，中景中等，背景最慢，但世界最右端必须映射到背景/中景视觉最右端。
   - 跳跃时，gameplay 稳定；背景向下较多；中景向下更少，接近前景稳定。
   - 攻击推近用 Phaser camera zoom/easing，不能整体缩放 canvas。

6. 碰撞线按实体材质，不按装饰像素。
   - 平台脚底接触面应跟随石块/金属/实体 top plane。
   - 草、花、发光边、雾、装饰不应抬高碰撞面。

7. 终点必须利用完整世界。
   - 终局门要在世界和视觉最右端。
   - 角色到门时，背景和中景也应滚到资产右端。
   - 胜利后 `R` 必须重开完整状态。

## 工具调用规则

高质量 Web 2D 游戏不能跳过图像生成工具：

- 使用 `$generate2dmap side_scroll_mode` 生成或规划：
  - 完整 scenery background；
  - 可选真 alpha 中景；
  - 平台/门/机关/拾取物/危害物视觉资产；
  - runtime object metadata；
  - collision planes；
  - scene hooks。

- 使用 `$generate2dsprite hero_action_bundle` 生成或规划：
  - 主角动作；
  - 敌人和 Boss；
  - projectile / impact / slash / dash / parry FX；
  - transparent sheet、frame、GIF/contact sheet；
  - per-action QC。

- 只有用户明确同意外部视频生成时，才调用 Volcengine/Seedance。没有真实 task id 和下载文件时，用静态背景继续，不伪造动态。

## Gearfall Mender 失败反例

失败表现：

- 使用程序化 SVG/Phaser Graphics 画背景、平台、角色和敌人，虽然可运行但明显是占位符。
- 背景预览曾出现黑图仍被 layer benchmark 放过。
- 后来预览虽然非空，但只是几何图形和局部噪声，不是高精度图像资产。
- runtime benchmark 证明了移动、跳跃、胜利，却没有证明美术质量达标。

必须写入 benchmark 的反例 gate：

- `procedural_placeholder_art_used`：最终可见资产来自 Canvas/SVG/HTML/CSS/Phaser Graphics/脚本绘图，直接 hard-fail。
- `visual_asset_source_missing`：manifest 缺少 asset source、prompt、raw path、processed path、QC path，hard-fail。
- `black_or_broken_layer_preview`：全尺寸 layer preview 黑屏、破图标、透明空图，hard-fail。
- `noise_or_shape_only_background`：背景主体由程序化噪声、纯色块、简单几何图组成，hard-fail。
- `sprite_not_generate2dsprite_qc`：主角/敌人/Boss/FX 没有 sprite sheet/contact sheet/GIF/QC，hard-fail。
- `benchmark_false_positive_placeholder_pass`：如果上述任一问题被 benchmark 放过，先修 benchmark，不允许继续声明成功。

## 最小成功标准

一个高质量 Web 2D 游戏节点只有在以下证据都存在时才能进入 final handoff：

- `asset_manifest.json` 中所有 final visible assets 的来源不是 `procedural_debug`。
- 背景/中景/平台等地图资产有 `generate2dmap` 或等价 image generation provenance。
- 主角/敌人/Boss/FX 有 `generate2dsprite` 或等价 image generation provenance。
- 每个主要动作有 contact sheet 或 GIF QC。
- Progressive layer previews 展示真实图像资产，而不是形状占位。
- Runtime screenshots 证明 Phaser 真实加载了选中的资产。
- BH/VU/IA 全通过，并且 VU 包含 visual asset source gate。
