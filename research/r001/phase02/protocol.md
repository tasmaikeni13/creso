# Frozen Phase 02 protocol — r001-p02-v1

Machine specification: `protocol.json`. Frozen before development or final MC
draws. Solver attacks may run beforehand because they select no statistical
law or favorable method result. Freeze code/config hashes in Git before final
simulation. Changes motivated by results require a new protocol and fresh draws.

The unit is an independent quadratic problem context and its two gradient
observations. Its signal has unit Frobenius norm. In the primary law, an
independently sampled unit matrix v is orthogonal to g in vectorized space;
conditional half-errors are independent N(0,9) multiples of v. The context
orientation varies across units, and is fixed across both half observations and
independent evaluation. This is an intended rank-one uncertainty regime, not
a general gradient law. Rank one refers to covariance in vectorized space, not
the matrix rank of v. RASP receives only M and E, never g or v.

The selected γ minimizes development expected quadratic loss alongside η on
the finite grid. Each parameterized peer receives six parameters times four
stepsizes; simple maps receive the same 24 evaluations (duplicates retained).
These are one-step mathematical maps, not full training optimizer ports. SOAP's
documented first-step skip is a separate reference, not a claim that this is its
steady-state behavior. Complete peer state/parity belongs to Phase 03.

At the primary norm-controlled endpoint, every nonzero direction is scaled to
unit Frobenius norm. This remains feasible in the radius-one spectral ball, and
the same η=0.3 is used. Any scalar damping of the γ=0 direction has that same
normalized direction. Independent evaluation errors use fresh conditional
draws. We report both the exact conditional quadratic progress
`η<g,D>-η²||D||²/2` and independently observed progress, MCSEs and paired CIs.

Shuffled E comes from an independent donor pool permuted **across contexts**;
an equal-norm random E is sampled
with the same unit-direction construction orthogonal to g. The evaluator uses
g solely to generate the known law and its matched marginal control, not to
provide information to RASP. Each donor is used once, so final experimental units
remain independent under the iid donor law and a permutation chosen independently.
In a fixed-orientation Gaussian context, shuffling independent E would have
the same population law; the rotating context is deliberately specified here.

Oracle diagnostic uses the known conditional covariance of mean noise and
is unattainable. Rank-one oracle can use the scalar solve; the multi-rank oracle
uses a separately converged projected quadratic optimizer with a PSD covariance.
No oracle enters RASP selection or supports an implementable-method claim.

All Gaussian, Student-t5 (variance scaled to one), and centered Bernoulli
outlier laws have finite variance; t5 also has finite fourth moment. The t5
statistical calibration remains empirical, whereas exact finite-population
enumeration separately exercises the Lean assumptions. Correlated/unequal
halves intentionally violate the iid centered premise. The measured adaptive
surrogate is compared with fresh mean-noise risk, never asserted unbiased.

Momentum has β=0 in the primary mechanism isolation. A separate β=0.9,
32-step rotating-signal attack and stationary variance calibration assess the
actual uncorrected momentum convention. Current disagreement is not substituted
for momentum noise variance. These are not training seed selection; 42–44 stay
untouched.

The three primary lower Bonferroni confidence limits must each exceed 0.01
absolute independently evaluated loss decrease. Fixed 8192 contexts per law;
no optional stopping or dropped failures. Secondary negatives remain visible.
An empirical coverage diagnostic uses a known Gaussian second moment and 300
fresh repetitions, accepting coverage 0.90–0.99; it does not prove coverage for
every nonlinear endpoint. Solver feasibility, VI and objective comparisons must
also pass before interpreting mechanism results.
