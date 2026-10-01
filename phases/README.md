# CRESO research phases

The active revision is **c001**. Phases 01–02 cover literature, mathematical and
formal verification, numerical attacks and statistical simulations. No TPU or
language-model training phase has started. See `state.json` for live gate results
and `research/c001/README.md` for executed artifacts.

## Objective and comparison requirements

Develop a substantial optimizer contribution with rigorous uncertainty control,
useful updates and credible cost. Novelty and impact must be earned by evidence.
The future confirmation contract is one identical 125M model, FineWeb-Edu,
**2,500,000,000 training tokens per optimizer per seed**, seeds **42, 43, 44**,
on **TPU v4-32 (16 chips)**. Use JAX/Pallas. Report quality, time, memory,
reliability and tuning cost separately. An all-peer claim requires every eligible
variant, including **Muon**, in the dated registry and no omitted stronger variant.

## Dependencies and execution state

| Phase | Work | Dependencies | State |
|---|---|---|---|
| [01](01-mathematics.md) | Frontier, mechanism and formal theory | Research contract | Passed |
| [02](02-falsification.md) | Numerical and statistical attacks | 01 definitions | Passed |
| [03](03-reference-implementations.md) | Complete optimizer references and parity | 01–02 | Not started |
| [04](04-protocol.md) | Model, data and preregistered comparisons | 01–03 | Not started |
| [05](05-tpu-kernels.md) | TPU kernels and numerical certification | 03–04 | Not started |
| [06](06-pilots-and-selection.md) | Fair tuning and pilot ablations | 02–05 | Not started |
| [07](07-confirmation.md) | Frozen competitive training | 01–06 | Not started |
| [08](08-analysis.md) | Statistical replication and claim audit | 07 | Not started |
| [09](09-publication.md) | Paper, cleanup and release | 01–08 | Not started |

Only requested phases execute. States are `not_started`, `running`, `passed`,
`failed`, `invalidated`, `blocked`; the table and machine state must agree.
A phase's narrower gate can pass while the breakthrough or all-peer objective
remains unmet. State that distinction in the handoff.

## Correction and invalidation

1. State the hypothesis, rival explanation, discriminating check and stop rule.
2. Verify the evaluator, then preserve exact inputs and raw outputs.
3. Diagnose theory, assumption, baseline, numerical, data or infrastructure failures.
4. Repair the responsible layer within scope; reprove changed mathematics.
5. Invalidate dependencies and update theory, instructions, claims and paper.
6. Use a new revision and untouched final draws for a substantive method/protocol
   change. Retain negative results. Never retune on confirmation seeds or relax gates.
7. Stop optional searches when enough evidence exists. Handoff at the authorized
   phase boundary; do not silently launch additional training phases.

| Change | Minimum affected phases |
|---|---|
| Decision rule, covariance envelope, sample reuse or assumptions | 01–09 |
| Reference/baseline fidelity defect | 03 and affected 04–09 |
| Model, dataset, token budget, metric or tuning budget | 04–09 |
| Kernel or collective arithmetic defect | 05–09, reference checks in 03 |
| Selection after viewing confirmation | 06–09, fresh confirmation required |
| Formatting or naming with identical semantics | Documentation/provenance only |

Each revision keeps its contract, source and query ledger, registry, claim map,
hypotheses, failure ledger, immutable protocol, commands, environment, source
hashes, raw manifest and phase handoff. Large data stay outside Git with durable
locations and checksums. No finite study can force success against every peer.
