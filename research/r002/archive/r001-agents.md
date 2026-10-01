# Working on RASP

RASP means Replica-Aware Spectral Proximal optimization. Read `theory.md` for the
current method and `phases/README.md` for phase state, dependencies and gates.
Use `phases/research-record.md` to recover literature decisions and limitations.

## Scope and execution

- The initial task prepares theory, proofs and plans. All experimental phases
  await the user's start instruction. Execute only the requested phase or range.
- Within that scope, research, repair and verify autonomously. Follow the
  failure-and-invalidation process in `phases/README.md`; do not wait for approval
  for ordinary reversible fixes already covered by the request.
- Apply relevant skills under `skills/`. The preparation read all five skills
  and all thirteen reference files. Future tasks should load the relevant skill
  and references, rather than reread everything mechanically.

## Research standards

- Separate definitions, proved claims, measured results and hypotheses. Cite
  primary sources. Check recent competitors before freezing comparisons.
- Preserve failed runs, raw measurements, exact configurations and source
  revisions. Update dependent phases and the paper when a premise changes.
- The target hardware is TPU v4-32 (16 chips). Use JAX/Pallas for planned TPU
  work. Never report CUDA timing as TPU timing or omit communication costs.
- Keep confirmation seeds 42, 43 and 44 out of method selection. Each optimizer
  and each seed receives 2.5B FineWeb-Edu training tokens on the same 125M model.
- Match tuning opportunity and baseline fidelity. An omitted eligible peer
  prevents an “all peers” claim. Do not weaken a gate to obtain a positive result.

## Verification and code

- From `formal/`: `lake build` and `lake env lean Audit.lean`.
- On a fresh checkout: `git submodule update --init --recursive`, then
  `cd formal` and `lake exe cache get`. Keep the Lean and mathlib pins.
- No `sorry`, `admit`, custom `axiom`, `unsafe` proof shortcuts or `native_decide`.
  Update `Audit.lean` and the claim map for new mathematical claims.
- Prove feasibility and existence for the actual matrix operator-norm ball.
  Do not replace a matrix theorem by a scalar analogy or assume the conclusion.
- Later Python code should follow PEP8, have focused comments and meaningful
  numerical tests. Record the formatter/linter and executable commands when
  that code exists; no training commands exist yet.
- Keep data, credentials, caches and checkpoints out of Git. Preserve the
  `skills/` submodule and its independent history.

## Definition of done

A phase has reproducible artifacts, passing stated gates, an updated claim and
failure ledger, and a short handoff. Report what changed, checks run, remaining
risks and the exact state. Do not call a preparation artifact an executed study.

Instruction design follows OpenAI's
[AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md):
keep repository context, commands and working rules concrete and discoverable.
