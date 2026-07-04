# AI Scientist Foundations For Web 2D Game AutoResearch

Use this reference before modifying or running the game-generation pipeline. The goal is not to copy scientific-paper tooling literally, but to preserve the automation architecture that made AI Scientist v1/v2 useful: explicit templates or generated plans, executable experiments, recorded evidence, critic feedback, and bounded iteration.

## Primary Sources

- AI Scientist v1 paper: `The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery`, arXiv `2408.06292`.
- AI Scientist v1 repo: `https://github.com/SakanaAI/AI-Scientist`.
- AI Scientist v2 paper: `The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search`, arXiv `2504.08066`.
- AI Scientist v2 repo: `https://github.com/SakanaAI/AI-Scientist-v2`.

## What To Transfer From v1

AI Scientist v1 is template-centered. It starts from a human-authored domain template and then automates idea generation, experiment iteration, plotting, paper writing, and review.

Transfer these mechanics to games:

- Treat the game template as the production scaffold, not as a vague prompt.
- Keep a reusable directory contract like v1 templates:
  - `prompt_contract.md` for the domain and style instructions.
  - `game_design_plan.json` for the structured design.
  - `scene_manifest.json` for runtime objects and assets.
  - `benchmarks/` for automated checks.
  - `screenshots/` and `evidence/` for proof.
- Generate multiple ideas before implementation.
- Each idea must contain a concrete execution plan, not only a title.
- Score ideas for interestingness, novelty, feasibility, and benchmarkability.
- Record an experiment journal after each implementation or benchmark round.
- Use reviewer feedback before declaring success.
- Only write final claims from real executed results, screenshots, metrics, and playable evidence.

Do not over-transfer v1:

- Do not make the Web 2D pipeline depend on one fixed background or one fixed game.
- Do not freeze creativity inside a single static template. The template should define required fields, gates, and artifact contracts.

## What To Transfer From v2

AI Scientist v2 moves from fixed human-authored templates toward higher-level ideation and agentic tree search. It first generates research ideas from broad topic prompts, then uses an experiment manager and BFTS-style search across stages.

Transfer these mechanics to games:

- Start from a high-level game/world/character prompt or reference images.
- Generate a design proposal before implementation, similar to a grant proposal or abstract.
- Run design reflection rounds before any asset/code generation.
- Use an independent critic/subagent at the design stage.
- Keep explicit stage budgets:
  - design candidates,
  - asset generation,
  - integration fixes,
  - benchmark-driven revisions.
- Treat every candidate or revision as a node:
  - `idea node`: game concept and player fantasy.
  - `design node`: level/ability/enemy/camera/art plan.
  - `asset node`: generated images, sprites, video, FX.
  - `integration node`: Phaser runtime and controls.
  - `evaluation node`: benchmark result and screenshots.
  - `revision node`: targeted fix derived from failures.
- Use best-first selection: continue from the strongest passing node rather than always editing the newest output.
- Carry the best node across stages and preserve checkpoints.
- Use screenshot/VLM-style critique for visuals, similar to v2 VLM figure critique.
- Mark failed nodes honestly:
  - build-buggy,
  - visual-buggy,
  - gameplay-buggy,
  - asset-provenance-buggy,
  - user-intent-buggy.

Do not over-transfer v2:

- Do not claim official AI Scientist scores or official OpenGame-Bench scores unless the real tools were run.
- Do not let tree search become unbounded. Keep budgets explicit and stop with useful evidence.
- Do not skip the implementation scaffold. Games still need a stable Phaser/Vite runtime template.

## Required Mapping

| AI Scientist concept | Web 2D game equivalent |
| --- | --- |
| Research topic | User game idea, role/environment description, reference images |
| Literature search | Reference analysis, prior-art/gameplay pattern search when needed |
| Idea JSON | Candidate game design JSON |
| Human-authored template in v1 | Phaser runtime + benchmark + asset contract scaffold |
| Template-free ideation in v2 | LLM-generated game design plan from broad brief |
| Experiment plan | Implementation plan for level, assets, controls, benchmarks |
| Experiment execution | Asset generation, code integration, build/playtest |
| Plot/VLM review | Screenshots, video probes, visual benchmark, LLM image critique |
| Paper writeup | Final playable handoff and production report |
| LLM reviewer | Design critic, visual critic, gameplay critic |
| BFTS node | Candidate/revision state with artifacts and score |

## Design-First Hard Rule

Before map, sprite, Seedance, or Phaser coding begins, create and pass a game design plan. This plan is the game analogue of the AI Scientist template/idea contract.

The design stage must produce:

- `game_design_plan.md`
- `game_design_plan.json`
- `design_critic_round_*.md` or `.json`
- `design_decision_log.md`

Implementation may start only when:

- the plan has a complete player loop,
- the art direction names foreground/background/midground treatment,
- the camera/parallax rules are explicit,
- the runtime object list is testable,
- the critic gives no hard-fail,
- benchmark gates are defined before code exists.

## Minimum Critic Criteria

Score each design from 1 to 10:

- user intent alignment,
- player fantasy clarity,
- core loop clarity,
- level progression,
- ability/enemy design,
- visual identity,
- asset feasibility,
- camera/parallax feasibility,
- benchmarkability,
- production risk.

Hard-fail if:

- the game cannot be finished in one playable level,
- the design depends on untestable visual claims,
- the background/midground/gameplay layer contract is vague,
- generated assets cannot be traced to prompts/provenance,
- no automated path can verify win/restart.

Default pass threshold:

- average score >= 8,
- no category below 7,
- no hard-fail.

