# Phase 02 — Numerical and statistical falsification

**State: running (c001).** Inputs: fixed Phase 01 definitions, experimental-research
and ml-research skills. Output: frozen protocol, raw evidence and phase02-handoff.md.

## Work

1. Check actual operator feasibility and each scalar segment against an
   independent optimizer before selecting configurations. Test adaptive selection,
   zero/degenerate cases and the covariance envelope.
2. Freeze synthetic laws, fixed contexts, effect thresholds, multiplicity,
   seeds, controls and stopping. Development selects 24 configurations per method;
   final contexts are untouched. Seeds 42–44 remain reserved.
3. Let peers average all 648 method replicas. CRESO uses eight proposals, 256
   calibration pairs and a 640-replica post-proposal mean. An additional independent
   assessment set never enters selection. Population labels are evaluator-only.
4. Require ideal Muon, feasible float64 NS5 and hard spectral baselines in the
   primary contrasts. Preserve TONGA-style inversion, deflation, scalar/norm
   controls, rank-one proximal, uncertified and proposal-reuse ablations.
5. Retain overlap, isotropic, zero, dependent and heavy-tail laws. Report true
   progress, independent noisy assessment, active fractions, certificate failures,
   MCSE, adjusted intervals, bootstrap sensitivity and exact raw configurations.
6. Verify raw hashes and replay selected decisions. Record CPU work and state;
   do not claim TPU throughput or full optimizer trajectories.

## Frozen gates

Use `research/c001/protocol.json`: all nine primary contrasts have adjusted lower
bounds above 0.01; primary active fractions ≥0.9; mixed-law improvement over fixed
deflation has lower bound >0.01; simultaneous coverage upper bounds on each valid
law are <0.05; independent verifiers and actual feasibility pass. Do not change
these thresholds after viewing final outcomes. Invalid-law successes do not
establish coverage. Ties and losses against other controls remain visible.

A failed gate is failed, not a success story. Substantive repair needs a new
revision and fresh final evidence; do not silently expand a local win's scope.
