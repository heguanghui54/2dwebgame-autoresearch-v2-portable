# Iteration Search Strategy

Use this reference when deciding how to iterate after design, asset, integration, benchmark, or user-feedback failures.

## AI Scientist v2 Baseline

AI Scientist v2 uses agentic tree search across all major experimentation stages. Stage 2 hyperparameter tuning is not a simple linear hill-climb:

- Stage 1 first finds a working preliminary implementation.
- The best Stage 1 node seeds Stage 2.
- Stage 2 creates hyperparameter tuning nodes from that parent.
- Tested hyperparameters are recorded to avoid redundant experiments.
- Buggy nodes can spawn debug children.
- Non-buggy nodes can spawn refinement children.
- A best-performing node is selected by evaluation and carried into Stage 3.
- Stages have iteration budgets and completion criteria.

For Web 2D games, copy the structure, not the exact ML metric logic.

## Why Pure Strategies Fail For Games

Pure graph search fails because:

- image/video generation is expensive and slow,
- too many visual branches become impossible to inspect,
- user taste is partly subjective,
- external tools like Seedance may be rate-limited or costly.

Pure greedy hill-climbing fails because:

- early bad art direction can trap all later fixes,
- camera/background/midground/player changes interact,
- a later user feedback item may require returning to an earlier good node,
- some improvements temporarily lower one metric before improving the whole scene.

Pure adaptive local tuning fails because:

- structural choices such as midground/no midground, character style, or level route are discrete,
- asset provenance and visual style are not continuous parameters,
- benchmark scores can miss high-level design incoherence.

## Recommended Strategy

Use a hybrid: stage-gated adaptive best-first graph search with local greedy repair.

Short name: `SABG` - Stage-gated Adaptive Best-first Graph search.

Principle:

- Use graph search for irreversible or high-level decisions.
- Use local greedy/coordinate tuning for numeric runtime parameters.
- Use rollback to the best checkpoint whenever a node improves one metric but harms hard-gated user intent.
- Use critic or screenshot review before expanding expensive asset branches.

## Node Types

Every node must record:

- parent node id,
- changed artifact or files,
- change reason,
- prompt or patch summary,
- benchmark results,
- screenshots/video probes,
- user-feedback items addressed,
- regression items,
- pass/fail label,
- next recommended action.

Node labels:

- `design_candidate`
- `design_revision`
- `background_asset`
- `seedance_video`
- `midground_asset`
- `hero_sprite`
- `phaser_integration`
- `camera_tuning`
- `collision_tuning`
- `gameplay_route`
- `benchmark_rule`
- `user_feedback_patch`

Bug labels:

- `build_buggy`
- `visual_buggy`
- `gameplay_buggy`
- `provenance_buggy`
- `regression_buggy`
- `user_intent_buggy`

## Stage Policy

### Stage 1: Design Search

Use breadth first, then best-first.

- Generate 3 design candidates.
- Critic scores all candidates.
- Expand only the top 1 or top 2.
- Stop when design critic passes.

Do not use local tuning here. Bad design must be redesigned, not patched with assets.

### Stage 2: Asset Direction Search

Use bounded best-first branching.

Branch only high-impact assets:

- background style,
- optional midground object design,
- hero silhouette/color,
- platform material language.

Default branch budget:

- 2 variants for background or hero if critic is uncertain.
- 3 variants only when user explicitly dislikes a core visual direction.
- 1 selected asset proceeds to integration.

Use screenshot/LLM visual review before expensive video generation.

### Stage 3: Playable Baseline

Use greedy stabilization.

Goal: get a playable path from spawn to victory with placeholder or selected assets.

Fix hard failures in this order:

1. build/server blank screen,
2. manifest loading,
3. player spawn and controls,
4. collisions,
5. route continuity,
6. win and restart.

Do not branch art here unless art breaks gameplay readability.

### Stage 4: Visual-Camera Tuning

Use adaptive coordinate search.

Tune one cluster at a time:

- background scale/crop,
- horizontal parallax mapping,
- vertical jump parallax,
- midground depth ratio,
- camera zoom target,
- camera easing duration,
- background video playback rate,
- hero scale and collision box,
- platform contact plane.

Rule:

- change one cluster,
- run screenshot benchmark,
- compare against previous best,
- keep if it improves hard gates and user-visible quality,
- rollback otherwise.

This is the stage where greedy hill-climbing is appropriate.

### Stage 5: User Feedback Search

Classify user feedback before editing.

- Structural feedback: branch from best checkpoint and compare alternatives.
- Numeric/camera feedback: local coordinate tuning.
- Asset-style feedback: bounded asset branch.
- Gameplay difficulty feedback: local gameplay tuning.
- Benchmark-miss feedback: add a benchmark, then fix.

Examples from the first successful game:

- "背景太高，看不到溪流" -> local background scale/crop tuning.
- "跳跃时背景上下运动反了" -> local camera/parallax rule fix.
- "背景动效太快" -> local video playback-rate tuning.
- "中景像灰度通道图" -> asset branch/rollback to earlier good midground.
- "门不在最右端" -> world endpoint mapping and playfield-fit benchmark.
- "脚悬空" -> collision/contact-plane tuning, not art regeneration.
- "角色不突出" -> bounded hero color/style branch.

### Stage 6: Regression Lock

After each accepted node, lock the passing evidence:

- screenshot set,
- benchmark JSON,
- selected manifest,
- asset provenance,
- user-feedback checklist.

Do not accept a new node if it breaks a locked hard gate unless explicitly replacing that gate with a stricter one.

## Scoring Function

Use hard gates first, weighted score second.

Hard gates:

- build health pass,
- playable start-to-win route,
- no fake Seedance,
- no blank/incorrect layer,
- final door at visual/world right edge,
- restart works,
- selected assets visible in screenshots.

Weighted score:

```text
score =
  0.25 * visual_usability
+ 0.20 * gameplay_completion
+ 0.15 * user_intent_alignment
+ 0.15 * camera_parallax_quality
+ 0.10 * character_readability
+ 0.10 * asset_provenance_quality
+ 0.05 * performance_stability
```

Hard-gate failure overrides weighted score.

## Expansion Rules

Expand a node when:

- it passes hard gates but has a clear improvement opportunity,
- a critic identifies a concrete next action,
- user feedback points to a localized issue,
- the node is the current best in its stage.

Do not expand a node when:

- it lacks provenance,
- screenshots do not use its assets,
- it fixes a metric by degrading user intent,
- it needs broad rework but was only meant to tune a numeric parameter.

## Stopping Rules

Stop a stage when:

- all hard gates for that stage pass,
- critic has no hard-fail,
- further improvements are cosmetic and outside the requested scope,
- budget is exhausted and current best is clearly reportable.

Stop the whole run only when:

- game can be played from start to victory,
- hard gates pass,
- user-visible screenshots/video confirm assets and motion,
- user feedback checklist is resolved or explicitly deferred,
- final handoff includes URL, assets, manifest, benchmark, screenshots, and provenance.

