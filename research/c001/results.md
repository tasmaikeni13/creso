# CRESO Phase 02 — executed results

Revision **c001**, frozen before final draws. This is a one-step synthetic matrix
study, not a language-model benchmark. All methods receive the same 648 replica
oracle budget; peers may average every replica. The method pays for its proposal
split and calibrated uncertainty. Population labels assess methods and select
development configurations, never the final per-context decision.

## Primary result

All nine prespecified primary contrasts pass: CRESO improves population quadratic
progress over ideal Muon, feasible float64 NS5 and tuned hard spectral projection
in three orthogonal-noise shapes. Every CRESO step in those laws has operator norm
0.5. The ideal-Muon gap is **0.125**: progress 0.375 versus 0.250, a 50% relative
improvement on this constructed law. The same gain is proved for an explicit
active 2×2 matrix witness. This does not establish a neural training advantage.

| Law | Peer | Mean paired improvement | Family-adjusted interval | MCSE | Gate >0.01 |
|---|---|---:|---|---:|---|
| orthogonal_2x2 | muon_polar | 0.125000 | [0.125000, 0.125000] | 0.000000 | Passed |
| orthogonal_2x2 | muon_ns5_feasible | 0.151641 | [0.148884, 0.154399] | 0.000994 | Passed |
| orthogonal_2x2 | hard_spectral | 0.052118 | [0.050056, 0.054181] | 0.000744 | Passed |
| rotated_4x4 | muon_polar | 0.125000 | [0.125000, 0.125000] | 0.000000 | Passed |
| rotated_4x4 | muon_ns5_feasible | 0.151009 | [0.148267, 0.153750] | 0.000988 | Passed |
| rotated_4x4 | hard_spectral | 0.053140 | [0.051076, 0.055204] | 0.000744 | Passed |
| rectangular_3x5 | muon_polar | 0.125000 | [0.125000, 0.125000] | 0.000000 | Passed |
| rectangular_3x5 | muon_ns5_feasible | 0.152056 | [0.149356, 0.154755] | 0.000973 | Passed |
| rectangular_3x5 | hard_spectral | 0.052678 | [0.050598, 0.054757] | 0.000750 | Passed |

There are 4,096 independent contexts per law, 49,152 in total. Each of 13 methods
gets 24 development configuration evaluations; zero and norm-matched full-mean
controls are additional. Configurations are selected per law, so these are local
mechanism comparisons, not one universally tuned optimizer. Six momentum choices
for zero-state ideal Muon give equivalent normalized inputs; equal evaluation
count does not make the effective hyperparameter search dimension equal.

The separately prespecified mixed-signal test improves over fixed deflation by
**0.133807**, 95% interval [0.129596, 0.138018]. This tests
restoration of useful signal in a noisy span. TONGA-style shrinkage also succeeds
in this law, so the contrast does not establish that validation is uniquely needed.

Student intervals use Bonferroni over nine primary contrasts; they describe
Monte Carlo sampling error and are asymptotic. The 2,000-replicate paired bootstrap
sensitivity intervals corroborate the primary effects. The algorithmic confidence
guarantee is a separate nonasymptotic moment bound. Seeds 42–44 are untouched.

## Every law, including losses and ties

| Law | CRESO | Ideal Muon | Feasible NS5 | Hard spectral | TONGA sketch | CRESO active fraction |
|---|---:|---:|---:|---:|---:|---:|
| orthogonal_2x2 | 0.375000 | 0.250000 | 0.223359 | 0.322882 | 0.375000 | 1.0000 |
| rotated_4x4 | 0.375000 | 0.250000 | 0.223991 | 0.321860 | 0.375000 | 1.0000 |
| rectangular_3x5 | 0.375000 | 0.250000 | 0.222944 | 0.322322 | 0.375000 | 1.0000 |
| orthogonal_rank2 | 0.468750 | 0.250000 | 0.295503 | 0.396150 | 0.499999 | 1.0000 |
| mixed_signal | 0.508807 | 0.444629 | 0.413321 | 0.466115 | 0.508807 | 1.0000 |
| signal_noise_overlap | 0.375000 | 0.650000 | 0.611473 | 0.650000 | 0.650000 | 1.0000 |
| isotropic_low | 0.374181 | 0.124997 | 0.084269 | 0.374990 | 0.374977 | 0.9641 |
| isotropic_high | 0.000000 | 0.103094 | 0.088723 | 0.285154 | 0.186457 | 0.0000 |
| zero_noise | 0.375000 | 0.375000 | 0.375000 | 0.375000 | 0.375000 | 1.0000 |
| zero_signal | 0.000000 | -0.031250 | -0.022590 | -0.000308 | -0.000578 | 0.0000 |
| dependent_replicas | 0.374800 | 0.250000 | 0.242590 | 0.287134 | 0.373096 | 1.0000 |
| heavy_tail_t3 | 0.375000 | 0.250000 | 0.225154 | 0.324609 | 0.375000 | 1.0000 |

