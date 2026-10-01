# Phase 04 — Model, data and preregistration

**State: not started.** Depends on Phases 01–03. Start only when requested.

Freeze one 125M model, parameter count, tokenizer and FineWeb-Edu revision,
deduplicated splits and hashes. Every optimizer/seed receives exactly 2.5B
training tokens. Reserve 42, 43 and 44 for confirmation. Publish tuning budgets,
validation cadence, primary loss metric, effect threshold, paired inference,
failure/resume policy and complete peer list before confirmation.

Fix replica microbatch granularity and token accounting. A replica is a
same-weight stochastic gradient, not a different local optimizer state. CRESO's
proposal/calibration/validation tokens count toward its training budget; every
peer gets the same global batch and eligible averaging information. If fewer
replicas or a new concentration method is required, reopen 01–02.

Prespecify CRESO rank/allowance search and match tuning opportunity for peers.
Muon and all eligible source variants must be included. Compare quality per token,
wall time and memory separately; do not let extra validation or data confer a
hidden advantage. Freeze checkpoint choice and all missing-run handling.

Gates: auditable model/data/token manifests, complete baseline set, fixed
statistical families and unchanged confirmation seeds. No training executed here.
