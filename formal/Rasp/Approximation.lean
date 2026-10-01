import Rasp.Matrix

/-! Certificates for feasible approximate steps. These theorems do not verify
an SVD implementation: the numerical primitive must discharge its error bounds.
All norms in the variational statements are ambient (Frobenius for Mat). -/

noncomputable section
namespace Rasp
open scoped RealInnerProductSpace
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

def ApproxVI (K : Set H) (μ γ : ℝ) (M E D : H) (ε : ℝ) : Prop :=
  D ∈ K ∧ ∀ V ∈ K, -ε ≤ ⟪residual μ γ M E D, V - D⟫

theorem approx_vi_gap {K : Set H} {μ γ ε : ℝ}
    (hμ : 0 ≤ μ) (hγ : 0 ≤ γ) {M E D V : H}
    (hD : ApproxVI K μ γ M E D ε) (hV : V ∈ K) :
    objective μ γ M E D - objective μ γ M E V ≤ ε := by
  have hi := hD.2 V hV
  have he := objective_expansion μ γ M E D V
  have hq : 0 ≤ μ / 2 * ‖V - D‖ ^ 2 + γ / 2 * ⟪E, V - D⟫ ^ 2 := by
    positivity
  linarith

theorem approx_vi_distance {K : Set H} {μ γ ε : ℝ}
    (hγ : 0 ≤ γ) {M E D V : H}
    (hD : ApproxVI K μ γ M E D ε) (hV : VI K μ γ M E V) :
    μ * ‖D - V‖ ^ 2 ≤ ε := by
  have hd := hD.2 V hV.1
  have hv := hV.2 D hD.1
  simp only [residual, inner_sub_left, inner_add_left, real_inner_smul_left,
    inner_sub_right] at hd hv
  simp only [← real_inner_self_eq_norm_sq, inner_sub_left, inner_sub_right]
  simp only [real_inner_comm V D] at hd hv ⊢
  have hn : 0 ≤ γ * (⟪E, D⟫ - ⟪E, V⟫) ^ 2 := by positivity
  nlinarith

/-- A computed residual with an ambient norm error τ yields a VI certificate
after multiplying by a bound on the feasible diameter. -/
theorem residual_roundoff_certificate {K : Set H} {μ γ ε τ R : ℝ}
    (hτ : 0 ≤ τ) {M E D computed : H} (hD : D ∈ K)
    (herr : ‖computed - residual μ γ M E D‖ ≤ τ)
    (hdiam : ∀ V ∈ K, ‖V - D‖ ≤ R)
    (hcheck : ∀ V ∈ K, -ε ≤ ⟪computed, V - D⟫) :
    ApproxVI K μ γ M E D (ε + τ * R) := by
  refine ⟨hD, fun V hV => ?_⟩
  have hc := real_inner_le_norm (computed - residual μ γ M E D) (V - D)
  have hb := mul_le_mul herr (hdiam V hV) (norm_nonneg _) hτ
  have hi := hcheck V hV
  rw [inner_sub_left] at hc
  linarith

variable (K : Set H) (hc : IsCompact K) (hne : K.Nonempty)

theorem zero_penalty_eq_projection (hK : Convex ℝ K) {μ : ℝ}
    (hμ : 0 < μ) {M E D : H} (hD : Solves K μ 0 M E D) :
    D = project K hc hne (μ⁻¹ • M) := by
  have hi := isotropicStep_solves K hc hne μ M
  have he : Solves K μ 0 M E (isotropicStep K hc hne μ M) := by
    simpa only [Solves, objective, zero_div, zero_mul, add_zero] using hi
  rw [← isotropicStep_eq_project K hc hne hK hμ M]
  exact solution_unique hK hμ (le_refl 0) hD he

theorem dualStep_lipschitz (hK : Convex ℝ K) {μ : ℝ} (hμ : 0 < μ)
    (M E : H) (a b : ℝ) :
    μ * ‖dualStep K hc hne μ M E a - dualStep K hc hne μ M E b‖ ≤
      |a - b| * ‖E‖ := by
  have h := lipschitz_signal hμ (le_refl 0)
    (dualStep_vi K hc hne hK hμ M E a)
    (dualStep_vi K hc hne hK hμ M E b)
  have he : M - a • E - (M - b • E) = (b - a) • E := by module
  rw [he, norm_smul, Real.norm_eq_abs, abs_sub_comm] at h
  exact h

