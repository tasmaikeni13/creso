# Phase 01 — Frontier and formal analysis

**State: passed (r001, 2026-10-01).** Evidence: `research/r001/phase01-handoff.md`. Inputs: `theory.md`, `formal/`, the preparation research
record, and the literature-frontier, mechanism-transfer and theory-research skills.

## Work

1. Refresh literature through the execution date. Follow citations and official
   code from the closest methods. Search operationally equivalent updates under
   different names; compare assumptions, objective, estimator, constraint,
   solver, parameter groups and computational cost. Freeze a dated registry.
2. Start with AdamW and momentum SGD as controls; Muon, Shampoo, SOAP, AdaMuon,
   NorMuon, Muon-NSR, Muon-VS, DeVA, MuCon, SPECTRA, Musec, SoftMusec, ARO and the
   strongest available Dion variant as competitors. Inspect OptMuon and other
   new methods for inclusion. Record each distinct eligible variant; do not
   choose the weakest member of a family. ODE-only proposals need an actual
   published discrete algorithm before becoming training baselines.
3. Write exact peer update definitions and formalize comparison lemmas that the
   proposed advantage depends on. Distinguish ideal polar updates from finite
   Newton–Schulz code. Do not assert that every peer lacks RASP's stability.
4. Audit every RASP equation against Lean, with rectangular shapes, zero signal,
   zero disagreement, rank deficiency, zero radius, large/small gradient scale,
   and input-dependent disagreement. Check units and optimizer state.
5. Extend solver analysis to approximate projections, finite precision and
   termination. The existing feedback bound assumes exact projection. Establish
   a usable feasibility/VI error certificate before planning an approximate kernel.
6. Maintain distinct candidate branches: coupled replica metric; plain spectral
   regularization; a richer covariance sketch; and the null explanation that only
   update magnitude matters. Use the transfer cards to reject unsupported bridges.

## Gates and outputs

- `lake build` and `lake env lean Audit.lean` pass with complete theorem coverage.
- Every claimed advantage has a precise domain, proof or falsifiable hypothesis.
- A facet comparison acknowledges SPECTRA's generic containment and the existing
  low-rank proximal solver. Equivalent prior instantiation kills the novelty claim.
- Output definitions, assumption ledger, competitor registry, complexity model,
  source snapshots/hashes and revised claim map in `research/<revision>/`.

If a theorem fails, repair or replace it and update all dependent phases before
proceeding. If novelty fails, retain the useful analysis and search a different
mechanism; a new name is not a new method.
