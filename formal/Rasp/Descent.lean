import Rasp.Core

noncomputable section
namespace Rasp
open scoped RealInnerProductSpace
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

theorem zero_signal {K : Set H} (hK : Convex ℝ K) (hz : (0 : H) ∈ K)
    {μ γ : ℝ} (hμ : 0 < μ) (hγ : 0 ≤ γ) {E D : H}
    (hD : Solves K μ γ 0 E D) : D = 0 := by
  apply solution_unique hK hμ hγ hD
  apply vi_solves hμ.le hγ
  refine ⟨hz, fun V _ => ?_⟩
  simp [residual]

/-- One step only, assuming the usual quadratic upper model and a deterministic
bound on the signal error. It makes no global stochastic-convergence claim. -/
theorem descent_upper_model {K : Set H} (hzero : (0 : H) ∈ K)
    {μ γ η L δ : ℝ} (hη : 0 ≤ η) {M E D g W : H} {f : H → ℝ}
    (hD : VI K μ γ M E D) (herr : ‖g - M‖ ≤ δ)
    (hmodel : f (W - η • D) ≤ f W - η * ⟪g, D⟫ +
      L / 2 * η ^ 2 * ‖D‖ ^ 2) :
    f (W - η • D) ≤ f W - η *
      ((μ - L * η / 2) * ‖D‖ ^ 2 + γ * ⟪E, D⟫ ^ 2 - δ * ‖D‖) := by
  have ha := alignment hzero hD
  have hi := real_inner_le_norm (M - g) D
  have he : ‖M - g‖ ≤ δ := by rwa [norm_sub_rev]
  have hn := mul_le_mul_of_nonneg_right he (norm_nonneg D)
  simp only [inner_sub_left] at hi
  have hs : μ * ‖D‖ ^ 2 + γ * ⟪E, D⟫ ^ 2 - δ * ‖D‖ ≤ ⟪g, D⟫ := by
    linarith
  have ht := mul_le_mul_of_nonneg_left hs hη
  nlinarith [hmodel]

end Rasp
