# Phase 03 — CPU references for RASP and peers

**State: not started.** Requires Phases 01–02. No TPU optimization yet.

Execution handoff: `research/r001/phase02-handoff.md`. The study evaluator and
one-step maps are research artifacts, not these complete multi-step optimizer
ports. Use all 52 registry IDs and preserve the paper/code discrepancies.

## Work

1. Implement a float64 CPU RASP reference directly from the frozen equations.
   Keep gradients, half-batch weighting, momentum, spectral projection, scalar
   solve, decay and parameter groups explicit. Define zero-input behavior and
   numerical stopping tolerances from the error certificate.
2. Implement every registered peer, using official implementations as the
   authority for variants and defaults. Pin source commits and licenses. Port
   actual momentum/Nesterov, normalization, bias correction, matrix orientation,
   damping, state dtype, decay order and nonmatrix fallback rules.
3. Use exact SVD/eigendecomposition as mathematical references. Prove or cite the
   numerical primitive's contract and verify its relation to the formal
   variational specification; add Lean results for new mathematical claims.
4. Check golden tensors against upstream implementations and finite-difference
   objective checks where informative. Cover rectangular matrices, repeated
   singular values, near-zero inputs, extreme scales and multi-step state updates.
5. Define a shared optimizer interface and checkpoint schema. Save parameter-group
   coverage, state bytes, update RMS, operator norm, disagreement alignment, root
   residual, projection error and iteration count. Round-trip optimizer state.

## Gates and outputs

- Every peer has a passing parity report, or a documented unresolved blocker.
- RASP matches independent constrained solutions and the formal counterexample.
- Tests detect known wrong variants: wrong half-batch normalization, post-clipping
  an anisotropic solve, momentum covariance substitution, and silent RMS rescaling.
- Checkpoint resume reproduces the uninterrupted CPU trajectory.
- Deliver documented reference modules, source pins, mathematical/numerical tests
  and a machine-readable optimizer registry. Record real commands in the README.

A formula change returns to Phase 01. A reference bug invalidates affected
tests, model/protocol assumptions and all derived kernels and measurements.
