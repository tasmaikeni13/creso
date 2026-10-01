# Phase 02 — Mathematical attacks and statistical simulation

**State: passed (r001, 2026-10-01).** Evidence: `research/r001/phase02-handoff.md`. Requires Phase 01. Apply theory-research and
experimental-research; simulations here test mechanisms, not LLM performance.

## Work

1. Build exact small finite-population cases and deterministic matrix quadratics.
   Independently verify solutions using dense constrained optimization, the VI,
   and the formal 2×2 counterexample. Test every failure found in Phase 01.
2. Design Monte Carlo cases spanning rectangular aspect ratios, rank deficiency,
   near-zero singular values, anisotropic and correlated noise, rotating signals,
   outliers, nearly deterministic gradients and deliberately unequal replicas.
   Include non-Gaussian distributions; check finite-variance assumptions explicitly.
3. Separate three questions: fixed-direction estimator calibration, realized
   disagreement suppression, and true expected progress of the adaptive update.
   Use independent evaluation draws for the last question. Estimate momentum
   noise separately; raw disagreement is not its covariance estimator.
4. Compare RASP with γ=0, unconstrained metric followed by projection, shuffled
   disagreement, equal-norm random disagreement, an oracle covariance diagnostic,
   and tuned peer methods. Control update norm and stepsize to distinguish risk
   information from simple damping. Keep oracle results labeled unattainable.
5. Predefine distributions, trial counts, effect thresholds and stopping rules.
   Save the random-generator version and seeds, use paired common random numbers,
   and report Monte Carlo standard errors and uncertainty coverage. Pilot variance
   can size a new fixed experiment; do not stop when a p-value becomes favorable.

## Gates and outputs

- Solver feasibility, objective and certificate agree across independent evaluators.
- A named regime supports a mechanism prediction beyond γ=0 and scalar damping;
  adversarial regimes and negative findings are retained.
- Results include distributions, full configurations, raw paired outcomes,
  estimator bias, true progress, solver work and state/communication estimates.
- Record how each result changes confidence in the competing hypotheses.

Kill or redesign the candidate if reliable disagreement fails to help even in
its intended controlled regime, if adaptive bias reverses the benefit, or if
required projection work makes TPU competitiveness implausible. Reopen Phase 01
for mathematical changes, and invalidate later dependent work.
