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
- Visual Usability.
- Intent Alignment.
- playfield fit.
- parallax depth and endpoint mapping.
- dynamic background truth/provenance.
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

Iterate up to 3 design rounds.

Pass only when:

- average score >= 8,
- no criterion below 7,
- no hard-fail,
- all benchmark gates are testable.

If the critic fails the design after 3 rounds, stop implementation and report the blocker.

## Design Decision Log

Record:

- chosen candidate and why,
- rejected candidates and why,
- critic changes applied,
- user constraints preserved,
- assumptions,
- risks deferred to implementation.

