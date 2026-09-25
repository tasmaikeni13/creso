# Phase 07 — Competitive confirmation runs

**State: not started.** Requires passing Phases 01–06 and their frozen artifacts.

## Immutable run contract

For **each optimizer and registered confirmatory variant**, train the same
**125M** model on **2,500,000,000 FineWeb-Edu training tokens for each seed
42, 43 and 44**. Run on the specified **v4-32 slice (16 v4 chips)**.
For N registered variants, the required training count is 3N runs and 7.5N billion
tokens, excluding the separately reported HPO and pilot budget.

## Work

1. Verify hashes, environment and hardware immediately before starting. Assign
   immutable run IDs containing method, configuration revision and seed.
2. Pair methods by seed, initialization and data order. Balance run order across
   methods to reduce system drift. Evaluate the same checkpoints by token count.
3. Save raw train/validation loss, elapsed times, synchronization/compile times,
   memory, throughput, solver diagnostics, numerical events and checkpoint hashes.
   Record any missing measurements. Preserve progress in durable storage.
4. Confirm final token count with the registered partial-batch policy. Save final
   and scheduled checkpoints. Do not select a favorable intermediate checkpoint
   unless the exact selection rule was preregistered for every optimizer.
5. Resume infrastructure interruptions from the exact model, optimizer, RNG and
   data-cursor state. Record both failed attempt and continuation. Numerical
   divergence is a method/configuration outcome, not a disposable infrastructure
   incident. Never replace a bad seed by another seed.
6. Release test evaluations only according to the frozen protocol. Do not tune
   μ, γ, learning rate or peer configurations based on these results.

## Gates and outputs

- Complete registry × {42,43,44} manifest, or explicit failed/missing run entries.
- Identical model/data/protocol hashes and exact per-run training-token budgets.
- All raw data and checkpoints have durable locations and integrity hashes.
- No positive performance claim is made before Phase 08's analysis.

If a bug invalidates results, preserve the invalid runs, repair the cause, update
affected phases and rerun the affected comparison with a new revision. If RASP
underperforms, diagnose scientifically; a redesign creates a new study. These
seeds/results are then development evidence, and an independent confirmation
strategy must be specified before another confirmatory claim. Do not pretend
repeated testing of the same held-out outcomes remains untouched confirmation.
