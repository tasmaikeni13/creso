# CRESO Lean formalization

The project verifies exact matrix decision geometry and conditional finite-law
statistics. Novelty and measured performance are not mathematical theorems.
There are **47 public theorems**, all listed in `Audit.lean` and the executable
claim map at `research/c001/claim-map.json`.

## Build and audit

```bash
lake exe cache get
lake build
lake env lean Audit.lean
```

Lean is `leanprover/lean4:v4.34.0-rc2`; mathlib is pinned to
`7974e751bece493b6ff508039423ca9fa2452fa8`. All nine dependency pins remain in
`lake-manifest.json`. Accept only standard `propext`, `Classical.choice`,
`Quot.sound`, or no axioms. No admitted proof, project axiom, unsafe shortcut or
`native_decide` is allowed. See the saved build, audit and formal-checks artifacts.

## Claim map

All declarations use namespace `Creso`.

| Theory claim | Exact formal result | Module / declarations |
|---|---|---|
| Actual rectangular geometry, Eq. 1 | Frobenius matrix space is identified with an actual Euclidean linear operator; convex compact operator-norm ball, including zero | Geometry: `matrixEquiv`, `asOperator`, `mem_spectralBall`, `spectralBall_convex`, `spectralBall_compact`, `zero_mem_spectralBall`, `frobenius_inner` |
| Feasible vertices | Certified norm bound and radial guard produce actual matrix-ball feasibility for arbitrary matrices; zero and three guarded vertices are feasible | Geometry: `radial_feasibility`; Core: `radialMatrix_feasible`, `guardedLibrary_feasible` |
| Mixture geometry | Every convex interpolation of feasible matrices remains in the actual operator ball | Core: `mix_feasible`, `mix_zero`, `mix_one` |
| Exact segment solver, Eqs. 8–9 | Quadratic expansion, endpoint/degenerate handling, clipped fraction maximizes each segment | Core: `progress_mix`, `certificate_quadratic`, `bestFraction_mem`, `bestFraction_maximizes`, `segment_optimal` |
| Existence of the matrix decision | A finite maximum exists; the guarded four-matrix library has a feasible pair/fraction maximizing every feasible segment | Core: `exists_finite_best`, `exists_matrix_decision`, `exists_guarded_matrix_decision` |
| Uniform certificate and oracle inequality, Eq. 10 | Explicit vertex error bounds imply valid certificate for arbitrary interpolation and selected-vertex regret ≤2b+solver error | Core: `uniform_certificate`, `vertex_certificate_error`, `selected_oracle_bound`, `selected_nonnegative_progress` |
| Conditional descent | A specified quadratic upper model and nonnegative learning rate imply certificate-based descent | Core: `certified_descent` |
| Chebyshev and simultaneous errors | Nonnegative finite masses, explicit second moments and positive thresholds; no success event is assumed | Statistics: `finite_chebyshev`, `finite_union_bound`, `simultaneous_moment_bound` |
| Trace calibration, Eqs. 3–4 | Relative error gives upper trace; failure mass follows from a variance premise; zero trace is handled exactly on positive support | Statistics: `relative_trace_upper`, `trace_upper_failure_mass`, `zero_trace_exact` |
| Covariance envelope, Eq. 5 | Squared-sum inequality and Cauchy–Schwarz give the two-trace bound; component inner-product decomposition is explicit | Statistics: `squared_sum_envelope`, `finite_split_envelope`, `finite_inner_trace_bound`, `finite_directional_envelope` |
| Sample mean variance | Pairwise zero cross moments and per-replica second moment bound imply v/n for a finite average | Statistics: `finite_sum_second_moment`, `finite_mean_second_moment` |
| Adaptive selection after calibration | Union of calibration and true-threshold mean failures controls arbitrary validation-dependent indices/fraction; no independence between these two events is assumed | Statistics: `two_stage_failure_bound`, `adaptive_certificate_failure_mass` |
| Signal recovery | Exact projector conditions Pg=0 and Pξ=ξ imply deflation recovers g; those conditions are not assumed for general replicas | Core: `deflation_recovers_signal` |
| Active Muon comparison and interpolation gain | Exact 2×2 progress gap 1/8, actual feasibility, and strict benefit of a matrix mixture | Core: `active_matrix_muon_gap`, `active_matrix_candidates_feasible`, `strict_matrix_interpolation_gain` |
| Required independence | A common-noise matrix direction has a positive false certificate and negative true progress | Core: `dependent_matrix_certificate_counterexample` |

## What these proofs do and do not establish

The matrix norm in the constraint is the associated operator norm, while the
ambient norm is Frobenius. The distinction is enforced by separate types.
Existence is proved by finite maximization and feasible interpolation; it is
not an assumed optimizer or a scalar replacement for matrix geometry. The
feasible set searched is a finite union of segments, not the entire operator ball.

The guarded library accepts arbitrary proposed matrices and proves radial
feasibility. Its ideal polar input has norm ≤r by the mathematical SVD identity;
that identity and the numerical SVD are **not mechanized here**. Kernel proofs
are mathematical specifications, not extracted executable optimizer code.

Finite statistical statements take explicit moment and orthogonal-component
premises. The Gaussian κ=2 calculation and the extension to infinite support
are analytical, not formalized probability models. Conditional iid sampling
supplies the mean cross-moment premise; it does not hold under common noise.
Zero thresholds are treated separately from positive-threshold Chebyshev.

No global neural smoothness, convergence, momentum covariance, bf16 reliability,
TPU efficiency, all-peer superiority or absolute novelty is proved. Continuous
probability and verified numerical factorizations remain formalization work.
