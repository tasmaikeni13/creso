# Preparation research record

**Date:** 2026-09-25. **Status:** proposal and exact formalization; experiments
unexecuted. This record is separate from the short theory so its contribution
boundary, alternatives and future tests remain auditable.

**Execution addendum, 2026-10-01:** this dated preparation record is preserved.
Phases 01–02 have now executed; [r001](../research/r001/README.md) is the current
evidence. It records 52 comparator variants, approximate certificates, 64 audited
public theorems, 30 Python tests and a fixed controlled study of 98,304 final
contexts. H1 is supported only in the named rotating rank-one law; adaptive
calibration fails, dependent replicas can harm and active solver work is a
serious implementation risk. All training and TPU claims remain open. Do not
read the preparation's historical “unexecuted” statements as current phase state.

## Contract and evidence labels

Target: a matrix update that uses observable gradient uncertainty when choosing a
spectrally bounded direction, with a mathematically specified solver and a
credible path to TPU implementation. The proposed contribution must differ
operationally from existing variance adaptation, spectral clipping and smoothing.

Current outputs are `theory.md`, Lean proofs, nine phase instructions and agent
guidance. No training implementation, Monte Carlo study, TPU measurement or
performance result is part of this preparation. Source-reported experiments
have **not** been independently reproduced here. `proved` below means a Lean
theorem about the stated exact model; `hypothesis` means a future test is needed.

Read before preparation: all five local skills—literature-frontier,
mechanism-transfer, theory-research, ml-research and experimental-research—and
all thirteen files in their `references/` directories. They are preserved in
the pinned `skills/` submodule. OpenAI's AGENTS.md guidance was also consulted.

## Search ledger

Coverage: primary arXiv papers, proceedings, author-hosted manuscripts, official
code and hardware/runtime documentation, searched through 2026-09-25. The search
was breadth first across optimizer families and mathematical mechanisms, then
deepened around the closest operational matches. Search-engine dates were not
treated as publication dates; versions and paper text determine chronology.

| Query family | Sources followed | Decision |
|---|---|---|
| Matrix optimizers, Muon variance, clipping, smoothing, nonconvergence | Muon; Shampoo; SOAP; AdaMuon; Muon-NSR/VS; DeVA; MuCon; SPECTRA; Musec; ARO | Plain smoothing/clipping is occupied; compare recent variants |
| Distributed orthogonal updates and gradient noise scale | Dion family; non-Euclidean noise-scale paper | Replica information and communication awareness have precedents |
| Mean–variance decisions and robust matrix optimization | Markowitz; Goldfarb–Iyengar | Transfer the quadratic decision structure; do not import a robustness guarantee |
| Low-rank metrics and proximal root solving | Becker–Fadili–Ochs | Scalar solver is known mathematics |
| Random-matrix denoising and singular shrinkage | Gavish–Donoho | Attractive alternative, but white-noise/low-rank assumptions are restrictive |
| Filtering, innovation covariance and covariance sketches | Kalman; Frequent Directions | Alternatives for temporal estimates or richer noise coverage |
| TPU v4 topology, JAX/Pallas, FineWeb-Edu | Official Google/JAX/Hugging Face pages | Correct hardware and token-accounting requirements |

Final adversarial query strings included:

- `optimizer "gradient disagreement" "spectral" proximal`
- `optimizer "replica" "rank-one" covariance`
- `"matrix" optimizer "mean variance" proximal`
- `"spectral norm" "rank one" "proximal" gradient noise optimizer`

This pass found SAGE's use of disagreement with spectral perturbations, which
was added to the comparison. Results dominated by financial portfolio tools were
not treated as evidence of an equivalent neural optimizer. The SAGE OpenReview
PDF was blocked; its arXiv full text was read instead. A Markowitz mirror failed;
the Berkeley student-organization mirror worked. Broad absence claims remain
unjustified: code, patents, unpublished work and other terminology may contain
an equivalent instantiation. Refresh the search in Phases 01 and 08.

## Primary evidence ledger

Descriptions identify mechanisms, not verified performance rankings.

