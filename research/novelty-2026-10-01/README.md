# Bounded RASP novelty check — 1 October 2026

**Decision:** the exact coupled RASP update is **apparently distinct** in the
searched literature. This is enough to proceed with a working algorithmic
novelty claim. **Primitive overlap was found.** Retain the current method and
credit its precedents; no equivalent full update triggered replacement.

## Contract and stopping point

User request: one short literature check, stop when there is enough evidence,
and iterate if an equivalent method exists. Target: `theory.md` equations (1)–(2),
including simultaneous same-weight half-gradients, their mean and difference,
momentum, the vectorized rank-one penalty and the actual matrix operator-norm
ball. Names or abstracts alone do not decide equivalence.

Search ran approximately **12:24–12:33 UTC**, with **24 queries** recorded in
[the ledger](search-ledger.md). Coverage: general web discovery, primary arXiv
texts, NeurIPS proceedings, author manuscripts and official artifacts. Existing
[r001 evidence](../r001/evidence.md) supplies the earlier frontier. Stop reason:
the closest new equation was resolved; the final synonym queries mostly returned
unrelated uses of covariance, repeated clipping methods and temporal differences.
Further open-ended searching is not required for this working decision.

## Closest comparisons

These are **reported by source** method descriptions. The overlap judgments are
**inferred from sources**, without new training replication.

| Primary work | Operational overlap | Exact remaining difference |
|---|---|---|
| [Consensus gradient, §15.3, equations 15.10–15.12](https://www.cse.iitb.ac.in/~cs709/2015a/notes/readingAssignment/ImprovingOptByModelingUncertainty.pdf), Le Roux, Bengio, Fitzgibbon | Centered empirical covariance shrinks the mean gradient; two observations give RASP's rank-one covariance | No coupled matrix operator-ball minimization in the inspected method |
| [TONGA, NeurIPS 2007](https://papers.neurips.cc/paper_files/paper/2007/file/9f61408e3afb633e50cdf1b20de6f466-Paper.pdf) | Earlier uncertainty-based descent and efficient online low-rank covariance lineage | Historical precedent; not the specified paired, constrained matrix update |
| [Becker–Fadili–Ochs, Theorems 3.4/3.8](https://fadili.users.greyc.fr/Pub/bibtex/manuscript/higherorderFB.pdf) | General low-rank metric proximal calculus contains the scalar-root solver | Solver construction is prior mathematics |
| [SPECTRA v2, §3](https://arxiv.org/html/2603.14315v2) | Generic composite subproblem contains RASP's objective | Published wrappers do not instantiate the simultaneous difference penalty |
| [PoLoRA v1, §2.3, equations 11–14](https://arxiv.org/html/2607.17620v1) | Gradient second moments determine a preconditioned spectral LMO | Kronecker metric changes the constraint; product-aware LoRA updates, rather than RASP's centered rank-one decision penalty |
| [MONA v1, §4.1, Algorithm 1](https://arxiv.org/html/2605.26842v1) | Gradient differences modify a momentum input before polar approximation | Differences are temporal; acceleration is added linearly, without the replica risk objective |

### Exact equation check

The consensus-gradient chapter defines

\[
C=\frac1n\sum_i(g_i-\bar g)(g_i-\bar g)^T,
\qquad d=(I+C/(n\sigma^2))^{-1}\bar g.
\]

**Algebraic comparison:** set \(n=2\), \(g_1=\operatorname{vec}A\),
\(g_2=\operatorname{vec}B\), \(e=\operatorname{vec}(A-B)/2\). Then
\(C=ee^T\). With \(\beta=0\), RASP's inactive-constraint step is

\[
\operatorname{vec}D
=\mu^{-1}(I+(\gamma/\mu)ee^T)^{-1}\operatorname{vec}G.
\]

For \(\gamma>0\), choose \(\sigma^2=\mu/(2\gamma)\); the directions coincide
up to the step-size factor \(1/\mu\). Thus neither this shrinkage nor the
two-observation covariance is a new primitive. This maps existing equations;
it adds no new Lean theorem.

The remaining claim concerns the full **joint constrained choice**. The existing
proved 2×2 example in `theory.md` distinguishes that choice from shrinkage followed
by Euclidean spectral projection. Neither this distinction nor a generic
framework's containment proves publication significance by itself.

## One opportunity and its falsifier

Retain the coupled replica/spectral instantiation as the candidate contribution.
Its smallest existing discriminator is the 2×2 noncommutation example; r001
already preserves the numerical mechanism evidence and unfavorable laws.
The next practical uncertainty is the cost of the active solve. The strongest
failure reason is that its cost exceeds any useful directional improvement.

**Novelty falsifier:** a prior concrete optimizer with the same paired
observation and the same constrained quadratic, or an algebraically equivalent
full direction map. Finding it rejects this instantiation claim and requires a
new method revision, with dependent artifacts invalidated. Merely renaming a
known covariance update would not repair that failure.

## Limits and handoff

The Fed-SR publisher page returned HTTP 429 in the browser and HTTP 403 during
snapshot retrieval. Indexed publisher text
describes a differentiated gradient-norm penalty on the training objective,
which is a different optimization variable; record it as a screened lead with
limited access, rather than a fully inspected exclusion. Private, unpublished,
unindexed and non-English equivalents remain outside this bounded search.

MONA is an additional eligible discrete peer; PoLoRA is a LoRA comparator.
The [baseline addendum](baseline-addendum.json) preserves these discoveries
without editing the frozen r001 registry or pretending they were considered in
its execution. Incorporate MONA before the later comparison protocol freezes.
No all-peer training claim exists. Source snapshots and failed retrievals are in
[the follow-up manifest](source-manifest.json), separate from r001's manifests.
Only literature records and their dependent prose changed; the method, formal
claims and measured simulations retain their existing revision.
