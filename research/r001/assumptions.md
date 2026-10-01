# Definition, units and assumption audit

The frozen optimizer is equations (1)–(2) of `theory.md`, with no bias correction,
no hidden RMS rescale, and real rectangular matrices. Let N=mn and q=min(m,n).
μ>0, γ≥0, r≥0, 0≤β<1, η≥0. D has update-direction units, M and E have
gradient units; μ has gradient/direction units and γ has inverse
(gradient × direction) units. A loss multiplier with fixed μ,γ changes the
algorithm. All statements below distinguish the Frobenius ambient norm from the
induced Euclidean matrix operator norm.

| Case | Exact specification / consequence | Formal evidence / attack |
|---|---|---|
| Arbitrary rectangular, including empty dimensions | Compact convex actual operator ball; unique minimizer | `matrix_exists_unique`; no rank premise |
| M=0 | D=0 | `zero_signal` |
| E=0 or γ=0 | Isotropic spectral-ball projection of M/μ | `zero_penalty_eq_projection` |
| Rank deficiency / repeated singular values | Unique D; no singular gap required | Existence and strong convexity; a numerical SVD remains a separate contract |
| r=0 | Only the zero operator, hence zero matrix, is feasible | `mem_spectralBall`, injective `asOperator`; tested in Phase 02 |
| Small/large gradient magnitudes | Well-defined exact step; scalar arithmetic may overflow | Scale sweeps, with no scale-invariance claim |
| E changes with M | Equation (5) is inapplicable | Counterexamples / independent evaluation; do not condition on E and assume iid noise remains iid |
| Replica swap | E changes sign; D unchanged | `disagreement_sign_invariant` |
| Non-Gaussian finite support | Fixed-direction identity holds for centered iid halves | `directional_noise_identity`; adaptive direction excluded |
| Infinite-support finite variance | Finite theorem does not formalize measure theory | Simulation laws explicitly have finite second moments; no Lean expectation extension claimed |
| Unequal/correlated halves | Identity can fail | Exact finite enumeration and deliberately misspecified simulations |
| Momentum β>0 | M includes earlier gradients and deterministic initialization bias | Raw E estimates current G noise, not M noise; stationary diagnostic separately measures both |
| Weight decay and nonmatrix groups | Outside exact theorem | Phase 03 must specify these; no training implementation here |

## Approximate solver contract

For a feasible approximate step U define an ε-VI by
`<residual(U), V-U> ≥ -ε` for every feasible V. Lean proves both
`Q(U)-Q(D*) ≤ ε` and `μ ||U-D*||F² ≤ ε`.
If the computed residual has norm error ≤τ and feasible distances from U are ≤R,
a checked ε-VI for that residual gives an `(ε+τR)`-VI for the true residual.
This covers roundoff only when τ is independently bounded; a reported float
residual alone is not a rigorous interval certificate.

If P is the exact projected dual step, `||U-P||F ≤ εp`, and the true scalar
residual `|z-γ<E,U>| ≤ εf`, Lean proves

```
μ ||U-D*||F ≤ μ εp + (εf + γ ||E||F εp) ||E||F.
```

A computed scalar residual with error δf uses εf=|computed residual|+δf.
The theorem does not assume U is feasible. Independently bound its actual
operator norm by b>0 and repair with `min(1,r/b) U`; `radial_feasibility`
proves feasibility over the actual rectangular matrix ball. Include the repair
distance in εp before certifying accuracy. A Frobenius upper bound is safe but
may be unnecessarily conservative. A point estimate of the largest singular
value is insufficient for a formally certified b.

For exact projection, F is strongly increasing, its root is bracketed by
±|F(0)|, and exact sign-preserving bisection has width w0/2^k. Lean proves the
midpoint direction error bound `μ ||D(mid)-D*||F ≤ width ||E||F/2`.
Choose a finite iteration limit from this bound and the desired tolerance.
With inexact projections, require sign intervals excluding zero before updating
a bracket; otherwise refine or use the residual certificate. Do not assume exact
bracket signs for an approximate matrix kernel. If requested tolerance lies
below the certified arithmetic floor, return failure with the residuals.

## Dependency and proof boundaries

`Core` → `Solver` → `Matrix` → `Approximation`. Matrix existence is discharged
by compactness and convexity, not supplied as a conclusion. Approximation uses
the existing VI, exact-projection certificate and Cauchy–Schwarz. The zero-penalty
comparison is also a peer stability lemma: ordinary spectral projection already
has the fixed-signal Lipschitz guarantee. No proof of superiority, adaptive-risk
unbiasedness, stochastic convergence, a numerical SVD, or bf16 error bounds is
claimed. Phase 02 evaluates numerical contracts empirically; Phase 05 must
independently certify the actual TPU primitives.
