# Frozen peer definitions and facet comparison — 2026-10-01

These are source-reported definitions, not parity-certified implementations.
`competitors.json` lists distinct eligible update IDs. Phase 03 must port the
pinned discrete code and verify tensors, state, orientation, groups and decay.
No source training result supplies a performance ranking on our future protocol.

## Notation and common conventions

G is the ordinary minibatch gradient; M is a momentum buffer; all products in
moment estimates and divisions are entrywise unless stated otherwise.
`P_c(X)=U diag(min(s_i,c)) Vᵀ` is exact Frobenius projection onto the actual
operator ball; `H_c(X)=U diag(c s_i/sqrt(c²+s_i²)) Vᵀ` is soft clipping.
`polar₀` preserves nonzero singular vectors and sets null singular modes to zero;
an arbitrary thin-SVD completion at rank deficiency is a different specification.
`NS_K` is an actual finite polynomial map, not `polar₀`.
`RMS(X)=||X||F/sqrt(mn)`. Unless noted, zero buffers initialize moments and
decoupled decay gives `W+ = (1-ηλ)W - ηU`. Group policy is source-specific.

## Controls and matrix families

| Definition ID | Discrete update and state | Primary authority / parameter groups / cost |
|---|---|---|
| adamw | `M=β1 Mprev+(1-β1)G`, `V=β2 Vprev+(1-β2)G²`; `U=(M/(1-β1^t))/(sqrt(V/(1-β2^t))+ε)` | [AdamW](https://arxiv.org/abs/1711.05101); all groups, typically no decay for gains/biases; 2N moments |
| sgdm | `M=β Mprev+(1-β)G`; U=M; source Nesterov branch uses `(1-β)G+βM` | Pinned Muon momentum convention and standard momentum control; N state |
| muon-ns5 | Same EMA; Nesterov input `(1-β)G+βM`. Orient small dimension as rows, normalize by Frobenius norm+1e-7, perform five steps `X←aX+(bXXᵀ+c(XXᵀ)²)X`, coefficients `(3.4445,-4.775,2.0315)`. Undo transpose; scale `sqrt(max(1,m/n))` | [KellerJordan pin](https://github.com/KellerJordan/Muon/tree/f98f1cacc0263b04290753e32be8d498c1efc806). Hidden matrices; auxiliary AdamW for embeddings/head/gains. bf16 code, O(KNq) |
| muon-polar | Same momentum/groups but `NS5` replaced by `polar₀`; diagnostic exact geometry | Exact ideal differs from finite polynomial; rank-zero behavior explicit, O(Nq) SVD |
| shampoo | `L=εI+Σ GGᵀ`, `R=εI+Σ GᵀG`; matrix update `L^(-1/4) G R^(-1/4)` (tensor order controls exponent); practical blocked/momentum/grafting variants must be separately pinned | [Gupta et al., Algorithm 1](https://proceedings.mlr.press/v80/gupta18a.html). O(m²+n²) state, periodic eigensystems. Include standard faithful distributed/block implementation in Phase 03 |
| soap | Accumulate EMA of GGᵀ,GᵀG; periodically refresh eigenspace bases QL,QR via eigensolve/QR. Rotate G to `g'=QLᵀGQR`, apply Adam moments in that basis, rotate update back. Reproject state when basis changes | [SOAP v2](https://arxiv.org/html/2409.11321v2), [pin](https://github.com/nikhilvyas/SOAP/tree/a1e553530fde97d0e6b307d7c82ac6d38b072340); first-step skip, max dimension and 1D policy in code; 2N plus matrix stats/bases |
| adamuon-v1 | EMA M; `O=NS_K(M)`, `V=β2 Vprev+(1-β2)O²`; bias-correct V, divide O by sqrt(Vhat)+ε; rescale to RMS 0.2 | [v1 Algorithm 1](https://arxiv.org/html/2507.11005v1). Hidden matrices+AdamW fallback. 2N state |
| adamuon-v3 | `M=β Mprev+G`; `O=NS_K(sign(M))`; `V=β Vprev+(1-β)O²`; `U=0.2 sqrt(mn) (O/(sqrt(V)+ε))/||O/(sqrt(V)+ε)||F`, no v1 bias correction | [v3 Algorithm 1](https://arxiv.org/html/2507.11005v3). Newest variant; zero denominator requires explicit numerical handling in Phase 03 |
| normuon | O from actual Muon/PolarExpress routine; row state `v=β2 vprev+(1-β2)mean_cols(O²)`; `Y=O/(sqrt(v)+ε)`; `U=Y ||O||F/||Y||F` | [NorMuon](https://arxiv.org/html/2510.05491v1), [Dion pin](https://github.com/microsoft/dion/tree/7692479288f928a3d61d1cc58137b4dbe4f71000). Row normalization in fp32; split matrices / LR scales preserved; N+rows state |
| muon-nsr, muon-vs | `Γ=βΓprev+β(1-β)(Mprev-G)²`, `M=βMprev+(1-β)G`; hats divide by `1-β^t`; `T=G+β/(1-β) Mhat`. NSR input `T/(sqrt(T²+αΓhat)+ε)`, VS input `T/(sqrt(Γhat)+ε)`. Then NS_K and source shape scale | [Variance Muon v2 Algorithm 1](https://arxiv.org/html/2601.14603v2), EMNLP pin. Distinguish source small-gradient amplification from actual clipping. β=0/1 and ε placement need code parity; 2N moments |
| muon-nsr-post | Same statistics but `O=NS_K(T)`, `U=O/sqrt(1+αΓhat/(T²+ε))` | v2 Algorithm 2, named reshuffled post-order diagnostic; algebraically distinct from pre-order algorithm |
| deva-spectral-paper | EMA L,R; QL,QR refreshed periodically; `G'=QLᵀGQR`, `M'=β1Mprev'+(1-β1)G'`; row norms r, column norms c of M'; `V=β2Vprev+(1-β2)rcᵀ`; `Γ=(V/(rcᵀ+ε))^(-1/2)`; `U=QL [0.2 sqrt(max(m,n)) Γ⊙polar(M')] QRᵀ` | [DeVA v2 Algorithm 2](https://arxiv.org/html/2602.06880v2); rotates back explicitly. Finite code uses NS, not exact polar; matrix states plus moments |
| deva-spectral-code | Pinned `optimizers/deva.py`: first-step skip; Nesterov input after accumulating M'; quarter-power row/column factors divided by sqrt(V+ε); Adam-style bias multiplier; basis updates after parameter update; decay applied to updated W | [pin](https://github.com/Tsedao/Decoupled-Variance-Adaptation/tree/2e4d26ef8d44903099f694875264316fd9143ef2). Distinct order and numerical contract, not silently equated to paper |
| deva-memory, deva-instant | Algorithm 3 replaces EMA outer product by product of EMA row/column norms; Algorithm 4 uses row/column norms of G' instead of M' | DeVA v2 appendices; separate variants, never discard memory variant because different fidelity is convenient |
| mucon | `U=P_τ(M)`, with τ from the source SpectralP shape/scaling parameterization; projection clips large singular values, preserves smaller ones | [MuCon §§2–4](https://arxiv.org/html/2605.26459v1). Its polar/absolute-value rational filter is not automatically a certified SVD-free algorithm. Reference exact clipping and practical approximation must be distinguished |
| musec, softmusec | First input `Mhat_0=G0`; subsequently `Mhat_t=(1-βsrc) Mprev + βsrc Gt`. Store `M=P_c(Mhat)` or `M=H_c(Mhat)` and use U=M. Practical H uses coupled NS inverse square root; clipping feeds into future momentum | [Musec v2 Algorithms 2–4](https://arxiv.org/html/2609.11655v2). Source β is new-gradient coefficient, unlike RASP. Soft NS5 and exact H diagnostics differ; N state |
| aro-sign, aro-sink, aro-adam | `M=EMA(G)`; `R=QR(M f(RprevᵀM)ᵀ)`; `U=R f(RᵀM)`. f=entrywise sign, alternating row/column norm normalization (source SinkGD iteration budget), or source momentum-first Adam map. Full-model vs hybrid groups and QR/shifted-Cholesky-QR alternatives are source variants | [ARO Eq.4, §§3–5](https://arxiv.org/html/2602.09006v1). R0=I; base f state, rotation dimensions and ε are part of definition. O(m²) rotation state; no claim that eigen rotation is equivalent |

## Frameworks, distributed and newly retrieved families

| Definition ID | Exact operational delta | Primary authority |
|---|---|---|
| spectra-framework-{adamw,sgdm,signum,ademamix,mars} | Apply optional P/H to G before the base map; postprocess base direction U with `αH_c(U)` (or exact P diagnostic). Weight update `(1-ηλ)W-ηαH_c(U)`; source wrapper recovers direction from weight difference, subtracting decay | [SPECTRA v2 §5, Algorithm 1](https://arxiv.org/html/2603.14315v2), [official pin](https://github.com/mlolab/llm-spectral-clipping/tree/ed9df11d797aa94f312f4d7810d5f8cd8ddc9897). Freeze pre/post configuration in Phase 04; do not select only SGDM when adaptive variants are eligible |
| signum | EMA M, U=sign(M) | SPECTRA source base; scalar sign is not matrix polar |
| ademamix | `m1=EMAβ1(G)`, `m3=EMAβ3(G)`, `v=EMAβ2(G²)`; `U=(m1hat+αm3)/(sqrt(vhat)+ε)` with source warmup schedules for α,β3 | `src/optim/ademamix.py` at SPECTRA pin. Include base plus wrapper; 3N moments |
| mars | Correct gradient `C=G+αβ1/(1-β1)(G-Gprev)` (paper approximate variant); source clipping then Adam/Muon-style branch; state includes previous gradient | `src/optim/mars.py` at SPECTRA pin. Published choices and code finite filtering must be recorded separately in Phase 03 |
| spectra-spike | `M=μMprev+G`; estimate top k triplets; `T=M-Uk diag(sk) Vkᵀ`; `σtail=sqrt(||T||F²/(q-k))`; `O=T+σtail UkVkᵀ`; U=0.2O/(RMS(O)+ε) | [Spectra ICML Algorithm 1](https://proceedings.mlr.press/v306/huang26d.html), [official repo](https://github.com/kimmichtank/spectra/tree/b41c9c893f709b35613c6ad5c3e8025b21bbf180). Final proceedings PDF inspected and hashed; same tail rule, explicit ε denominator. k<q required; cached power iteration |
| dion | Add G to M; `P=qr(MQ)`, `R=MᵀP`; feedback `M←M-(1-μ)PRᵀ`; `Q←column_normalize(R)`; U=PQᵀ with source rectangular scale | [Dion simple/reference at pin](https://github.com/microsoft/dion/tree/7692479288f928a3d61d1cc58137b4dbe4f71000). Low-rank basis plus full feedback M |
| dion3-plain, dion3-nor | Add G to M; select k=ceil(f rows) by row L1 norm; O=finite polar routine on selected submatrix. Optional NorMuon row normalization and Frobenius norm restoration. Update selected W rows; selected M rows retain μ times their previous accumulated values, unselected retain error feedback | [Dion3 Algorithm 4](https://arxiv.org/html/2608.11612v1), pinned `dion2.py`, `nordion2.py`. Include f=1 control and f=1/4,1/8 within equal HPO; normalized variant is `Dion3=NorDion2` code alias. Decay all W rows |
| optmuon-a, optmuon-i | `αt=ρt-1`, `ρt=((1+max_i≤t ||Gi||²)/(1+Σ_i≤t ||Gi||²))^q`. A: q=1/2, `M=G+(1-α)Mprev`, `h=min(α²,α/sqrt(1+Σ αj||Mj||²))`. I: q=2/3, `M=(1-α)(Mprev-grad(Wprev;ξt))+G`, `h=min(sqrt(α),1/sqrt(1+Σ αj^(-1/2)||Mj||²))`. U=`h||M||F polar(M)` | [OptMuon v2 Algorithm 1](https://arxiv.org/pdf/2606.08783v2). ρ0=1, M0=0, W0=W1. I has two gradient evaluations on the same samples; charge work separately. No official code found; v1's monotone tracker is not v2 |
| newton-muon | EMA/Nesterov source M, input-second-moment ZZT with damping/update schedule; U=`polar(M(ZZT)^(-1))` or its pinned finite NS implementation | [paper](https://arxiv.org/html/2604.01472v1), [official code pin](https://github.com/zhehangdu/Newton-Muon/tree/df78af0db523d8bceb25af4919a3e3e7082b80f3). Extra layer input statistics and solves, not replica covariance |
| softsignum, softmuon | EMA M. SoftSignum U=tanh(τt M) entrywise; SoftMuon U=`M(MᵀM+τt^(-2)I)^(-1/2)`. Source quantile/MAD temperature schedule after sign phase, τ≥1 | [Softsign Algorithms 1–3](https://arxiv.org/html/2605.31371v1), [official code](https://github.com/brain-lab-research/softsign). Smooth bounded maps already exist |
| htmuon-svd, htmuon-ns, htmuon-ht | Source EMA M. SVD variant U=`U diag(si^p) Vᵀ`, 0<p<1; NS variant multiplies NS5(M) by the source approximate Gram root `(MᵀM)^(p/2)`; HT replaces singular values by `i^(-α)` | [HTMuon v2 Algorithms 3–6](https://arxiv.org/html/2603.10067v2), [code](https://github.com/TDCSZ327/HTmuon). Source rectangular scale, matrix-root normalization and symmetrization retained |
| namo, namo-d | EMA M. NAMO tracks scalar v=EMA(||G||F²); U=`sqrt(1-β2^t)/(1-β1^t) ||M||F polar(M)/(sqrt(v)+ε)`. NAMO-D tracks column-norm squares; compute similarly bias-scaled column-norm ratios d, clamp each to `[c mean(d),mean(d)/c]`, U=polar(M)diag(dclamped) | [NAMO v2 Algorithms 1–2](https://arxiv.org/html/2602.17080v2), [official code](https://github.com/minxin-zhg/namo). Norm-only vs column noise adaptation are distinct |
| distance-adaptive, scale-calibrated, distance-free | Adaptive: radius `rbar=max(rbar,||W-W0||)`, η=rbar/sqrt(k+1), EMA, norm LMO. Calibrated: `η=(||M||dual-||G-M||dual)+/L`, same LMO. Free: scalar distance certificate and recentered 1D majorized radius solve, exact Eqs.3–7 and Algorithm 3 | [Distance-aware Muon](https://arxiv.org/html/2605.18999v1). Gradient/error/trajectory observability and L differ; no transfer of deterministic theorem to stochastic training |
| deflated-muon-ns, deflated-muon-pe | Approximate top triplets; when sr<τs1, remove k modes si>τs1, normalize remainder by its Frobenius norm, reinsert head at 1/γ; apply original finite NS5 / PolarExpress polynomial. Otherwise ordinary routine | [Deflation Algorithms 1,3](https://arxiv.org/html/2609.21102v1), [code pin](https://github.com/ComputationalRobotics/Spectral-Deflation/tree/1eb15ce3fe39c2ebd168a33db0d9d72c897dc1e3). Both maps eligible; cost includes randomized sketch and grouping |
| adaptive-ns-muon | Periodically use measurement routine, record Gram spectral moments, fit ESD in background, select current polynomial routine from source candidate set; apply chosen routine to momentum between refreshes | [Adaptive NS Algorithm 1](https://arxiv.org/html/2609.33047v1). Auxiliary fit and scalar reductions are counted; exact routine/candidates are paper-defined, no official release located |
| physical-muon-dense, physical-muon-probe | Reset X=0; Mhat=Nesterov momentum/scalar normalization. Dense Euler `X←cliprails[X+h(Mhat-XXᵀMhat)]`; probe mean of K writes `h(Mhat v-XXᵀMhat v)vᵀ`, v iid Rademacher, T iterations. Use X as Muon update | [Physical Muon Eqs.3–4](https://arxiv.org/html/2609.37525v1). Actual published discrete algorithm; continuous equilibrium and Euler are distinct; charge KT probes and reset state |

Distance-free exact scalar definition (source Eqs.3–7):
`S+=ωG`, `B-=ω<G,W-W0>`, `d=max(d,B+/||S||dual)` (zero ratio when S=0);
`y=W-W0`, `s=argmin_{||s||≤1}<M,s>`, `z(R)=W0+(1-β)y+βRs`.
Choose R≥0 to minimize
`f(W)+β<G,Rs-y>+Lβ²||Rs-y||²/2+Msrc βL||(1-β)y+βRs||²`
`+ρLβ²||Rs-y||²+λLβ²(R-d)²/2` and set W+=z(R).
The paper's training implementation instead uses a capped product-Frobenius
proxy, with a no-center variant selected in its source diagnostic. Preserve that
discrepancy and the cap/grid/smoothing search in Phase 03; the deterministic
norm-generic theorem does not automatically cover the stochastic proxy.

## Facets that decide equivalence

RASP observes **two same-weight, equal iid gradient group means**, estimates the
vectorized rank-one operator `E⊗E`, and minimizes a strongly convex objective
inside the spectral ball. It has one persistent matrix momentum and a transient
disagreement. The optimizer chooses D through a coupled metric projection.

Muon-NSR/VS use temporal, coordinatewise deviations before polar filtering;
AdaMuon/NorMuon use post-filtered element/row second moments; DeVA uses rotated
structured statistics; Shampoo/SOAP use accumulated row/column geometry.
None of these inspected instantiations solves the specified simultaneous
rank-one risk objective. This is an operational comparison, not a claim that
they are statistically weaker. Their richer or cheaper observations may win.

SPECTRA's **generic composite subproblem contains RASP's objective** by setting
its linear input to -M and its regularizer to μ||D||F²/2+γ<E,D>²/2. Its published
pre/post clipping algorithms are different instantiations. A time-varying random
regularizer does not inherit its fixed-regularizer convergence theorem.
BFO contains the **solver construction** with isotropic-plus-rank-one metric.
Markowitz contains the **mean–variance decision structure**. No novelty claim
attaches to those parts.

Exact γ=0 RASP equals spectral projection (`zero_penalty_eq_projection`) and
already has the same fixed-signal Lipschitz guarantee. Soft spectral maps also
regularize small singular values. We do not assert all peers are discontinuous,
unstable or missing variance adaptation. The actual 2×2 example distinguishes
coupled optimization from metric inversion then Euclidean projection; it does
not establish a universal optimization advantage over that different method.

SAGE uses polar SAM perturbations and isotropic noise scaled by multi-distribution
disagreement ([v2 §3](https://arxiv.org/html/2605.07914v2)); it does not instantiate
the RASP direction objective. It is a novelty comparator, not a same-oracle
training baseline because it needs distribution labels and extra perturbation
gradients. Adaptive batch-size noise-scale work likewise changes the sampling
policy, which the fixed-token protocol must treat separately.