/-- Both projection error and scalar residual error contribute. The point Dhat
need not be feasible; use radial_feasibility or a separate feasible certificate. -/
theorem approximate_feedback_error (hK : Convex ℝ K) {μ γ εp εf : ℝ}
    (hμ : 0 < μ) (hγ : 0 ≤ γ) {M E D Dhat : H}
    (hD : Solves K μ γ M E D) (z : ℝ)
    (hp : ‖Dhat - dualStep K hc hne μ M E z‖ ≤ εp)
    (hf : |z - γ * ⟪E, Dhat⟫| ≤ εf) :
    μ * ‖Dhat - D‖ ≤ μ * εp + (εf + γ * ‖E‖ * εp) * ‖E‖ := by
  let P := dualStep K hc hne μ M E z
  have he : feedback K hc hne μ γ M E z =
      (z - γ * ⟪E, Dhat⟫) + γ * ⟪E, Dhat - P⟫ := by
    dsimp [feedback, P]
    rw [inner_sub_right]
    ring
  have hi := abs_real_inner_le_norm E (Dhat - P)
  have hab := abs_add_le (z - γ * ⟪E, Dhat⟫) (γ * ⟪E, Dhat - P⟫)
  have hn := mul_le_mul_of_nonneg_left hp (norm_nonneg E)
  have hg := mul_le_mul_of_nonneg_left (hi.trans hn) hγ
  rw [abs_mul, abs_of_nonneg hγ] at hab
  have hb : |feedback K hc hne μ γ M E z| ≤ εf + γ * ‖E‖ * εp := by
    rw [he]
    dsimp [P] at hg hab
    nlinarith
  have hc' := feedback_error_bound K hc hne hK hμ hγ hD z
  have ht := norm_sub_le_norm_sub_add_norm_sub Dhat P D
  have ht' := mul_le_mul_of_nonneg_left ht hμ.le
  have hp' := mul_le_mul_of_nonneg_left hp hμ.le
  have hb' := mul_le_mul_of_nonneg_right hb (norm_nonneg E)
  dsimp [P] at ht'
  nlinarith

theorem feedback_initial_bracket (hK : Convex ℝ K) {μ γ : ℝ}
    (hμ : 0 < μ) (hγ : 0 ≤ γ) (M E : H) :
    feedback K hc hne μ γ M E (-|feedback K hc hne μ γ M E 0|) ≤ 0 ∧
      0 ≤ feedback K hc hne μ γ M E |feedback K hc hne μ γ M E 0| := by
  have hn := abs_nonneg (feedback K hc hne μ γ M E 0)
  have hl := feedback_strong_mono K hc hne hK hμ hγ M E (by linarith :
    -|feedback K hc hne μ γ M E 0| ≤ 0)
  have hu := feedback_strong_mono K hc hne hK hμ hγ M E hn
  have ha := le_abs_self (feedback K hc hne μ γ M E 0)
  have hb := neg_abs_le (feedback K hc hne μ γ M E 0)
  constructor <;> linarith

theorem feedback_root_interval (hK : Convex ℝ K) {μ γ : ℝ}
    (hμ : 0 < μ) (hγ : 0 ≤ γ) (M E : H) {a b z : ℝ}
    (ha : feedback K hc hne μ γ M E a ≤ 0)
    (hb : 0 ≤ feedback K hc hne μ γ M E b)
    (hz : feedback K hc hne μ γ M E z = 0) : a ≤ z ∧ z ≤ b := by
  constructor
  · by_contra h
    have hlt := lt_of_not_ge h
    have hm := feedback_strong_mono K hc hne hK hμ hγ M E hlt.le
    rw [hz] at hm
    linarith
  · by_contra h
    have hlt := lt_of_not_ge h
    have hm := feedback_strong_mono K hc hne hK hμ hγ M E hlt.le
    rw [hz] at hm
    linarith

theorem interval_midpoint_error {a b z : ℝ} (ha : a ≤ z) (hb : z ≤ b) :
    |(a + b) / 2 - z| ≤ (b - a) / 2 := by
  apply abs_le.mpr
  constructor <;> linarith

/-- This width certificate needs exact bracket signs. Uncertain signs from an
approximate projection must instead use approximate_feedback_error. -/
theorem bisection_step_error (hK : Convex ℝ K) {μ γ : ℝ}
    (hμ : 0 < μ) (hγ : 0 ≤ γ) (M E : H) {a b z : ℝ}
    (ha : feedback K hc hne μ γ M E a ≤ 0)
    (hb : 0 ≤ feedback K hc hne μ γ M E b)
    (hz : feedback K hc hne μ γ M E z = 0) :
    μ * ‖dualStep K hc hne μ M E ((a + b) / 2) -
      dualStep K hc hne μ M E z‖ ≤ (b - a) / 2 * ‖E‖ := by
  have hi := feedback_root_interval K hc hne hK hμ hγ M E ha hb hz
  have he := interval_midpoint_error hi.1 hi.2
  exact (dualStep_lipschitz K hc hne hK hμ M E _ _).trans
    (mul_le_mul_of_nonneg_right he (norm_nonneg E))

theorem bisection_width_step (w : ℝ) (n : ℕ) :
    w / (2 : ℝ) ^ (n + 1) = (w / (2 : ℝ) ^ n) / 2 := by
  rw [pow_succ, div_mul_eq_div_div]

/-- A certified upper bound on the actual matrix operator norm permits a
radial feasibility repair, including radius zero. No scalar matrix surrogate. -/
theorem radial_feasibility {m n : ℕ} {r b : ℝ} (hr : 0 ≤ r) (hb : 0 < b)
    (A : Mat m n) (hbound : ‖asOperator m n A‖ ≤ b) :
    (min 1 (r / b)) • A ∈ spectralBall m n r := by
  rw [mem_spectralBall, map_smul, norm_smul, Real.norm_eq_abs]
  have hc : 0 ≤ min 1 (r / b) := le_min (by norm_num) (div_nonneg hr hb.le)
  rw [abs_of_nonneg hc]
  have h1 := mul_le_mul_of_nonneg_left hbound hc
  have h2 := mul_le_mul_of_nonneg_right (min_le_right (1 : ℝ) (r / b)) hb.le
  have he : r / b * b = r := div_mul_cancel₀ r hb.ne'
  linarith

end Rasp
