# Phase 01 handoff — r001

**Passed, 2026-10-01.** Scope: frontier definitions and formal analysis only.

- 52 discrete variant IDs frozen with dated primary sources and code pins.
- Actual matrix existence, uniqueness and noncommutation proofs preserved.
- Twelve approximation/termination/comparison lemmas added; 61 public theorems
  plus `matrixStep` audited. Only standard Lean axioms; all nine dependency pins
  and the skills submodule unchanged and clean.
- `lake build` and `lake env lean Audit.lean` pass; outputs and coverage/pin
  checks are saved in this directory.
- Advantage claims have domains or explicit falsifiers; SPECTRA containment,
  known BFO solver and known primitives prevent an absolute novelty claim.

Phase 02 receives H1 and its rival branches, exact certificates and preserved
failures. Its protocol must freeze before final draws. No reference training
ports, TPU kernels, tuning pilots or later training phases have executed.
