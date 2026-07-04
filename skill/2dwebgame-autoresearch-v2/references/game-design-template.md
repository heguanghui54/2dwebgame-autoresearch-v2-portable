# Game Design Template And Critic Gate

Use this template after reference analysis and before any asset generation or code integration. It is the pipeline's equivalent of AI Scientist v1's template contract plus AI Scientist v2's prompt-generated proposal.

## Output Files

Create these files under the run folder:

```text
design/
  game_design_plan.md
  game_design_plan.json
  design_critic_round_1.md
  design_critic_round_2.md
  design_critic_round_3.md
  design_decision_log.md
```

If a round passes earlier, later critic files are not required.

## Candidate Generation

Generate 3 candidates unless the user gave a precise design and asked not to branch.

Each candidate must include:

- `title`
- `one_sentence_fantasy`
- `target_player_feeling`
- `reference_image_observations`
- `visual_style`
- `core_loop_30s`
- `verbs`
- `level_flow`
- `ability_progression`
- `enemy_and_hazard_plan`
- `boss_or_elite_plan`
- `win_condition`
- `restart_rule`
- `camera_and_parallax_plan`
- `background_dynamic_plan`
- `midground_plan`
- `character_action_plan`
- `visual_asset_source_plan`
- `public_benchmark_bootstrap_plan`
- `public_benchmark_input_plan`
- `asset_manifest_plan`
- `benchmark_plan`
- `risk_register`

## Required Plan Content

### Game Summary

- Name the game.
- State the playable genre and subgenre.
- State the main player fantasy in one sentence.
- State what makes this run visually and mechanically specific.

### User Intent And References

- List all user-provided images and descriptions.
- Summarize each reference's palette, composition, depth, and motion cues.
- Name what must be preserved.
- Name what must be avoided.

### Player Loop

Define a 30 to 90 second playable loop:

```text
spawn -> learn movement -> jump challenge -> enemy contact -> gain/activate skill -> pass gate -> elite/boss -> right-edge exit -> victory -> R restart
```

### Controls

Default controls:

- `A/D` or arrow keys: move.
- `W`, up arrow, or space: jump.
- `Shift`: dash.
- `J`: light attack.
- `K`: heavy attack.
- `L`: parry.
- `I` or `U`: skill_cast.
- `R`: restart after death or victory.

Change only if the user requests different controls.

### Level And Runtime Objects

List runtime objects, not painted decorations:

- spawn,
- platforms,
- moving platforms if any,
- pickups,
- ability gate,
- hazards,
- enemies,
- elite or boss,
- checkpoint,
- final door/exit at visual right edge,
- collision planes,
- scripted hooks.

For each platform, state whether the collision plane follows stone/solid material rather than grass or decoration.

### Art Direction

Define:

- background as a complete pure scene, not split into fake layers,
- optional alpha midground only when needed,
- gameplay platforms and characters as runtime layer,
- no foreground overlay unless user explicitly asks.

For midground:

- must be concrete cutout objects,
- must reveal background through true alpha,
- must not be semi-transparent full-screen haze,
- must use colors coordinated with the background,
- must not become grayscale/channel-like,
- must visually connect to bottom when designed as rooted rocks/trees,
- must use softer edges only for fog, glow, and tiny vines.

### Visual Asset Source Plan

Before implementation, declare how every final visible asset will be produced. This is a hard gate, not documentation after the fact.

Required mapping:

- background, midground, platforms, gates, pickups, hazards: `generate2dmap` side-scroll mode or an equivalent image-generation / approved high-resolution asset workflow.
- hero, enemies, boss, slash/projectile/impact/dash/parry FX: `generate2dsprite` hero/action bundle mode or an equivalent sprite-generation / approved high-resolution asset workflow.
- dynamic background video: real Seedance or equivalent external service only when authorized and provenance is available.
- debug overlays, collision guides, layout sketches: may use Canvas/SVG/Phaser Graphics, but must be marked `procedural_debug` and excluded from final selected visual stack.

For each asset role, the plan must include:

- intended generator or approved asset source,
- source prompt/reference image,
- raw output path,
- processed output path,
- QC/contact-sheet/preview path,
- runtime screenshot proof requirement.

Hard rule:

- Low-resolution user references are style/input references only. They cannot be enlarged and shipped as final high-precision assets.
- Procedural Canvas/SVG/HTML/CSS/Phaser Graphics/geometry art cannot be accepted as final high-quality background, platform, character, enemy, boss, or FX art.

If external `generate2dmap` / `generate2dsprite` skills are not available, the plan must use v2's embedded subfunctions:

- `references/embedded/generate2dmap-SKILL.md`
- `references/embedded/generate2dsprite-SKILL.md`

