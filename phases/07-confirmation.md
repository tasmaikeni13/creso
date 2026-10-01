# Phase 07 — Frozen competitive training

**State: not started.** Depends on Phases 01–06. Start only when requested.

Run each frozen optimizer on the same 125M model for **2.5B FineWeb-Edu tokens
per seed**, seeds **42, 43 and 44**, using TPU v4-32 (16 chips). This is 7.5B
training tokens per optimizer. Include every eligible peer, with Muon mandatory.
No method/configuration selection or checkpoint choice may change after viewing
confirmation. A missing eligible peer prevents the all-peer objective.

Preserve token-level progress, independent validation, elapsed synchronized time,
peak memory, throughput, certificates, active and zero fractions, precision
fallbacks, failures, exact resumes and checkpoint/source manifests. Charge all
calibration and communication. Report quality, cost and reliability separately.

Use only preregistered failure/resume rules. A model or optimizer change creates
fresh confirmation, never a favorable replacement of an unlucky seed.
Gates: complete frozen runs, correct budgets, intact seeds/data and reproducible
raw evidence. No outcome is assumed to beat peers; retain loss or inconclusiveness.
