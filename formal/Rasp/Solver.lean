import Rasp.Core

/-! The scalar feedback solver. The general low-rank proximal calculus is
due to Becker, Fadili and Ochs (2019); it is not claimed as a new theorem. -/

noncomputable section
namespace Rasp
open scoped RealInnerProductSpace
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]
variable (K : Set H) (hc : IsCompact K) (hne : K.Nonempty)

/-- The unique isotropic constrained quadratic minimizer when μ > 0. -/
def isotropicStep (μ : ℝ) (M : H) : H :=
  Classical.choose (exists_solution hc hne μ 0 M 0)

theorem isotropicStep_solves (μ : ℝ) (M : H) :
    Solves K μ 0 M 0 (isotropicStep K hc hne μ M) :=
  Classical.choose_spec (exists_solution hc hne μ 0 M 0)

theorem isotropicStep_vi (hK : Convex ℝ K) {μ : ℝ} (hμ : 0 < μ) (M E : H) :
    VI K μ 0 M E (isotropicStep K hc hne μ M) := by
  have h := solves_vi hK hμ.le (le_refl 0) (isotropicStep_solves K hc hne μ M)
  simpa only [VI, residual, zero_mul, zero_smul, add_zero] using h

/-- The Frobenius/Euclidean projection, defined by its minimization problem. -/
def project (X : H) : H := isotropicStep K hc hne 1 X

theorem project_minimizes_distance (X V : H) (hV : V ∈ K) :
    ‖project K hc hne X - X‖ ^ 2 ≤ ‖V - X‖ ^ 2 := by
  have h := (isotropicStep_solves K hc hne 1 X).2 V hV
  simp only [objective, zero_div, zero_mul, add_zero] at h
  simp only [← real_inner_self_eq_norm_sq, inner_sub_left, inner_sub_right]
  simp only [project] at *
  rw [real_inner_comm X (isotropicStep K hc hne 1 X), real_inner_comm X V]
  linarith

theorem isotropicStep_eq_project (hK : Convex ℝ K) {μ : ℝ} (hμ : 0 < μ) (M : H) :
    isotropicStep K hc hne μ M = project K hc hne (μ⁻¹ • M) := by
  let D := project K hc hne (μ⁻¹ • M)
  have hd := isotropicStep_vi K hc hne hK (by norm_num : (0 : ℝ) < 1) (μ⁻¹ • M) (0 : H)
  have hv : VI K μ 0 M 0 D := by
    refine ⟨hd.1, fun V hV => ?_⟩
    have hi := mul_nonneg hμ.le (hd.2 V hV)
    have hm : μ * μ⁻¹ = 1 := mul_inv_cancel₀ hμ.ne'
    simp only [residual, zero_mul, zero_smul, add_zero, one_smul, inner_sub_left,
      real_inner_smul_left] at hi ⊢
    dsimp [D, project] at *
    rw [mul_sub, ← mul_assoc, hm, one_mul] at hi
    exact hi
  exact solution_unique hK hμ (le_refl 0)
    (isotropicStep_solves K hc hne μ M) (vi_solves hμ.le (le_refl 0) hv)

def dualStep (μ : ℝ) (M E : H) (z : ℝ) : H :=
  isotropicStep K hc hne μ (M - z • E)

def feedback (μ γ : ℝ) (M E : H) (z : ℝ) : ℝ :=
  z - γ * ⟪E, dualStep K hc hne μ M E z⟫

theorem dualStep_vi (hK : Convex ℝ K) {μ : ℝ} (hμ : 0 < μ) (M E : H) (z : ℝ) :
    VI K μ 0 (M - z • E) E (dualStep K hc hne μ M E z) :=
  isotropicStep_vi K hc hne hK hμ _ _

theorem root_solves (hK : Convex ℝ K) {μ γ : ℝ} (hμ : 0 < μ) (hγ : 0 ≤ γ)
    (M E : H) {z : ℝ} (hz : feedback K hc hne μ γ M E z = 0) :
    Solves K μ γ M E (dualStep K hc hne μ M E z) := by
  have hv := dualStep_vi K hc hne hK hμ M E z
  have heq : z = γ * ⟪E, dualStep K hc hne μ M E z⟫ := sub_eq_zero.mp hz
  apply vi_solves hμ.le hγ
  refine ⟨hv.1, fun V hV => ?_⟩
  have hi := hv.2 V hV
  have hr : residual μ 0 (M - z • E) E (dualStep K hc hne μ M E z) =
      residual μ γ M E (dualStep K hc hne μ M E z) := by
    unfold residual
    simp only [zero_mul, zero_smul, add_zero]
    have hs : z • E = (γ * ⟪E, dualStep K hc hne μ M E z⟫) • E :=
      congrArg (fun q : ℝ => q • E) heq
    rw [hs]
    abel
  rwa [hr] at hi

