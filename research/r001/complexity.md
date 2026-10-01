# Cost model (estimates, not TPU measurements)

For a block m×n, N=mn, q=min(m,n), S projections:

| Method component | Arithmetic / storage |
|---|---|
| RASP split mean/difference, momentum, dot products | O(N), persistent M: N scalars; E: N transient scalars |
| Unconstrained rank-one inverse | `X=(M - γ<E,M>E/(μ+γ||E||F²))/μ`; O(N), exact when spectrally feasible |
| Active root with dense SVD projections | O(S N q), including S matrix inputs and reductions; O(N+q²) typical workspace; vendor routines vary |
| γ=0 spectral projection | One projection O(Nq); exact-SVD simulation diagnostic |
| Finite NS5 Muon | Five polynomial matrix filters O(Nq+q³) per iteration, plus normalization; actual output differs from polar |
| Dion3, selected fraction f | Communication and filtering on f rows, extra row state; official batching/feedback matter |
| Shampoo/SOAP | O(m²+n²) matrix state plus moments, periodically O(m³+n³) decompositions; block size matters |
| k-direction sketch candidate | kN state and reductions, higher-dimensional low-rank proximal solve; not selected |

The scalar unconstrained expression is Sherman–Morrison, prior mathematics.
Testing its largest singular value is itself work. Simulation reports an SVD
feasibility check separately and never presents the fast path as zero projection
cost. A certified cheaper bound (e.g. Frobenius or a rigorously bounded estimate)
can avoid an SVD but is conservatively restrictive. A coupled solver warm start,
accelerated root or partial SVD is a future implementation choice, not a timing
result.

## Replica communication

Target p=16 TPU v4 chips. For b-byte gradient entries, a standard ring all-reduce
of N values sends `2(p-1)/p * bN` bytes per chip. A transparent implementation
all-reduces the ordinary gradient plus a signed gradient channel (positive on
one half, negative on the other), allowing each chip to recover G,E. This adds
one such all-reduce, about 0.938 GB per chip for 125M fp32 values, excluding
collective latency and any model/optimizer sharding traffic. The group means
must be weighted by token counts; unequal valid-token halves invalidate the iid
equal-half formula. Alternative subgroup reductions must account for exchanges
needed to expose both halves; do not count them as communication-free.

Persistent momentum is about 500 MB at fp32 for 125M scalars before sharding;
one full transient E is another 500 MB. These are upper bookkeeping values
because nonmatrix parameters may use auxiliary AdamW and the architecture is
not frozen until Phase 04. Peak memory also includes G, D, autodiff buffers,
SVD/NS workspace, and collective buffers. Chips do not necessarily hold full
replicas; the actual mesh and partition rules belong to Phase 05.

No CPU SVD timing here predicts TPU time. A full-step cost comparison requires
training arithmetic, state dtype, actual matrix sizes, projection count,
collective latency/bandwidth and overlap. Multiple exact projections are a
serious risk, but flop counts alone cannot settle feasibility. Stop before
confirmation if profiling shows they dominate the matched training budget.
