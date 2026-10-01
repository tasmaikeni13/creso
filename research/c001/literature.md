# Frontier and mechanism decisions — 1 October 2026

## Answer to the research contract

CRESO's exact four-vertex, two-trace calibrated spectral decision was not found
in the bounded searches below. This supports **apparently distinct composition**,
not a proof of absence or extreme novelty. The mathematical tools are established.
The prospective contribution is a complete adaptive confidence contract for a
replica-derived spectral update, with a finite solver and explicit statistical
cost. Our simulations test that contract and its narrow intended regime.


## Closest primary work and exact differences

| Primary work | Mechanism and regime | Consequence for CRESO |
|---|---|---|
| [Consensus gradient / TONGA chapter](https://www.cse.iitb.ac.in/~cs709/2015a/notes/readingAssignment/ImprovingOptByModelingUncertainty.pdf), equations 15.10–15.12 | Noise covariance produces inverse-metric shrinkage; rank-one specialization supplies a known shrinkage operation. | Noise deflation is prior art. TONGA-style sketch inversion is a mandatory local control. |
| [Worker Disagreement Reveals Sharp Directions in Local SGD](https://arxiv.org/html/2605.27739v1), sections 3–4, Appendix C | Local parameter gaps estimate a curvature/noise subspace; filtering this span has preliminary training evidence. Gaps are collected at different weights after local steps. | Replica-subspace filtering is not new. CRESO uses same-weight gradient differences and independently calibrated in-span/residual traces. The connection to Hessian geometry is a hypothesis, not transferred as a theorem. |
| [Statsformer](https://arxiv.org/html/2601.21410v1), section 4 | Validation and convex aggregation protect against unreliable candidates in supervised prediction; oracle inequalities are classical. | Including a null candidate and validating a library is established. CRESO's in-library oracle inequality is an optimizer instantiation, not a new aggregation principle. |
| [Adaptive Sampling Strategies](https://arxiv.org/abs/1710.11258) | Inner-product and orthogonality tests control stochastic gradient reliability and sample size. | Certified stochastic directions precede this project. CRESO fixes an oracle budget and selects spectral candidates; no new concentration principle is claimed. |
| [Kalman Gradient Descent](https://arxiv.org/abs/1810.12273) | Estimates latent gradients and uncertainty through temporal filtering. | Temporal filtering is a separate discarded branch; CRESO does not inherit a state-space calibration guarantee. |
| [MARS-M](https://arxiv.org/html/2510.21800v3) | Variance reduction combined with Muon matrix updates. | Add the actual MARS-M variant to the future peer inventory; generic MARS or a SPECTRA wrapper is not a substitute. |
| [Muon under gradient noise](https://arxiv.org/html/2609.32861v1) | Studies noisy orthogonalization and regimes where a polar update can be harmful. | The rank-one orthogonal-noise witness is motivated by an established limitation. Our 1/8 matrix gap and simulations do not establish a new universal lower bound for Muon. |
| [BFO](https://fadili.users.greyc.fr/Pub/bibtex/manuscript/higherorderFB.pdf), [SPECTRA](https://arxiv.org/html/2603.14315v2) | Composite spectral optimization and related proximal machinery. | CRESO solves a finite union of feasible segments rather than a full composite proximal problem. Generic composite containment is not evidence of an equivalent confidence estimator. |
| [Exact worst-case tail under bounded kurtosis](https://arxiv.org/abs/2607.05226) | Stronger moment-tail analysis is a possible calibration lead. | CRESO deliberately uses elementary Chebyshev bounds. This abstract-level lead is not a checked implementation or a novelty claim. |

Source claims above are source-reported; the full local study is independent
synthetic evidence. Source hashes and retrieval failures are in
`source-manifest.json`; the primary comparator registry is standalone.

## Candidate portfolio and selection

| Branch | Prediction | Main rival explanation / kill criterion | Disposition |
|---|---|---|---|
| Rank-k replica proximal metric | Better noise representation than rank one. | TONGA already supplies covariance shrinkage; richer sketch alone does not repair adaptive estimation or nested spectral solves. | Retained as a control, rejected as the main novelty claim. |
| Certified interpolation of frozen spectral candidates | Confidence remains valid after validation-dependent selection; restoration helps when deflation deletes signal. | Generic aggregation is known; low-rank gains may all come from old deflation; calibration can be too conservative. | Selected; all three limitations are explicitly tested. |
| Jackknife / debiased nonlinear polar maps | Less orthogonalization bias. | Feasibility after correction and singular-gap behavior unresolved; jackknife itself is old. | Unexecuted research branch, not a failed measured experiment. |
| Temporal/Kalman filtering | Reuse information across optimizer steps. | Drift and momentum covariance require new assumptions; known filtering lineage. | Deferred; no theorem or execution claimed. |

## Nontriviality and potential

Actual rectangular matrix feasibility, exact finite optimization, adaptive
selection, and a covariance envelope that does **not** assume a learned subspace
contains all noise are substantive engineering and mathematical obligations.
The proof technique is elementary convexity plus moment bounds. No new general
optimization theory, sharp minimax bound or neural-training convergence theorem
has been obtained. The selected method is worth studying because it repairs a
specific statistical defect and exhibits active-constraint benefits; those
benefits alone cannot establish a breakthrough.

Novelty falsifier: an earlier same-weight replica method with a frozen feasible
library, calibrated projected/residual trace envelope and adaptive segment
selection equivalent after a parameter change. Continue from the closest sources
if such an example is supplied. Novelty does not become certain merely because
13 final mechanism queries and the source traversals did not find one.
