# Phase 06 — Pilots, fair tuning and mechanism selection

**State: not started.** Requires Phases 02–05. These are development experiments;
confirmation seeds **42, 43, 44 remain unused for selection**.

## Work

1. Run a short integration pilot for every registered optimizer. Verify loss,
   token counts, masks, schedules, update diagnostics, memory and resume behavior.
   Distinguish reference/kernel bugs from an optimizer's genuine instability.
2. Execute the preregistered HPO design with equal compute opportunity and common
   development seeds. Include published strong defaults and comparable learning
   rate/decay ranges; give each method an opportunity to tune its essential
   damping, preconditioner, clipping and momentum parameters. Report all trials.
3. Tune RASP's μ, γ, radius and solver tolerance without silently adding loss-scale
   normalization, RMS matching or state averaging. A new component requires a
   revised theory, baseline comparison and ablation.
4. Test γ=0, precondition-then-project, shuffled and random disagreement,
   scalar/norm-matched damping and an estimate using independent data for analysis.
   Include a control that pays for the same replica communication. Charge extra
   data and backward passes when a diagnostic uses them.
5. Use validation metrics only. Compare matched-token quality and measured
   wall-clock efficiency. Check whether changing the solver tolerance changes
   which method wins. Diagnose any advantage that disappears after norm matching.
6. Freeze the candidate, every peer's best eligible configuration, the source
   commits, kernel/environment pins, all stopping rules and the analysis plan.

## Gates and outputs

- Every eligible peer has a faithful working configuration and comparable tuning.
- RASP has a supported mechanism explanation and a plausible cost/quality route
  to matching or exceeding the full peer set. A scalar-only explanation narrows
  or kills the proposed contribution.
- Full-run budget is concrete: 7.5B tokens per optimizer/variant, plus separately
  accounted development and ablation work. Pilot timing supplies the TPU-hour
  forecast; no invented throughput or speedup appears in the proposal.
- Deliver the selection report, all trial manifests, ablation analysis and a
  frozen confirmation manifest. Do not inspect locked test outcomes to select it.

On failure, update the failure ledger and reopen the responsible earlier phases.
Do not launch full confirmation merely to search for a lucky favorable seed.
