# Phase 03 — Complete reference optimizers

**State: not started.** Depends on passed Phases 01–02. Start only when requested.
Use ml-research and the mathematical claim map.

Implement complete CRESO and eligible peer trajectories with parameter groups,
weight decay, first-step state and exact scaling. The local matrix study is not
this phase. Muon requires ideal polar diagnostics and parity with its published
bf16 NS5 implementation. Preserve source coefficients, normalization, Nesterov,
shape scaling, approximation count and nonmatrix fallback. Port all 54 eligible
variants, including MONA and MARS-M, or mark the all-peer target incomplete.

Implement streaming same-weight replica statistics, freeze proposals, account
for both noise traces and zero variance, and return a certificate for the actual
step. If momentum is added, derive its estimator and covariance rather than
transferring iid claims. Check whole trajectories and independent gradient laws.

Measure per-replica gradient overhead, decompositions, buffers, state and
communication. In particular, 256 calibration pairs cannot be hidden as a
single two-way split. Keep total data/compute accounting comparable.

Gates: numerical references match definitions; complete peer source parity and
edge cases pass; steps are feasible; no certificate survives an invalid estimator;
state/oracle costs are reproducible. Record commands, pins and failure handoff.