| Work and primary source | Evidence inspected and relevance |
|---|---|
| [Muon, official implementation](https://github.com/KellerJordan/Muon) | README/usage and implementation reference. Matrix orthogonalization with auxiliary AdamW; finite Newton–Schulz and scaling must be reproduced faithfully. |
| [Shampoo, Gupta et al. 2018](https://proceedings.mlr.press/v80/gupta18a.html) | Paper's matrix preconditioner construction. Accumulated row/column statistics establish a structured-metric predecessor. |
| [SOAP, Vyas et al.](https://arxiv.org/html/2409.11321v1) | Method section and eigenspace update. Adam in a periodically refreshed Shampoo basis; relevant memory/eigendecomposition comparator. |
| [AdaMuon, Si et al.](https://arxiv.org/html/2507.11005v1) | Sections 3.2–3.3 and Algorithm 1: second moments after orthogonalization, followed by RMS rescaling. |
| [Variance-Adaptive Muon](https://arxiv.org/html/2601.14603v1) | Muon-NSR/VS method equations and variance recurrence. Uses temporal momentum/gradient deviations; a close noise-adaptation precedent. |
| [DeVA](https://arxiv.org/html/2602.06880v1) | Equations 13–15 and Algorithm 2: structured variance estimation and modulation in a matrix basis. |
| [ARO](https://arxiv.org/html/2602.09006v1) | Rotation/update construction and covariance assumptions in the analysis. Norm-aware rotated adaptation is another direction-sensitive predecessor. |
| [MuCon](https://arxiv.org/html/2605.26459v1) | Spectral clipping/projection method and numerical discussion. Establishes that spectral-ball projection alone is not a new optimizer mechanism. |
| [SPECTRA](https://arxiv.org/html/2603.14315v1) | Section 3, composite regularized formulation, pre/post spectral clipping and source noise-spike observations. Its generic regularizer can contain RASP's objective. |
| [Musec and SoftMusec](https://arxiv.org/html/2609.11655v1) | Clipped momentum recurrence, smooth variant and theoretical assumptions. September 2026 competitor that must not be omitted. |
| [Smoothed polar flows](https://arxiv.org/html/2608.01911v1) | Smooth spectral potential and continuous-time analysis. A flow theorem is not automatically a discrete stochastic guarantee. |
| [Non-Euclidean gradient noise scale](https://arxiv.org/html/2602.03001v1) | Distributed local-gradient variance estimation and batch adaptation. Reusing replica gradients is established prior practice. |
| [Dion/NorMuon official repository](https://github.com/microsoft/dion) | Official method descriptions and code pointers; distributed cost and row-adapted orthogonal updates require comparison. |
| [Dion3](https://arxiv.org/abs/2608.11612) | Abstract/official-code discovery only. Full algorithm fidelity is a Phase 01/03 task; no theorem from it is used here. |
| [OptMuon](https://arxiv.org/abs/2606.08783) | Abstract-level discovery of scalar trajectory adaptation; inspect its full algorithm before registry freeze. |
| [SAGE](https://arxiv.org/html/2605.07914v1) | Section 3/algorithm description: polar SAM-style perturbation and isotropic Gaussian noise scaled by cross-distribution disagreement. No equivalent RASP quadratic solve appears in that construction. |
| [Becker–Fadili–Ochs, 2019](https://fadili.users.greyc.fr/Pub/bibtex/manuscript/higherorderFB.pdf) | Theorem 3.8 and scalar root discussion: diagonal-plus-low-rank proximal metrics reduce to a strongly monotone root problem. This is the closest solver precedent. |
| [Markowitz, 1952](https://traders.studentorg.berkeley.edu/papers/Markowitz.pdf) | Expected return, covariance and feasible allocation tradeoff, especially pp. 80–82. Supplies a decision structure; portfolio constraints and statistical assumptions do not transfer automatically. |
| [Gavish–Donoho, optimal singular shrinkage](https://arxiv.org/pdf/1405.7511) | Signal-plus-white-noise asymptotic model and loss-specific shrinkers. The model assumptions, rather than the existence of a shrinker, are the transfer bottleneck. |
| [Kalman, 1960](https://www.cs.cmu.edu/~./motionplanning/papers/sbp_papers/k/Kalman1960.pdf) | State/error-covariance formulation and filtering construction. A candidate for distinguishing temporal drift from observation noise, requiring a credible gradient-state model. |
| [Frequent Directions, author note](https://edoliberty.github.io/papers/simplefd.pdf) | Covariance update and deterministic sketch bound. Supplies a richer-noise alternative with additional state and decomposition work. |

Other discovery leads include robust portfolio uncertainty
([Goldfarb–Iyengar](https://pubsonline.informs.org/doi/abs/10.1287/moor.28.1.1.14260)),
scalar auxiliary-variable optimizer constructions, and recent Muon convergence
counterexamples. They were not used as uninspected theorem premises. In particular,
a squared risk penalty is not asserted to equal a worst-case ellipsoidal
uncertainty objective.

## Breadth-first mechanism portfolio

The target interface is `(matrix signal, uncertainty observations) → bounded
matrix update`, with same-step observability and an implementable solver.

| Branch | Source mechanism → target relations | Assumptions lost or needed | Prediction / kill test | Decision |
|---|---|---|---|---|
| Mean–variance allocation | Expected return → predicted descent; allocation → vectorized update; covariance risk → directional gradient uncertainty; feasible portfolios → spectral ball | Gradient noise changes with weights; covariance estimate can be poor; no positivity/simplex allocation constraint | Real disagreement should beat shuffled disagreement at matched update norm; kill if adaptive bias dominates | Selected structure |
| Low-rank proximal geometry | Isotropic-plus-low-rank metric → one observed noise direction; metric projection → coupled spectral constraint; scalar root → feedback variable | Exact projection oracle or certified approximation is required | Root step must agree with independent constrained minimization; wrong post-projection order fails the 2×2 case | Selected solver, prior art credited |
| Random-matrix denoising | Signal singular values hidden in white noise → trustworthy gradient modes → singular shrinker | Gradient noise need not be white or signal low-rank; estimating noise scale is difficult | Test anisotropic/rotating noise; kill naive transplant when calibration collapses | Reserve alternative |
| State estimation | Latent state → true gradient; innovation → observed gradient minus prediction; covariance gain → adaptive trust | Parameter movement causes signal drift; a temporal difference conflates drift and observation noise | Abrupt drift should distinguish temporal estimate from simultaneous split estimate | Reserve; simultaneous replicas chosen |
| Streaming covariance sketches | Streaming outer products → noise covariance observations; sketch directions → low-rank metric | Several noise directions cost memory and more-dimensional solves; stale directions may hurt | Gain from richer coverage must pay for extra communication/state | Reserve if rank-one coverage fails |
| Smooth spectral potentials | Regularized matrix map → bounded, continuous direction near small singular values | Many such methods already exist; ODE stability does not certify discrete training | γ=0 establishes how much benefit comes from ordinary regularization | Required control, insufficient novelty alone |
| Robust uncertainty sets | Ambiguity in returns → gradient uncertainty set; robust support penalty → conservative update | Squared quadratic penalty differs from a norm support function; uncertainty-set calibration needed | Adversarial noise test can discriminate robust versus mean–variance objectives | Rejected as an exact interpretation of RASP |

### Selected relational bridge

At a fixed parameter state, two equal iid minibatch means provide a common signal
and an observable disagreement. A fixed candidate direction turns matrix noise
into a scalar projected fluctuation. The squared disagreement is calibrated for
that fixed direction, while the linear term rewards predicted descent. An
isotropic quadratic gives a unique minimizer, and the operator-norm ball limits
the matrix action. The low-rank metric couples that choice to the disagreement
through a scalar feedback root.

The bridge preserves decision variable, uncertainty direction, quadratic cost
and feasible-set relations. It does **not** preserve a portfolio's financial
interpretation, a Kalman model, a population covariance estimate, or risk
unbiasedness after direction selection. Two gradient means need not cost two
full batches, but their reduction/storage costs are real. Treat μ and γ as
dimensioned parameters; loss rescaling changes their calibration.

## Adversarial novelty comparison

| Closest predecessor | Shared content | Proposed residual delta / unresolved issue |
|---|---|---|
| MuCon / smooth spectral maps | Regularized bounded spectral update | Specific simultaneous-disagreement metric is added; clipping/smoothing is not the contribution |
| Muon-NSR/VS | Noise-aware adaptation | Different noise observation and coupled feasible minimizer; advantage over temporal statistics is untested |
| AdaMuon / DeVA / ARO | Direction-dependent variance or geometry adaptation | RASP uses one vectorized disagreement direction in its constrained objective; richer peers may win |
| SPECTRA | General regularized spectral optimization | Contains the objective at framework level. Only a particular estimator/regularizer instantiation and its implementation could be a contribution |
| Non-Euclidean noise-scale adaptation | Simultaneous distributed-gradient information | Chooses update direction at fixed global batch rather than adapting batch size |
| SAGE | Disagreement information plus spectral geometry | SAGE constructs a perturbation and injects isotropic noise; RASP penalizes a direction in a convex per-step solve |
| Becker–Fadili–Ochs | Rank-one proximal reduction and scalar root | Solver theorem is an application of prior work; no solver novelty claim |

**Current claim:** no equivalent instantiated RASP update was found in the
inspected corpus. A general framework already contains its objective. This is a
candidate algorithmic composition, not a certification that it is “completely
new.” A publication claim requires the refreshed search, useful implementation,
and discriminating empirical evidence.

## Hypotheses, rival explanations and failure ledger

| ID | Status | Claim or failed branch | Discriminating evidence / action |
|---|---|---|---|
| T1 | Proved | A unique spectrally feasible exact matrix step exists | `matrix_exists_unique`, `matrixStep_feasible` |
| T2 | Proved | Fixed-disagreement signal stability and alignment | `firm_stability`, `lipschitz_signal`, `alignment`; no changing-noise claim |
| T3 | Proved, limited | Finite iid fixed-direction noise identity | `directional_noise_identity`; adaptive direction and momentum excluded |
| T4 | Proved, prior mathematics | Coupled scalar solver and exact-projection stopping bound | `exists_root`, `root_unique`, `feedback_error_bound` |
| F1 | Rejected | Precondition then Euclidean-project is the same update | Actual 2×2 proof gives an objective gap of 1/9 |
| F2 | Rejected novelty branch | Plain clipping/smoothing is a new optimizer | MuCon, SPECTRA, Musec and smooth-polar literature |
| F3 | Rejected claim extension | Fixed-direction unbiasedness establishes risk unbiasedness for the selected update | The selected direction depends on the samples; independent evaluation required |
| H1 | Open | Useful noise information improves expected progress beyond damping | RASP versus shuffled E, random E, γ=0 and norm-matched controls |
| H2 | Open | One noise direction is enough to justify its cost | Anisotropic multi-direction noise versus richer covariance controls |
| H3 | Open | Coupled solve can compete on TPU elapsed time | Count/profiling of projections and collectives, including communication control |
| H4 | Open | Quality/cost match or exceed every registered peer | Full frozen 125M/2.5B/three-seed study, with uncertainty |

Principal risks: finite-sample adaptive bias; signal/noise correlation; stale
momentum; rank-one covariance coverage; loss/shape scaling; expensive repeated
projections; bf16 errors around clipping thresholds; unequal masked batches;
overfitting HPO or held-out seeds; limited power with only three seeds.

## Prepared verification and future evidence

The Lean sources prove the displayed theory for finite real rectangular matrices,
with separate Frobenius and operator norms. Build and axiom checks are documented
in `formal/README.md`. They certify mathematical statements, not an executable
SVD, stochastic training trajectory, implementation speed or novelty.

The next discriminating work is Phase 01's current-frontier and approximation
audit, followed by Phase 02's controlled falsification. No Monte Carlo outcomes,
training curves or TPU throughput have been invented to fill the plan.

Planning sources: [TPU v4](https://docs.cloud.google.com/tpu/docs/v4),
[Pallas TPU](https://docs.jax.dev/en/latest/pallas/tpu/quickstart.html),
[FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu), and
[OpenAI AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
