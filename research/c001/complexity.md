# CRESO cost model

Let d=mn, s=min(m,n), rank k≤4 and K=4 candidates. The reference performs
three matrix SVDs (O(mns)), one four-row sketch SVD (O(16d)), n_c projected
calibration contractions (O(n_c k d)), mean reductions and K(K+1)/2=10 scalar
quadratic solves with matrix inner products. The two mean SVDs may share a
factorization; that optimization is unimplemented. Work does not grow through
a nested spectral projection root.

The method consumes eight proposal gradients, 512 calibration gradients and
128 extra validation gradients at the same weights, 648 in total. Calibration
pair sums are reused only by the valid unconditional union argument. Baselines
receive all 648 gradients. The independent 256-replica assessment is outside
the method and tuning input. No sample or token is free in a training budget.

Calibration can stream differences, projected coordinates and residual norms;
all gradients need not be stored. A rank-k basis costs kd scalars, three nonzero
candidates cost 3d and mean/difference/work buffers add several d. Exact memory
depends on sharding and factorization; no full-model peak-memory claim is made.

A distributed implementation needs a proposal barrier, basis distribution,
post-proposal statistics, aggregate gradient and selection scalars. Collective
count/bytes and per-replica gradient materialization are unresolved. Sixteen
TPU chips do not make 648 independent replicas a single inexpensive collective.

Host profiles in diagnostics.json use 8², 32² and 64² matrices, seven repeats,
batch four, float64 and one BLAS thread. Timers include required replica reductions,
exclude generation/gradient compute and network communication, and are CPU only.
Simple Muon/spectral maps are faster; the rank-one proximal comparator is slower.
Calibration conservatism and information cost can erase training usefulness.
