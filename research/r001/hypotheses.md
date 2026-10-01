# Mechanism portfolio and transfer cards

Frozen before simulation. Sources and the original relation map are in the
preparation record; this execution audits their operational predictions.

| Branch | Reconstruction and source | Prediction | Rival / kill criterion |
|---|---|---|---|
| H1 coupled replica metric (selected) | Markowitz quadratic directional risk; BFO low-rank metric proximal solve; `(M,E)→argmin Q` | In a rotating anisotropic finite-variance noise regime, real E improves independent quadratic progress at identical update norm | Damping alone: improvement vanishes after norm matching or shuffled E works equally well; kill intended regime if fixed experiment excludes the predefined benefit |
| H0 plain spectral regularization | μ quadratic, γ=0; SPECTRA/MuCon precedents | Spectral clipping alone explains gains in heavy-tail magnitude regimes | No uncertainty information needed; null in deterministic E=0 case |
| H2 richer covariance sketch | Several vectorized disagreement directions, PSD sketch metric; Frequent Directions / BFO rank-k precedent | Better coverage than one observation under high-dimensional anisotropic noise | Extra observations/state/solver cost overwhelm gain; no new algorithm selected here |
| H3 only update magnitude | Scalar damping of γ=0 direction; NAMO/OptMuon magnitude precedents | Tuned η or matched norms remove the benefit | A directional benefit at matched norm and against shuffled E rejects this explanation locally |

## Selected transfer

**Socket:** identify unreliable matrix update components using simultaneous
observations at fixed weights while preserving spectral feasibility.
**Domain-neutral bridge:** choose d in a compact convex set to maximize linear
reward minus an isotropic quadratic and a squared observed uncertainty loading.
**Relations:** predicted return↔<M,D>; allocation↔vectorized matrix D;
directional risk↔<E,D>²; feasible allocation↔operator ball. The portfolio simplex
and a population covariance are not transported. One observation is rank one
in vectorized space even when E is a full-rank matrix.

**Observability adapter:** two equal iid group means from the same global token
batch. Their difference cancels the shared signal. The fixed-direction variance
identity supplies calibration; no adaptive-risk conclusion crosses that bridge.
**Timescale mismatch:** current disagreement is not stationary momentum noise.
**Units mismatch:** μ and γ require explicit scaling. **Solver adapter:** a
metric projection requires a coupled root; unconstrained inversion followed by
Euclidean clipping violates the 2×2 example. **Cost mismatch:** repeated matrix
projections and another communication channel require later profiling.

**Intervention:** scramble the uncertainty direction while preserving its norm
and marginal distribution; normalize both updates to the same Frobenius norm
within the spectral ball; independently evaluate expected progress. A positive
effect in this constructed law is mechanism evidence, not validation for LLMs.

## Ranked opportunity tickets

1. H1, current uncertainty orientation: smallest test is a fixed-context iid
   two-draw quadratic attack with context-dependent noise orientation; strongest
   failure is adaptive selection or noise aligned with signal. An existing
   same-observation, same-objective, same-constraint instantiation kills novelty.
2. H2, richer coverage: compare rank-one suppression to unattainable population
   covariance under broad noise. Do not invent a sketch method unless this
   diagnostic identifies a missing capability worth its cost.
3. Certified cheap projection: count projections, distinguish inactive fast
   paths from active constraints, and carry explicit numerical error. The solver
   mathematics is prior work; a useful TPU implementation remains open.
