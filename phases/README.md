# Research execution guide

These are nine research phases. The initial theory, source review and Lean
verification are preparation artifacts. The user authorized phases 01 and 02
on 2026-10-01. No training pilot or TPU run has started.

## Objective and fixed requirements

Develop a defensible matrix optimizer that matches or exceeds every eligible
peer under a frozen comparison protocol. The required confirmation experiment:

- One identical 125M-parameter language model for all methods.
- FineWeb-Edu, **2,500,000,000 training tokens per optimizer per seed**.
- Three seeds: **42, 43, 44**. Each optimizer therefore uses 7.5B tokens.
- Google Cloud **TPU v4-32**, containing **16 v4 chips**.
- Report quality, time, memory, numerical reliability and tuning cost separately.

“All peers” means every eligible method in the dated Phase 01 registry, including
the newest relevant competitors found before the registry freezes. It is not a
universal mathematical guarantee. If an eligible baseline is missing, mark the
objective unmet. Published or statistically defensible negative results must
remain visible; do not iterate by selecting lucky seeds or weakening baselines.

## State and dependencies

| Phase | Work | Depends on | State |
|---|---|---|---|
| [01](01-mathematics.md) | Frontier, definitions and formal analysis | Preparation | Passed |
| [02](02-falsification.md) | Mathematical attacks and statistical simulations | 01 | Running |
| [03](03-reference-implementations.md) | CPU reference methods and correctness | 01–02 | Not started |
| [04](04-protocol.md) | Data, 125M model and preregistered protocol | 01–03 | Not started |
| [05](05-tpu-kernels.md) | TPU implementation and numerical certification | 03–04 | Not started |
| [06](06-pilots-and-selection.md) | Fair tuning, pilots and mechanism ablations | 02–05 | Not started |
| [07](07-confirmation.md) | Frozen competitive training | 01–06 | Not started |
| [08](08-analysis.md) | Statistics, replication and claim audit | 07 | Not started |
| [09](09-publication.md) | Paper, repository cleanup and release | 01–08 | Not started |

Use the states `not_started`, `running`, `passed`, `failed`, `invalidated`, and
`blocked`. On starting Phase 01, create `phases/state.json` with the revision,
phase states, artifact paths and gate results. This table and that file must agree.
Use immutable revision IDs such as `r001`; create new IDs when the method or
protocol changes. Do not manufacture completion records retroactively.

## Autonomous correction loop

Within the requested phase scope:

1. Read its inputs and current failed gates. Write the hypothesis, alternatives,
   smallest discriminating check, expected evidence and stop condition.
2. Verify the evaluator before using it to select a method. Execute the smallest
   check that can falsify the proposed explanation; save inputs and raw outputs.
3. Diagnose failures: theorem, estimator, numerical method, implementation,
   baseline fidelity, data, infrastructure, statistical power or hypothesis.
   Search primary literature when the current explanation is inadequate.
4. Repair the responsible layer. For a theory failure, revise the definition or
   assumptions, prove the replacement, and rerun its counterexamples before
   changing the kernel or scaling training. Archive the rejected branch.
5. Trace every downstream dependency. Mark affected artifacts invalidated;
   rewrite dependent phase instructions, `theory.md`, claim map and any paper.
   A passing stale result does not validate a changed method.
6. Recheck the failed gate and directly affected gates. Stop optional checks once
   evidence is sufficient. Continue useful work within the requested scope.
7. At a phase boundary, provide a concrete handoff and await the next requested
   phase. A failed gate may require an earlier phase to be reopened; report that
   dependency instead of silently launching work beyond the requested range.

No finite experiment can force a method to beat every competitor. Iterate toward
the objective while evidence supports a promising branch. If the hypotheses are
falsified, record the failure and propose a replacement. If the available compute
or statistical power cannot resolve the question, say so. Never label a failed
or inconclusive comparison as success.

## What invalidates what

| Change | Minimum invalidation |
|---|---|
| Objective, estimator, momentum, scaling or assumptions | 01–09 |
| CPU algorithm or baseline fidelity bug | 03 and affected 04–09 |
| Dataset split, tokenization, model, metric or tuning budget | 04–09 |
| Kernel/collective bug affecting arithmetic | 05–09; reference checks in 03 |
| Hyperparameter selection after seeing confirmation | 06–09; new confirmation revision |
| Infrastructure interruption with exact resumable state | Affected run only; preserve logs |
| Formatting/prose correction without semantic change | Affected documents only |

Check the actual dependency graph; this table is a lower bound. A failed full run
is evidence about that revision. Preserve it even if the next revision succeeds.

## Research records

Create artifacts as their phases execute, under `research/<revision>/`:

- `contract.md`, source/query ledger, dated competitor registry and claim map.
- Hypothesis portfolio with predictions, rival explanations and kill criteria.
- `failures.jsonl`: ID, phase, inputs, symptom, diagnosis, repair, invalidations.
- Immutable configs, code/dependency hashes, environment manifest, run IDs,
  commands, raw metrics and checkpoint manifests.
- Phase handoff: checks, results, uncertainty, gates and remaining limitations.

Large data/checkpoints belong in durable external storage, with locations and
checksums in Git. Raw evidence is never overwritten to make a graph look better.
The [preparation research record](research-record.md) is the starting ledger;
all reported source performance there is unreplicated in this repository.
