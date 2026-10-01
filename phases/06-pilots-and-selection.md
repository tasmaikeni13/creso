# Phase 06 — Fair tuning and pilot selection

**State: not started.** Depends on Phases 02–05. Start only when requested.
Use ml-research and experimental-research skills.

Run prescribed pilots on development seeds only. Match tuning budgets and baseline
fidelity across every eligible method, including Muon, MONA and MARS-M. Count
CRESO's gradient/calibration/collective costs and all failed tuning trials.
Investigate whether conservative residual-trace bounds cause zero updates at
realistic noise dimensions and whether the noise subspace deletes signal.

Prespecified ablations: covariance deflation/TONGA inversion, no certificate,
proposal-data reuse, shuffled/equal-energy subspaces, norm-matched directions,
rank, trace residual, sample count and calibration frequency. No momentum/drift
certificate is inferred from iid one-step results. A scheduled or smaller-sample
certificate is a new mathematical method and reopens 01–02.

Select once on allowed data. Freeze chosen configurations and source hashes before
07. Keep all failed runs and negative ablations. Never select on seeds 42–44.
Gates: meaningful progress, useful cost, complete fair tuning and validated
statistical assumptions. Stop the branch if it stalls or cost destroys utility.
