# Phase 08 — Statistical analysis, replication and claims

**State: not started.** Requires Phase 07. Apply experimental-research and
ml-research. Derive tables from immutable raw data with versioned scripts.

## Work

1. Publish all three seed outcomes and paired RASP-minus-peer differences, plus
   means, standard deviations and interval assumptions. Report token-weighted
   NLL and perplexity correctly; do not average batch perplexities into corpus
   perplexity or count checkpoints/tokens as independent training replicates.
2. Follow the frozen noninferiority and superiority margins. Correct for the
   registered family of peer comparisons where inferential claims require it.
   Bootstrap intervals with three seeds are fragile; show sensitivity rather
   than treating thousands of resamples as new independent evidence. With three
   nonzero paired differences, the smallest two-sided exact sign-test p-value
   is 0.25. Three wins alone cannot establish conventional significance that way.
3. Separate training-seed uncertainty, finite-test-set uncertainty, Monte Carlo
   error and measurement noise. Model-based intervals require stated assumptions.
   A large test set does not remove uncertainty across training seeds.
4. Compare matched-token quality, matched-time quality, time to the frozen loss
   target, peak memory and failure rates. Include setup, HPO and communication
   cost separately. Missing or diverged baselines stay in the result table.
5. Check mechanism predictions against ablations and out-of-regime failures.
   Refresh the novelty search; compare the final algorithm, not the original
   proposal, to contemporaneous work. Seek an independent implementation audit
   and external replication artifacts without claiming replication occurred.
6. Mark each claim supported, contradicted or unresolved. Matching all peers
   requires every eligible comparison to meet its declared practical criterion;
   an unsupported statistical claim remains unresolved. Extra seeds or a changed
   benchmark are a proposed extension, not an unannounced replacement of 42/43/44.

## Gates and outputs

- Reproducible analysis, raw per-seed tables, effect sizes, uncertainties,
  multiplicity decisions, ablations and a complete claim-evidence table.
- No conclusion exceeds the three-seed design or the observed hardware/model/data.
- Failing the scientific objective triggers diagnosis and dependent-phase revision;
  it does not trigger selective reporting. Keep an honest negative/inconclusive
  release if no supported improvement survives.

A changed method invalidates confirmation. Retain the old study and design
independent evidence for the replacement rather than relabeling it successful.
