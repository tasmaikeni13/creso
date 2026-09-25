# Phase 05 — TPU kernels and distributed correctness

**State: not started.** Requires Phases 03–04 and the approximate-solver analysis
from Phase 01. Target: Google Cloud TPU v4-32, **16 v4 chips**.

## Work

1. Record actual hosts, processes, `jax.devices()`, chip/core mapping, topology,
   HBM and software versions. The hardware name denotes 32 TensorCores, not
   necessarily 32 devices exposed by the runtime. The documented chip topology
   is 2×2×4, with 32 GiB HBM per chip. Verify allocation against the
   [official v4 specification](https://docs.cloud.google.com/tpu/docs/v4).
2. Implement JAX references first, using explicit shardings and correct collectives.
   Preserve the same global batch. Obtain two equal, independently sampled group
   means at the same weights, then their mean and difference. Log group sample
   counts, reduction dtype and all communication; do not treat device-local
   sums as unbiased averaged gradients without normalization.
3. Implement the strongest faithful TPU versions of RASP and all peers. Use
   [Pallas TPU](https://docs.jax.dev/en/latest/pallas/tpu/quickstart.html) only where
   profiling justifies custom kernels. Profile matrix products, projections,
   root iterations, state traffic, eigensolvers and collectives separately.
4. Select precision deliberately: float64 CPU oracle, float32 reference, and
   bf16 matrix inputs with float32 accumulation where validated. Certify both
   projection error and scalar feedback error; a small feedback residual alone
   cannot certify an approximate projection. Never call a polar iteration a
   spectral projection without proving or checking its actual contract.
5. Test representative 125M model shapes, sharding, transposes, padding, uneven
   masks, rank deficiency, scale extremes and interrupted multi-host resume.
   Measure warmed-up execution with synchronization; report compilation separately.
6. Tune compiler flags and layout fairly for peers. Record maximum memory,
   temporary buffers, materialized copies and communication volume per step.

## Gates and outputs

- Every kernel meets its registered reference error and feasibility tolerances.
- Distributed gradients agree with a single-process reference using the same data.
- No deadlocks, silent host divergence, hidden extra tokens or dropped parameters.
- Checkpoint/resume preserves all optimizer, data-cursor and RNG state.
- Deliver source, pinned environment, shape benchmarks, parity logs and an honest
  end-to-end cost forecast. If repeated projections dominate, revisit the solver
  or mechanism before scaling; speed is not established by a FLOP count.

Numerical changes that alter the algorithm return to Phase 01. A TPU port bug
invalidates measurements derived from that port.
