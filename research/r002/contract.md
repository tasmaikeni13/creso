# Revision r002 — research contract

Started 1 October 2026 from `6deb195`. User explicitly authorizes a new mechanism,
theory and Lean proofs, execution of Phases 01–02, replacement of current project
instructions and a GitHub push. Muon is mandatory. Later training phases await
their start instruction. The former RASP revision remains in `research/r001`;
active specifications and its state are snapshotted in `archive/`.

## Target

Develop CRESO: Certified Replica Spectral Optimization. Seek an adaptive matrix
update with a valid uncertainty certificate, useful progress when the actual
operator-norm constraint is active, and a fixed small number of decompositions.
High novelty and a breakthrough are research ambitions, not assumed outcomes.

## Proposed mechanism and claim types

Separate proposal replicas from independent validation replicas at the same
weights. Proposal differences supply a low-dimensional noise subspace. Construct
a small library of operator-feasible directions including Muon, an ordinary
gradient direction, a subspace-deflated direction and zero. Validate directional
linear rewards; include explicit uncertainty allowances. Optimize the certified
quadratic progress over every pairwise interpolation in the library. This needs
scalar quadratic solves, rather than nested matrix projection roots.

The new mathematical targets are: actual matrix feasibility and existence;
exact interpolation optimization; uniform certificates for decisions selected
after validation; a finite-law simultaneous confidence bound; and an oracle
inequality against the included proposal directions. Any covariance envelope
needed for a certificate must be stated and checked. A learned subspace alone
does not certify that it contains future noise. The algorithm does not observe
the true gradient or a population covariance operator.

## Comparison and evidence

Primary Phase 02 question: does the new decision rule improve independent
quadratic progress over both ideal Muon and finite NS5 Muon, as well as a tuned
full-gradient spectral baseline, under an active spectral constraint and the
same total replica oracle budget? Compare against all implemented controls,
preserve an inventory of eligible but unported peers, and never infer an
all-peer training result from local maps. Baselines may use the mean of every
replica; the proposed method pays for its split. Record state and communication.

Separate selected-proposal guarantees from comparisons to stronger peers using
the full replica mean. Baseline initial-state maps cannot represent complete
optimizer trajectories. Independent validation samples never double as the
confirmation measurement. Seeds 42–44 remain untouched.

## Search, iteration and stopping

Compare a noise-subspace branch, a validated interpolation branch and a nonlinear
spectral debiasing branch. Credit low-rank covariance, sample splitting, convex
aggregation and scalar optimization as prior mechanisms. Search exact composed
updates under operational synonyms; stop once the closest sources and their
differences are resolved. An equivalent prior instantiation rejects novelty.

Implement independent verifiers before selection. Archive failed prototypes.
Freeze the numerical protocol and source revision before final draws. Require
positive adjusted primary contrasts against the named controls, verified active
constraints, valid certificate diagnostics under their stated law, and preserved
negative regimes. A failed gate is reported as failed or unresolved; thresholds
are not relaxed to obtain success. The handoff must say whether a breakthrough
claim remains speculative even if all these smaller gates pass.
