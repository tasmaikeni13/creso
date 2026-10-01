# CRESO assumption ledger

| Assumption | Role | Evidence / boundary |
|---|---|---|
| Same weights within a step; proposal frozen before following samples | Fixed vertex error control | Algorithm/reference order; not local optimizer states |
| Post-proposal gradients iid and unbiased conditional on weights/proposals | Mean variance v/n and honest reward | Gaussian laws satisfy it; common-noise attack fails completely |
| Fourth moment bound Var(||SE||²)≤κq² | Relative trace upper bound | Gaussian κ=2 analytical; t₃ not covered |
| Both projected and residual traces are included | Noise span may be incomplete | Omitting residual produces 269/512 false certificates |
| Orthogonal projector and exact norm geometry | Directional envelope and feasibility | Exact specification; SVD/numerical precision only tested |
| Upper loss model, η≥0 and Lη≤μ | Descent from progress | Conditional theorem; no neural global smoothness proof |
| Fixed finite candidate library | Uniform certificate and finite solver | Four vertices; no full-ball or full-simplex optimum claim |
| All baselines get equal total oracle/data budget | Fair local comparison | Full 648-replica average available to every peer |
| Zero variance handled exactly | Avoid invalid zero-threshold Chebyshev | Finite proof and zero-noise tests; floating tolerances are empirical |

Continuous Gaussian calculations and measurability are analytical extensions.
Finite masses and moments, matrix geometry and adaptive decision implications
are kernel-verified. Momentum, drift, shared noise, source bf16 parity and TPU
cost need new evidence. A calibration estimate is not an oracle covariance.