Do not invent a new simplified generation contract.

### Public Benchmark Bootstrap Plan

Before implementation, declare how public benchmarks will be configured:

- project-local `.game_scientist/benchmarks.json`
- `.game_scientist/benchmark_bootstrap_report.json`
- expected `ready_public_runner_count`
- VBench runner or wrapper
- T2I-CompBench runner or wrapper
- DoveNet/iHarmony runner or wrapper and checkpoint
- skipped public runners and exact skip reasons

Hard rule:

- If all public runners are `SKIPPED_NO_SCORE`, the run may continue only as prototype/advisory. It cannot be called final high-quality automatic benchmark iteration.

### Public Benchmark Input Plan

Define the inputs each runner will receive:

- VBench: dynamic background video, runtime camera sweep, or character-action preview clip.
- T2I-CompBench: runtime screenshots, full-scale layer previews, and the design/reference prompt contract.
- DoveNet/iHarmony: composite screenshot, valid foreground/playfield/midground mask, and optional same-camera target if a strict score is claimed.
- Local OpenGame-style: Playwright screenshots, route trace, controls trace, console/request logs.

### Camera And Parallax

Define:

- horizontal range maps world left to asset left and world right to asset right.
- horizontal movement speed: gameplay fastest, midground medium, background slow.
- jump vertical parallax: gameplay stable, midground small downward motion, background larger downward motion.
- attack zoom: Phaser camera zoom/easing, not whole-canvas scaling.
- attack zoom depth ratios must prevent the foreground from sliding over background.

### Dynamic Background

If using Seedance:

- require real external generation and provenance.
- 4K or available highest resolution.
- about 5 seconds.
- seamless loop.
- two-screen horizontal scene and slightly taller than viewport.
- no letterbox, blur bars, mirror fill, UI, characters, enemies, or platforms.
- upper/middle/lower regions must all have motion.
- motion must include light beams, fog belts, particles/rain/drops, water/reflection, and glows when present.

If Seedance is not actually called or downloaded, mark dynamic background disabled.

### Character Plan

Require at least:

```text
idle, walk, run, jump, dash, light_attack, heavy_attack, parry, skill_cast, hurt, death
```

State:

- body silhouette,
- color contrast against background,
- weapon and FX,
- frame count targets,
- foot baseline rule,
- action continuity rule,
- which FX are separate sprites.

### Benchmark Plan

Define hard gates before implementation:

- Build Health.
- Visual Asset Source Gate.
- Visual Usability.
- Intent Alignment.
- playfield fit.
- parallax depth and endpoint mapping.
- dynamic background truth/provenance.
- public benchmark bootstrap ready.
- public benchmark input artifacts ready.
- grounded foot contact.
- full control and victory route.
- restart after victory.

## Critic Workflow

Use a second agent when available. If no subagent tool is available, run a clearly separated critic pass in the main agent and save it as if it came from an independent reviewer.

Critic prompt shape:

```text
You are a strict game design and production critic. Review this Web 2D Phaser game plan before any implementation. Score each criterion 1-10, list hard-fails, and propose concrete revisions. Do not implement assets or code.
```

Criteria:

- user intent alignment,
- novelty and hook,
- genre/loop coherence,
- level progression,
- visual identity,
- character readability,
- camera/parallax plausibility,
- asset feasibility,
- benchmarkability,
- production risk.
- real visual asset source feasibility.
- public benchmark infrastructure feasibility.
- benchmark input protocol feasibility.

Iterate up to 3 design rounds.

Pass only when:

- average score >= 8,
- no criterion below 7,
- no hard-fail,
- all benchmark gates are testable,
- final visual assets have a concrete generate2dmap/generate2dsprite/image-generation or approved-asset path.
- public benchmark bootstrap and input plans are concrete enough to run before final selection.

If the critic fails the design after 3 rounds, stop implementation and report the blocker.

Additional critic hard-fails:

- The plan uses code-drawn shapes, SVG, Canvas, CSS, Phaser Graphics, procedural noise, or debug rectangles as final high-quality art.
- The plan lacks a source/provenance/QC path for background, midground, platform art, hero sprite, enemy/boss sprite, or FX.
- The plan relies on benchmarks that only check non-empty screenshots and do not check whether real generated assets are visible.
- The plan has no public benchmark bootstrap or leaves all public runners skipped while still claiming automatic benchmark iteration.
- The plan has no benchmark input protocol for video, screenshots, masks, prompts, and route traces.
- The plan would allow a playable prototype to be called a final high-quality game without returning to real asset generation.

## Design Decision Log

Record:

- chosen candidate and why,
- rejected candidates and why,
- critic changes applied,
- user constraints preserved,
- assumptions,
- risks deferred to implementation.
