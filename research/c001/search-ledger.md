# Bounded mechanism search — 2026-10-01

Sources: primary papers via arXiv/publishers, official optimizer code and a
dated comparator registry. The redesign considered broader noise, variance reduction
and temporal filtering queries, then narrowed to the following 13 mechanism
queries. The final narrow search ended around 14:19 UTC; no ongoing background
search is needed. Source retrieval followed for hashes.

| Query | Decision / useful lead |
|---|---|
| optimizer "independent" "validation gradient" "convex" combination | Validation is a known reliability device; no exact spectral library match found. |
| "optimizer" "portfolio" "confidence" gradients | Portfolio and confidence weighting are broad prior mechanisms; inspect exact operational update. |
| "stochastic" "line search" "empirical Bernstein" | Stochastic line-search confidence precedes this work; step acceptance alone is not novelty. |
| "gradient" "disagreement" "subspace" optimizer noise | Worker Disagreement, May 2026: close subspace-filtering precursor. |
| stochastic optimization "convex combination" "validation" optimizers | Statsformer and classical aggregation lineage: oracle inequality is established math. |
| "optimizer" "holdout" "confidence" spectral | No equivalent update retrieved; query absence is weak evidence. |
| "Muon" "jackknife" | No usable equivalent found; nonlinear debiasing branch remains unproved. |
| "spectral" "shrinkage" "sample splitting" gradient optimizer | Statistical shrinkage and splitting are old components. |
| "stochastic line search" "independent" confidence gradient direction interpolation | Related adaptive-sampling/reliability literature; not a spectral replica certificate. |
| "optimizer" "certified" "spectral" "replica" | No exact composition retrieved. |
| empirical covariance trace "kurtosis" "Chebyshev" relative confidence | Elementary moment bound; bounded-kurtosis sharp-tail paper is an unimplemented lead. |
| optimizer "spectral" "Chebyshev" "validation" | Mostly unrelated spectral approximation hits; no equivalent optimizer. |
| gradient optimizer "pairwise interpolation" confidence covariance | No equivalent final decision retrieved. |

Closest papers were opened at the relevant methods/theory, not judged from a
title. Statsformer section 4 and worker-gap sections 3–4 delimit novelty; Muon
noise and MARS-M refresh the competitor boundary. Full historical consensus,
TONGA, BFO, SPECTRA and MONA records are in the primary source manifest.
Not an exhaustive systematic review. Citation chaining, non-English work,
unindexed code and alternate formalizations remain coverage gaps.