theorem solution_is_dualStep (hK : Convex ℝ K) {μ γ : ℝ} (hμ : 0 < μ) (hγ : 0 ≤ γ)
    {M E D : H} (hD : Solves K μ γ M E D) :
    D = dualStep K hc hne μ M E (γ * ⟪E, D⟫) := by
  have hd := solves_vi hK hμ.le hγ hD
  have hv : VI K μ 0 (M - (γ * ⟪E, D⟫) • E) 0 D := by
    refine ⟨hd.1, fun V hV => ?_⟩
    have hi := hd.2 V hV
    have hr : residual μ 0 (M - (γ * ⟪E, D⟫) • E) 0 D = residual μ γ M E D := by
      simp only [residual, zero_mul, zero_smul, add_zero]
      abel
    rwa [hr]
  exact solution_unique hK hμ (le_refl 0) (vi_solves hμ.le (le_refl 0) hv)
    (isotropicStep_solves K hc hne μ _)

theorem exists_root (hK : Convex ℝ K) {μ γ : ℝ} (hμ : 0 < μ) (hγ : 0 ≤ γ) (M E : H) :
    ∃ z, feedback K hc hne μ γ M E z = 0 := by
  obtain ⟨D, hd⟩ := exists_solution hc hne μ γ M E
  refine ⟨γ * ⟪E, D⟫, ?_⟩
  unfold feedback
  rw [← solution_is_dualStep K hc hne hK hμ hγ hd]
  ring

theorem feedback_strong_mono (hK : Convex ℝ K) {μ γ : ℝ} (hμ : 0 < μ) (hγ : 0 ≤ γ)
    (M E : H) {a b : ℝ} (hab : a ≤ b) :
    b - a ≤ feedback K hc hne μ γ M E b - feedback K hc hne μ γ M E a := by
  by_cases heq : a = b
  · simp [heq]
  have hp : 0 < b - a := sub_pos.mpr (lt_of_le_of_ne hab heq)
  have h := firm_stability (dualStep_vi K hc hne hK hμ M E a)
    (dualStep_vi K hc hne hK hμ M E b)
  simp only [zero_mul, add_zero, inner_sub_left, inner_sub_right, real_inner_smul_left] at h
  have hn : 0 ≤ μ * ‖dualStep K hc hne μ M E a - dualStep K hc hne μ M E b‖ ^ 2 := by
    positivity
  have hd : 0 ≤ ⟪E, dualStep K hc hne μ M E a⟫ - ⟪E, dualStep K hc hne μ M E b⟫ := by
    apply nonneg_of_mul_nonneg_right (a := b - a)
    · nlinarith [h]
    · exact hp
  unfold feedback
  nlinarith [mul_nonneg hγ hd]

theorem root_unique (hK : Convex ℝ K) {μ γ : ℝ} (hμ : 0 < μ) (hγ : 0 ≤ γ)
    (M E : H) {a b : ℝ}
    (ha : feedback K hc hne μ γ M E a = 0)
    (hb : feedback K hc hne μ γ M E b = 0) : a = b := by
  rcases le_total a b with hab | hba
  · have h := feedback_strong_mono K hc hne hK hμ hγ M E hab
    rw [ha, hb] at h
    linarith
  · have h := feedback_strong_mono K hc hne hK hμ hγ M E hba
    rw [ha, hb] at h
    linarith

/-- A stopping certificate for an exact projection with an inexact scalar root. -/
theorem feedback_error_bound (hK : Convex ℝ K) {μ γ : ℝ} (hμ : 0 < μ) (hγ : 0 ≤ γ)
    {M E D : H} (hD : Solves K μ γ M E D) (z : ℝ) :
    μ * ‖dualStep K hc hne μ M E z - D‖ ≤ |feedback K hc hne μ γ M E z| * ‖E‖ := by
  let d := dualStep K hc hne μ M E z
  let f := feedback K hc hne μ γ M E z
  have hv := dualStep_vi K hc hne hK hμ M E z
  have hd : VI K μ γ (M - f • E) E d := by
    refine ⟨hv.1, fun V hV => ?_⟩
    have hi := hv.2 V hV
    have hr : residual μ γ (M - f • E) E d = residual μ 0 (M - z • E) E d := by
      dsimp [residual, f, feedback]
      module
    rwa [hr]
  have h := lipschitz_signal hμ hγ hd (solves_vi hK hμ.le hγ hD)
  have heq : M - f • E - M = -(f • E) := by abel
  rw [heq, norm_neg, norm_smul, Real.norm_eq_abs] at h
  exact h

end Rasp
