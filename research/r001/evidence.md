# Phase 01 evidence and claim map

Execution date: 2026-10-01. Paper claims here are **source-reported**; we have
not independently replicated their training results. Source/commit hashes are
in the three manifests. Exact definitions, state, groups, numerical ordering and
cost are in `peer-updates.md`; uncertainty and boundaries are in `assumptions.md`.

## Closest evidence cards

| Work / role | Used claim and mechanism | Assumptions / evaluation boundary | Evidence status and falsifier |
|---|---|---|---|
| [SPECTRA v2](https://arxiv.org/html/2603.14315v2), containment | Composite direction subproblem admits the RASP regularizer; actual wrappers pre/post soft-clip existing optimizers | Fixed regularizer convergence theorem; source transformer experiments have different tuning/data budgets | Source-reported containment, directly inspectable §3; kills a claim of a new composite primitive. Does not prove equivalence to its instantiated wrappers |
| [BFO Theorem 3.8](https://fadili.users.greyc.fr/Pub/bibtex/manuscript/higherorderFB.pdf), solver precedent | Diagonal-plus-rank-one metric prox reduces to a unique monotone scalar root; rank-k extension in Theorem 3.4 | Convex proximal problems; numerical examples are not matrix language-model timings | Direct mathematical precedent. RASP scalar solve is a specialization, not a new solver |
| [Markowitz](https://traders.studentorg.berkeley.edu/papers/Markowitz.pdf), bridge | Linear reward minus quadratic covariance risk | Population covariance and portfolio constraints differ from an observed matrix difference and spectral ball | Structure transfer only; no portfolio performance or estimation guarantee transfers |
| [Variance Muon v2](https://arxiv.org/html/2601.14603v2), closest estimator | Temporal coordinatewise variance adapts pre-polar input; post-order variant differs | Source language-model experiments; correlation, drift and finite NS matter; tuning differs from our future protocol | Source-reported, pinned code discrepancy retained. Finding same-weight replica rank-one metric solve would falsify operational distinction |
| [DeVA v2](https://arxiv.org/html/2602.06880v2), geometry | Rotated factorized variance, explicit rotation back | Basis refresh / source implementation order differs from paper; source training comparison is not our study | Paper and code variants retained, no cross-paper ranking |
| [MuCon](https://arxiv.org/html/2605.26459v1), [Musec v2](https://arxiv.org/html/2609.11655v2), clipping | Existing hard/soft spectral clipping and clipped-momentum feedback | Their parameter/state and rational/NS implementations differ; no universal stability disadvantage | Source-reported, γ=0 equivalence formally established for ordinary projection; kills novelty of clipping |
| [Dion3](https://arxiv.org/html/2608.11612v1), resource rival | Selected-row polar updates, residual feedback and optional row normalization; Gram NS | Source distributed/CUDA timing is not TPU evidence; row fractions and code alias preserved | Strong resource rival, no source speed ratio used as our measurement |
| [Muon noise limits](https://arxiv.org/html/2609.32861v1), negative context | Matched-response Gaussian quadratics can favor SGD over polar updates | Restricted quadratic/noise model; does not imply RASP superiority | Source-reported counterweight to assuming orthogonalization is always beneficial |

The registry includes 52 discovered eligible discrete variants, including the
newest source versions and broader families. Their source evaluations are
incomparable in budget/model/data. Phase 03 must establish tensor/state parity;
Phase 04 must match tuning opportunity. Neither has begun.

## Claims and disconfirmation

| ID | Claim | Kind / evidence | Domain and disconfirmation |
|---|---|---|---|
| D1 | Exact matrix direction is the unique constrained quadratic minimizer | Definition + proved: `matrix_exists_unique`, `matrixStep_solves` | μ>0, γ≥0, r≥0, finite rectangular real matrices |
| P1 | Fixed independent directions have calibrated replica disagreement | Proved: `directional_noise_identity` | Finite centered iid law; dependent/unequal replicas invalidate it |
| P2 | Fixed E gives Lipschitz signal response and antitone realized penalty | Proved: `lipschitz_signal`, `disagreement_antitone` | Not adaptive risk or a universal comparative advantage |
| P3 | Coupled constrained solve differs from inverse-then-project | Proved actual matrix example and gap 1/9 | Existence example only; no guarantee every input benefits |
| P4 | Approximate feasible VI bounds objective/distance; roundoff and projection errors propagate | Proved: twelve new declarations in `Approximation.lean`; full map in `formal/README.md` | Numerical primitive must justify error bounds. No verified SVD/bf16 extraction |
| N1 | Specific same-weight split-gradient instantiation appears distinct | Literature inference, finite inspected corpus | Equivalent prior update kills this; absolute primitive novelty is unsupported |
| H1 | Current disagreement orientation helps true progress beyond damping | Hypothesis, frozen Phase 02 experiment | Norm matching and shuffled E; adaptive bias / aligned-noise reversal attacks |
| H2 | Broader covariance can improve rank-one coverage | Hypothesis / oracle diagnostic only | Additional observations and solver work may make it unusable |
| H3 | RASP beats peers on 125M/FineWeb-Edu/TPU | Untested hypothesis | No training, TPU timing or all-peer measurement exists |

## Frontier conclusion

The occupied primitives prevent the requested claim that these primitives have
never been discussed. The supported opportunity is the apparently distinct
instantiation and its measurable use of current noise orientation. Phase 02 can
support or reject that mechanism in named controlled laws. It cannot establish
universal superiority or the later language-model result.
