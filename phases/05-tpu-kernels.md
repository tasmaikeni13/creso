# Phase 05 — TPU implementation and certification

**State: not started.** Depends on Phases 03–04. Start only when requested.
Target TPU v4-32: 16 chips. Use JAX/Pallas and source-faithful peer kernels.

Implement candidate construction, sketch factorization, streamable projected and
residual traces, validation contractions and ten scalar decisions. Share mean
factorizations if parity allows. Avoid materializing hundreds of full gradients.
Account for the proposal barrier, basis broadcasts, aggregate means and trace
collectives. Same-weight unbiasedness and independent data must survive sharding.

Validate matrix operator-norm bounds under actual bf16/fp32 arithmetic. A measured
SVD norm is not a formal roundoff enclosure. Certify feasibility and objective
errors, include exact-reference fallbacks, and charge them. Add explicit allowance
for numerical reward/trace errors before claiming a confidence certificate.

Benchmark compiled, warmed and synchronized kernels and complete optimizer steps,
including communication, calibration gradient work and recompilation costs.
Muon NS5, full-data spectral and adaptive baselines need equal accounting.
Record compilation versions, shape cases, p50/p95 time, state and peak memory.

Gates: source/reference parity, justified arithmetic tolerances, streaming memory,
complete collectives and reproducible TPU profiles. CPU/CUDA timing is not TPU timing.
