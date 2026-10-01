# RASP: Replica-Aware Spectral Proximal optimization

**Research specification · updated 1 October 2026.** The exact per-step mathematics below is
proved in [Lean](formal/README.md). Training performance and publication novelty
remain hypotheses.

## 1. Problem and proposed mechanism

An update can have bounded spectral norm while following an unreliable gradient
direction. Recent methods already address spectral clipping, smoothing and
variance adaptation; these primitives are established
([MuCon](https://arxiv.org/abs/2605.26459),
[Variance-Adaptive Muon](https://arxiv.org/abs/2601.14603)).
RASP proposes to put **simultaneous gradient disagreement inside the constrained
direction choice**. It transfers the mean–variance decision structure of
[Markowitz](https://traders.studentorg.berkeley.edu/papers/Markowitz.pdf)
to a matrix update with a spectral budget.

For a matrix parameter, split the same global batch into two equal groups,
compute averaged gradients $A_t,B_t$ at the same weights, and define

$$
G_t=(A_t+B_t)/2,\qquad E_t=(A_t-B_t)/2,\qquad
M_t=\beta M_{t-1}+(1-\beta)G_t,\quad M_0=0.
\tag{1}
$$

Use $0\le\beta<1$, without momentum bias correction. For $\mu>0$, $\gamma\ge0$
and $r\ge0$, let $K_r=\{D:\|D\|_{\mathrm{op}}\le r\}$ and choose

$$
\boxed{D_t=\arg\min_{D\in K_r}
Q(D),\quad Q(D)=\frac\mu2\|D\|_F^2+
\frac\gamma2\langle E_t,D\rangle_F^2-\langle M_t,D\rangle_F,\qquad
W_{t+1}=W_t-\eta_tD_t.}
\tag{2}
$$

Here $\langle A,B\rangle_F=\sum_{ij}A_{ij}B_{ij}$. The quadratic disagreement
penalty has rank at most one in **vectorized parameter space**; $E_t$ can be a full-rank
matrix. The penalty measures one observed disagreement direction, not the whole
noise covariance. Weight decay and nonmatrix parameters are outside this theorem.

## 2. Why disagreement is relevant—and its limit

For independent identically distributed finite-support centered errors $a,b$,
write $A=g+a$, $B=g+b$. For any direction $U$ fixed independently of the draws,

$$
\mathbb E\langle E,U\rangle_F^2
=\mathbb E\langle G-g,U\rangle_F^2
=\tfrac12\mathbb E\langle a,U\rangle_F^2.
\tag{3}
$$

Lean proves the finite weighted double sum with joint mass $p_ip_j$.
This is **not an unbiased-risk theorem for the adaptive $D_t$**, nor an estimator
identity for momentum noise. Correlated or unequal batches need a revised model.
Phase 02's finite iid ±1 arithmetic example computes a realized adaptive
surrogate of zero and factorized fresh risk 1/4; its averages are Lean proved in
[StatisticalExamples.lean](formal/Rasp/StatisticalExamples.lean).

## 3. Exact guarantees

Suppress $t$. The solution exists and is unique for every rectangular real matrix,
including singular inputs. It is characterized by

$$
\langle\mu D+\gamma\langle E,D\rangle_FE-M,V-D\rangle_F\ge0
\quad(V\in K_r).
\tag{4}
$$

Consequently $\langle M,D\rangle_F\ge\mu\|D\|_F^2+
\gamma\langle E,D\rangle_F^2$, and $M=0$ gives $D=0$.
For solutions $D,V$ at signals $M,N$ with **the same $E,\mu,\gamma,r$**,

$$
\mu\|D-V\|_F^2+\gamma\langle E,D-V\rangle_F^2
\le\langle M-N,D-V\rangle_F,\qquad
\mu\|D-V\|_F\le\|M-N\|_F.
\tag{5}
$$

There is no singular-value-gap assumption. Increasing $\gamma$ while fixing
$M,E,\mu,r$ weakly decreases $\langle E,D\rangle_F^2$; swapping the two
replica groups leaves the solution unchanged. These statements control the
realized surrogate, without promising lower population variance.

If $\eta\ge0$, $\|g-M\|_F\le\delta$, and the loss satisfies the quadratic upper
model $f(W-\eta D)\le f(W)-\eta\langle g,D\rangle_F+
(L\eta^2/2)\|D\|_F^2$, then

$$
f(W-\eta D)\le f(W)-\eta\big[(\mu-L\eta/2)\|D\|_F^2+
\gamma\langle E,D\rangle_F^2-\delta\|D\|_F\big].
\tag{6}
$$

This conditional one-step bound does not establish stochastic convergence.

## 4. Coupled solver

Let $P_{K_r}$ be the Frobenius projection. Define

$$
D(z)=P_{K_r}((M-zE)/\mu),\qquad
F(z)=z-\gamma\langle E,D(z)\rangle_F.
\tag{7}
$$

There is exactly one root $z_\star$, and $D(z_\star)=D_t$.
For $b\ge a$, $F(b)-F(a)\ge b-a$; with **exact projections**,
$\mu\|D(z)-D_t\|_F\le|F(z)|\|E\|_F$.
The scalar reduction specializes known low-rank proximal calculus
([Becker–Fadili–Ochs, Theorem 3.8](https://fadili.users.greyc.fr/Pub/bibtex/manuscript/higherorderFB.pdf)).
Lean specifies the projection variationally. Phase 01 adds approximate
certificates in [Approximation.lean](formal/Rasp/Approximation.lean): if
`||Dhat-D(z)||F≤εp` and `|z-γ<E,Dhat>|≤εf`, then
`μ||Dhat-Dstar||F≤μεp+(εf+γ||E||F εp)||E||F`. Feasibility is separate.
For a feasible ε-VI point, the objective gap is at most ε and
`μ||Dhat-Dstar||F²≤ε`. A residual error bound τ enlarges the VI tolerance
by τ times a feasible diameter. The actual matrix ball permits radial repair
using a certified operator upper bound. None of these theorems verifies numerical
SVD or bf16 arithmetic. Exact bracket signs give dyadic bisection termination;
uncertain computed signs require the residual certificate instead.

Coupling matters: with $\mu=\gamma=r=1$, $M=\operatorname{diag}(3,1)$ and
$E=\operatorname{diag}(1,1)$, the unconstrained solution is
$\operatorname{diag}(5/3,-1/3)$. Its Frobenius projection is
$C=\operatorname{diag}(1,-1/3)$, but (2) gives $D=\operatorname{diag}(1,0)$,
with $Q(C)-Q(D)=1/9$. All three optimization claims are proved over actual
$2\times2$ matrices.

## 5. Contribution boundary

The proposed contribution is the specific split-gradient quadratic penalty
coupled to spectral feasibility. [SPECTRA](https://arxiv.org/abs/2603.14315)
already supplies a general composite framework broad enough to contain this
objective. The projection, proximal solver, strong convexity and mean–variance
principle are prior mathematics. No equivalent instantiated update was found in
the [searched corpus](phases/research-record.md); absolute novelty is unverified.

The split reuses the same tokens but adds gradient storage/communication.
Repeated projections may be too expensive. $\mu,\gamma$ require scale calibration;
loss-scale invariance is not claimed. Rank-one noise coverage and adaptive
estimation may make RASP worse than simpler clipping. The phases must test these
failure modes before any claim of better loss, speed or memory use.

## 6. Executed mechanism evidence

Phases 01–02 executed on 2026-10-01; see the [full report](research/r001/results.md).
A preregistered rotating rank-one Gaussian quadratic law supports a directional
benefit over γ=0, shuffled disagreement and equal-norm random disagreement at
the same update norm and stepsize. The independent loss-decrease contrast over
γ=0 is 0.11505, with adjusted interval [0.10269,0.12742]. This is a controlled
one-step simulation with unusually informative disagreement, not training.

Adaptive risk is biased, dependent replicas can harm, and active spectral solves
are expensive. A full peer registry/parity, certified TPU kernel and matched
language-model comparison still require their later phases. The occupied
primitives and apparently distinct instantiation boundary remain unchanged.
