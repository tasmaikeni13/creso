# Lean formalization

The exact RASP specification and every numbered equation/guarantee in
[`theory.md`](../theory.md) are represented here. Bibliographic novelty and
empirical performance are not mathematical theorems.

## Build and audit

From this directory, with elan installed:

```bash
lake exe cache get
lake build
lake env lean Audit.lean
```

- Lean: `leanprover/lean4:v4.34.0-rc2`.
- mathlib: `7974e751bece493b6ff508039423ca9fa2452fa8`.
- All transitive dependency commits are pinned in `lake-manifest.json`.
- `Audit.lean` prints the axiom dependencies of every public theorem and the
  mathematical matrix-step definition. Accept only Lean's standard `propext`,
  `Classical.choice`, and `Quot.sound`, or no axioms. There are no project axioms,
  admitted proofs, `native_decide` proofs or unsafe shortcuts.

The preparation build and axiom audit passed on 2026-09-25: **49 public theorems
plus `matrixStep`**, using only the three standard axioms listed above. All nine
dependency checkouts matched their pinned commits and had no local edits.
Local `.lake` caches are excluded from Git. A fresh checkout obtains the pinned
dependencies and their caches; no absolute local path is required by the package
configuration.

## Claim-to-declaration map

All names below are in the namespace `Rasp`.

| Theory item | Formal content | Declarations / source |
|---|---|---|
| Eq. (1), initialization and update | Mean, difference, uncorrected momentum, zero initialization, parameter subtraction; cancellation of the shared signal | `halfMean`, `halfDifference`, `momentum`, `momentumSequence_zero`, `momentumSequence_succ`, `parameterUpdate`, `centered_split` in [Algorithm.lean](Rasp/Algorithm.lean) |
| Eq. (2), Frobenius quadratic | Objective, residual, exact minimization and quadratic expansion | `objective`, `residual`, `Solves`, `objective_expansion` in [Core.lean](Rasp/Core.lean) |
| Covariance rank statement | The operator sends D to the inner product of E and D times E; its quadratic is the squared disagreement and its rank is at most one, including E=0 | `noiseOperator`, `noiseOperator_quadratic`, `noiseOperator_rank_le` in Core |
| Actual matrix geometry | Finite rectangular entries with Frobenius inner product; induced Euclidean operator as a continuous linear map; convex compact spectral ball | `Mat`, `matrixEquiv`, `asOperator`, `frobenius_inner`, `spectralBall_convex`, `spectralBall_compact` in [Matrix.lean](Rasp/Matrix.lean) |
| Eq. (2), existence/uniqueness/feasibility | All dimensions, radius ≥0, μ>0, γ≥0, arbitrary signal/disagreement | `matrix_exists_unique`, `matrixStep_solves`, `matrixStep_feasible` in Matrix |
| Eq. (3), finite iid noise | Nonnegative finite weights summing to one; zero weighted directional mean; independent joint mass p(i)p(j) | `iid_split_second_moment`, `directional_noise_identity` in [Statistics.lean](Rasp/Statistics.lean), together with `centered_split` |
| Eq. (4) | Minimization iff the variational inequality, proved from convex line segments and objective expansion | `solves_vi`, `vi_solves`, `solves_iff_vi` in Core |
| Alignment and zero signal | Zero must belong to the feasible set; uniqueness uses μ>0 | `alignment` in Core; `zero_signal` in [Descent.lean](Rasp/Descent.lean) |
| Eq. (5) | Two VI solutions for fixed E, μ, γ and feasible set; no singular gap premise | `firm_stability`, `lipschitz_signal` in Core |
| More disagreement penalty | For strictly larger γ and fixed other inputs, squared realized disagreement cannot increase | `disagreement_antitone` in Core |
| Replica-swap invariance | E and −E define the same quadratic and exact minimizer | `disagreement_sign_invariant` in Algorithm |
| Eq. (6) | Conditional one-step upper bound, with explicit loss upper-model and signal-error hypotheses | `descent_upper_model` in Descent |
| Eq. (7), projection and root | Euclidean projection specification, equivalence to isotropic minimization, both directions of the root/solution connection | `project_minimizes_distance`, `isotropicStep_eq_project`, `root_solves`, `solution_is_dualStep` in [Solver.lean](Rasp/Solver.lean) |
| Eq. (7), solvability/certificate | A root exists, is unique, has the stated monotonicity bound, and gives the exact-projection error certificate | `exists_root`, `root_unique`, `feedback_strong_mono`, `feedback_error_bound` in Solver |
| 2×2 noncommutation example | Full matrix feasibility and constrained optimality, unconstrained optimality, Euclidean projection optimality, objective gap 1/9 | `counterexample_optimal`, `counterexample_unconstrained`, `counterexample_projected`, `counterexample_gap` in [Examples.lean](Rasp/Examples.lean) |

The example's Euclidean projection is expressed as `Solves K 1 0 X 0 C`;
`project_minimizes_distance` and uniqueness connect that predicate to the
Frobenius-distance definition. It is not a scalar-only analogy.

## Assumptions and limits

`Mat m n` is Euclidean space indexed by `Fin m × Fin n`; it is linearly
identified with an actual rectangular matrix and its action on Euclidean
vectors. The ambient norm is Frobenius. The constraint norm belongs to the
associated operator. These norms cannot be silently interchanged by a scoped
matrix norm instance.

The variational core is proved in a real inner product space. The concrete
matrix wrapper discharges nonemptiness, convexity and compactness instead of
assuming matrix existence as an axiom. The finite statistics theorem assumes
zero mean in the tested fixed direction; a centered vector distribution supplies
that assumption for each direction. It does not cover dependent replicas,
infinite-support laws, adaptive direction selection, or momentum covariance.

`isotropicStep`, `project` and `matrixStep` use classical choice to specify exact
minimizers. They are **noncomputable definitions**. This development does not
claim to extract a numerical optimizer, verify an SVD implementation or certify
bf16 arithmetic. The solver stopping bound assumes an exact projection.

The descent theorem assumes a quadratic upper model for the actual loss at the
proposed step and an explicit bound on signal error. No global neural-network
smoothness, stochastic convergence, generalization, speed or memory advantage is
proved. Peer algorithms are cited context; their formal comparative analysis is
planned in Phase 01.
