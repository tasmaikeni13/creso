# CRESO — Certified Replica Spectral Optimization

**Revision c001, 1 October 2026.** This is an experimental matrix decision rule.
The exact optimization and finite-law statistical lemmas are verified in Lean;
continuous Gaussian moment calculations are analytical; comparative results
come from controlled one-step simulations. Neural training is not executed.

## 1. Problem and information order

At weights W let g = ∇f(W) be an unknown population matrix gradient. A replica
G = g + ε has zero conditional mean noise and finite second moment. All samples
in a step are at **the same weights**. Proposal replicas are independent of the
post-proposal replicas; the latter are mutually iid conditional on W. Shared
replica noise, drift, bias and momentum are not covered by this model.

Work in real rectangular matrices with Frobenius inner product. The feasible set
is the actual Euclidean operator-norm ball

\[
\mathcal B_r=\{D\in\mathbb R^{m\times n}:\|D\|_{\rm op}\le r\},\qquad
q_g(D)=\langle g,D\rangle-\frac\mu2\|D\|_F^2,\quad \mu>0,\ r\ge0. \tag{1}
\]

The algorithm maximizes a certificate over a **finite union of segments inside
this ball**. It does not maximize q over the entire ball and does not solve the
a full composite proximal objective. The parameter update is W⁺ = W − ηD. An
L-smooth upper model gives f(W⁺) ≤ f(W) − ηq_g(D) when η≥0 and Lη≤μ.
The Lean descent result assumes that explicit upper model; global smoothness
and a convergence rate for a neural network are not proved.

## 2. Freeze proposals before validation

From eight proposal replicas form their mean M and four differences
Eₐ = (G₂ₐ − G₂ₐ₊₁)/√2. Vectorize the differences, take their leading right
singular vectors, and form the orthogonal projector P of rank at most four.
Write R = I − P. P may miss noise or contain signal; neither possibility is
assumed away. Use the four vertices

\[
D_0=0,\quad D_1=\mathcal R_r(M/\mu),\quad
D_2=r\,\operatorname{polar}(M),\quad D_3=\mathcal R_r(RM/\mu). \tag{2}
\]

Here polar uses the partial isometry on nonzero singular values, so polar(0)=0;
\(\mathcal R_r(A)=A\min(1,r/\|A\|_{op})\) with A unchanged when its norm is zero.
Every vertex is feasible. Radial scaling preserves P-orthogonality; Euclidean
singular-value clipping need not preserve a vectorized noise subspace.
All four vertices and P are frozen before any following data are observed.
The implementation discards relative sketch singular values below 10⁻¹⁰ and
polar singular values below 10⁻¹², with explicit floating-point tolerances.
Exact SVD identities and these numerical thresholds are not Lean-verified.

The formal guarded library radially repairs three arbitrary proposed matrices
and includes zero. It proves their feasibility and a feasible maximizing
interpolation without assuming that such a matrix decision exists. In the
ideal library, repairing D₂ is the identity because its operator norm is ≤r.
A production approximate polar must receive a justified norm guard.

## 3. Calibrate uncertainty without assuming subspace completeness

The next 512 replicas supply n_c=256 difference pairs
E=(A−B)/√2. Their covariance equals that of one replica. Let

\[
q_P=\mathbb E\|PE\|_F^2,\quad q_R=\mathbb E\|RE\|_F^2,
\qquad \widehat q_S={1\over n_c}\sum_a\|S E_a\|_F^2. \tag{3}
\]

Assume, conditional on the proposal data, for S=P,R,
Var(‖SE‖²) ≤ κq_S². For Gaussian replicas κ=2 suffices:
Var(‖SE‖²)=2 tr((SΣS)²)≤2 tr(SΣS)². This is a standard Gaussian quadratic-form
identity, an analytical assumption check here, not a new concentration theorem
or a formalized Gaussian probability space. A Student-t₃ law lacks the required
fourth moment. κ is a justified bound, never an optimistic fitted value.

With δ∈(0,1), define

\[
a=\sqrt{4\kappa/(n_c\delta)}<1,\qquad
U_S=\widehat q_S/(1-a). \tag{4}
\]

Chebyshev gives Pr(U_S<q_S)≤κ/(n_ca²)=δ/4; unioning the two traces costs δ/2.
If q_S=0 then the nonnegative squared norm is zero almost surely; handle this
case exactly rather than divide by zero. This needs n_c>4κ/δ (more than 160
pairs for κ=2, δ=.05). The executed protocol uses 256; a two-replica training
update does not inherit this certificate.

Orthogonal decomposition, Cauchy–Schwarz and (x+y)²≤2(x²+y²) give, for any
frozen candidate D,

\[
\mathbb E\langle\epsilon,D\rangle^2
\le 2(q_P\|PD\|_F^2+q_R\|RD\|_F^2)
\le V(D):=2(U_P\|PD\|_F^2+U_R\|RD\|_F^2). \tag{5}
\]

Cross covariance between the two spans is allowed. Residual noise is measured,
not assumed zero. The factor two and trace envelope are conservative, especially
in high dimension; no sharp directional covariance estimate is claimed.

All 640 post-proposal replicas (512 calibration replicas plus 128 extra) supply
v. Thus n_v=640. On the successful trace event, use K=4 vertex allowances

\[
b_j=\sqrt{2K\,V(D_j)/(n_v\delta)}. \tag{6}
\]

For each fixed vertex, iid mean variance is its replica variance divided by n_v.
Union Chebyshev bounds against **true**, proposal-conditional moments cost δ/2.
Union this error event with calibration failure: with probability at least 1−δ,