TONGA/deflation ties in orthogonal rank-one cases mean that their gains can be
explained by established covariance filtering. In rank-two noise TONGA is better.
CRESO loses 0.275 progress in signal/noise overlap and returns zero in high
isotropic noise while hard spectral makes positive progress. It is slightly
worse than hard spectral in low isotropic noise. These are core limitations,
not excluded outliers. All 15 local controls are in the CSV and raw artifacts.

No interior interpolation is selected on the primary laws: the gain there is
deflation, not mixing. The independent active two-vertex witness shows a strict
1/8 mixing gain; the isotropic-low law has some interior mixtures. That witness
verifies the finite solver but does not make generic convex aggregation new.

## Confidence and assumption attacks

No certificate failure is observed on the ten valid Gaussian iid laws (40,960
contexts). A simultaneous one-sided Clopper–Pearson upper bound per law is
0.001293, below the declared 0.05. These data do not prove calibration is sharp:
the two-trace Chebyshev bound is conservative. Both true projected and residual
trace envelopes are checked from the known covariance. The in-library oracle
inequality has no numerical violation in the replay.

The dependent-replica law violates the assumption; it has 9 certificate failures
and frequent trace underestimation. The t₃ law violates the fourth-moment bound
even though its chosen deflated updates show no certificate failure. Neither
invalid law can establish the theorem's coverage.

The independent attacks are stronger diagnostics:

- Common unbiased noise shared by every replica yields **512/512** false
  certificates: certificate +0.375, true progress −0.125. Lean verifies a matrix
  witness. Differences cannot detect common noise.
- With noise outside the learned proposal span, calibrated residual bounds have
  **0/512** failures; incorrectly omitting them produces **269/512** failures.
- Correlated projected/residual noise can saturate the factor-two envelope.
  Dropping that factor without a covariance condition underestimates variance.

## Independent measurement and reproducibility

Every context has 256 additional independent assessment replicas, inaccessible
to the methods. The primary response is exact population quadratic progress
because the synthetic gradient is known. Independent noisy assessments and
their uncertainty are included for each control, not silently substituted for
population metrics. Confirmation seeds are reserved for future training.

All 192 final raw files pass SHA-256 checks. All 13 tuned methods replay exactly
from raw replica inputs; independent inner-product readouts and operator norms
agree within declared tolerances. All final aggregates match the raw results.
The exact protocol, code hashes and pre-final source commit are in the freeze
and final manifest. Raw replicas, gradients, subspaces, directions, certificates,
labels and assessments are stored losslessly outside Git.

## Cost and interpretation

The reference uses three matrix SVDs, a four-row sketch SVD and ten scalar pairs.
Measured host cost includes reductions and excludes gradient generation and
communication. At 64×64, CRESO takes about 16.4 ms per decision, versus 2.5 ms
for feasible NS5 and 43.1 ms for the rank-one constrained proximal comparator
(52.25 matrix SVDs). These seven-repeat CPU measurements are illustrative, not
TPU benchmarks or a throughput claim. CRESO is more expensive than simple peers.

Its elementary 95% certificate needs more than 160 calibration pairs; the study
uses 256. Streaming avoids retaining all 648 gradients, but basis/candidate
state and synchronization still need a complete implementation. The apparent
component composition is worth studying; no extreme-novelty, convergence,
all-peer training or breakthrough claim is supported yet.

[Result figure](results.svg). Full distributions, paired effects, independent
assessment and gates: `run-v1/final/results.json`. Every method's mean is in
`summary.csv`; replay and bootstrap checks are in `reproduction-checks.json`.

## Unrepaired published NS5 diagnostic

A supplemental exploratory comparison uses the pinned Muon coefficients, EMA/
Nesterov order, orientation and shape scale **without radial feasibility repair**.
It replaces bf16 with float64, so it is not source precision parity or a complete
training trajectory. Its 24 configurations are selected on independent development
data, with no final-data selection; its intervals are descriptive.

| Law | Unrepaired NS5 progress | CRESO minus source map | Exceeds radius 0.5 |
|---|---:|---:|---:|
| orthogonal_2x2 | 0.219897 | 0.155103 | 0.6824 |
| rotated_4x4 | 0.220695 | 0.154305 | 0.6831 |
| rectangular_3x5 | 0.219321 | 0.155679 | 0.6741 |
| mixed_signal | 0.473215 | 0.035593 | 1.0000 |
| zero_noise | 0.385916 | -0.010916 | 1.0000 |

The primary orthogonal-noise gains persist against this unrepaired map. It wins
in the noiseless law with a larger-than-radius step; neither map therefore
dominates in every local case. `source-muon-check.json` and its lossless supplemental
raw asset retain every law and the exact development selection. The primary
protocol/gates are unchanged. The pinned primary source was retrieved and its
coefficients checked; source bf16/whole-trajectory parity remains future work.