\[
|\langle v-g,D_j\rangle|\le b_j\quad\hbox{for every vertex }j. \tag{7}
\]

This proof does not condition a mean bound on the estimated trace. Calibration
statistics and v may be dependent because calibration pair sums are reused;
a union of the two failure events requires no independence between them.
Candidate independence from all these samples is essential. Zero-variance
vertices have exact zero error, including D₀. For finite positive-support laws,
Lean proves the moment bounds, zero-trace case and adaptive failure transfer.
The continuous-law version uses the same expectation/Markov argument on a
measurable conditional probability space; this extension is analytical, not
fully mechanized. The actual SVD proposal map is numerical, not proof extraction.

## 4. Optimize the certified finite decision

For every pair i≤j and t∈[0,1], set

\[
D_{ij}(t)=(1-t)D_i+tD_j,\qquad
J_{ij}(t)=\langle v,D_{ij}(t)\rangle-\frac\mu2\|D_{ij}(t)\|_F^2
-[(1-t)b_i+tb_j]. \tag{8}
\]

The uncertainty term is affine in the mixing weights because vertex errors
are controlled simultaneously. No selected-direction covariance estimate is
asserted unbiased. Convexity of the operator ball makes every mixture feasible.
Set Δ=D_j−D_i. Then

\[
J_{ij}(t)=q_v(D_i)-b_i+A_{ij}t-\frac{Q_{ij}}2t^2,\quad
A_{ij}=\langle v-\mu D_i,\Delta\rangle-(b_j-b_i),\quad
Q_{ij}=\mu\|\Delta\|_F^2. \tag{9}
\]

For Q>0 the exact maximizer is clip(A/Q,0,1). For Q=0 choose t=0 when A≤0
and t=1 otherwise. Enumerate the ten unordered pairs; choose the maximum with
lexicographic ties. Zero is available with certificate zero. The float64
reference resolves ties within 10⁻¹⁴ and treats Q≤10⁻²⁴ as degenerate; the
independent scalar optimizer checks its resulting tolerance, not exact arithmetic.
No nested spectral projection root is needed.

On event (7), for the selected mixture \(\widehat D\),

\[
q_g(\widehat D)\ge J(\widehat D)\ge0,\qquad
q_g(\widehat D)\ge\max_j\{q_g(D_j)-2b_j\}-\varepsilon_{\rm solve}. \tag{10}
\]

These are **current-state in-library** guarantees. They do not compare to an
optimizer using a stronger full-data gradient or prove dominance of another
training trajectory. Only two-vertex mixtures are searched; a full simplex
aggregate can be better. Selection and interpolation may depend arbitrarily on
v and the estimated bounds because (7) is simultaneous over frozen vertices.

## 5. A nontrivial active matrix witness, and a failure witness

For g=diag(1,0), replica noise along diag(0,1), exact noise deflation recovers g.
At r=.5 and μ=1 the deflated update diag(.5,0) has progress 3/8. The ideal polar
update on a nonzero noisy full mean is diag(.5,±.5), with progress 1/4.
The difference is **1/8**, while both matrix operator norms equal .5. Lean
verifies the positive-sign matrix example; the negative-sign case has the same
norm and squared penalty. This is a genuine constrained matrix comparison,
not a scalar replacement. Ordinary deflation and TONGA-style shrinkage also
recover this regime; its gain does not isolate CRESO's validation contribution.

Independence cannot be deleted. If every replica shares the same random ±diag(1,0)
noise and g=0, all differences vanish while v contains the common noise.
The false zero envelope certifies diag(±.5,0) with J=3/8, but true progress is
−1/8. Lean verifies this harmful matrix certificate, and the numerical attack
fails in every draw. Marginally unbiased replicas are insufficient.

## 6. Executed evidence, cost and research claim

[The frozen study](research/c001/results.md) has 49,152 final contexts, 12 laws,
13 tuned methods and two additional controls. Each tuned method gets 24
configuration evaluations on separate development data. Every baseline may
average all 648 method replicas, versus CRESO's eight proposal and 640 validation
replicas. Population labels only assess methods and select development configs;
final method decisions never receive g or Σ. An independent assessment set
checks noisy progress. Seeds 42–44 remain unused.

All nine prespecified primary contrasts pass a 0.01 minimum adjusted effect:
CRESO versus ideal Muon, feasible float64 NS5 and hard spectral projection in
three orthogonal-noise shapes. All those CRESO steps have active constraints.
Mixed-signal validation improves over unconditional deflation. TONGA-style
shrinkage ties CRESO on these clean cases; CRESO loses in other laws, including
signal/noise overlap and high isotropic noise. There is no all-peer claim.
Muon source bf16 parity and complete optimizer trajectories await Phase 03.

The reference uses three matrix SVDs and one 4×(mn) sketch SVD per decision, plus
streamable calibration contractions and ten scalar solves. The two mean-related
matrix SVDs can share a factorization; that optimization is not implemented.
The statistical stage has substantial gradient, state and communication cost.
At least 161 calibration pairs are needed by this elementary bound. No TPU
speed, memory advantage or scalable training benefit is established.

Literature checks found no equivalent **complete** composed update in their
bounded scope. Noise shrinkage, subspace filtering, confidence selection,
convex aggregation and scalar quadratic optimization are prior mechanisms.
The generic oracle proof is standard. CRESO's potentially publishable delta is
an explicit calibrated spectral decision with checked adaptive mathematics and
reproducible positive and negative cases. Extreme novelty, high impact and a
breakthrough remain **unestablished**. See [the frontier audit](research/c001/literature.md).
