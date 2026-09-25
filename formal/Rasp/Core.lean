import Mathlib

/-!
The variational core of Replica-Aware Spectral Proximal optimization (RASP).
All results in this file hold in a real inner product space; Matrix.lean
instantiates the feasible set with the actual matrix operator-norm ball.
-/

noncomputable section

namespace Rasp

open scoped RealInnerProductSpace

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

/-- The frozen, per-step mean--disagreement objective. -/
def objective (μ γ : ℝ) (M E D : H) : ℝ :=
  μ / 2 * ⟪D, D⟫ + γ / 2 * ⟪E, D⟫ ^ 2 - ⟪M, D⟫

/-- Gradient with respect to the proposed update, not the network parameters. -/
def residual (μ γ : ℝ) (M E D : H) : H :=
  μ • D + (γ * ⟪E, D⟫) • E - M

/-- The observed covariance operator acts on vectorized parameter space. -/
def noiseOperator (E : H) : H →L[ℝ] H := InnerProductSpace.rankOne ℝ E E

theorem noiseOperator_quadratic (E D : H) :
    ⟪noiseOperator E D, D⟫ = ⟪E, D⟫ ^ 2 := by
  simp [noiseOperator, real_inner_smul_left, pow_two]

theorem noiseOperator_rank_le (E : H) : (noiseOperator E).rank ≤ 1 := by
  by_cases h : E = 0
  · simp [noiseOperator, h]
  · exact (InnerProductSpace.rank_rankOne h h).le

/-- Exact minimization, including feasibility. No optimality conclusion is assumed. -/
def Solves (K : Set H) (μ γ : ℝ) (M E D : H) : Prop :=
  D ∈ K ∧ ∀ V ∈ K, objective μ γ M E D ≤ objective μ γ M E V

/-- The variational inequality that will be proved equivalent to minimization. -/
def VI (K : Set H) (μ γ : ℝ) (M E D : H) : Prop :=
  D ∈ K ∧ ∀ V ∈ K, 0 ≤ ⟪residual μ γ M E D, V - D⟫

theorem objective_expansion (μ γ : ℝ) (M E D V : H) :
    objective μ γ M E V - objective μ γ M E D =
      ⟪residual μ γ M E D, V - D⟫ +
        μ / 2 * ‖V - D‖ ^ 2 + γ / 2 * ⟪E, V - D⟫ ^ 2 := by
  simp only [objective, residual, inner_sub_left, inner_add_left, real_inner_smul_left,
    inner_sub_right, ← real_inner_self_eq_norm_sq]
  rw [real_inner_comm V D]
  ring

theorem objective_line (μ γ t : ℝ) (M E D U : H) :
    objective μ γ M E (D + t • U) - objective μ γ M E D =
      t * ⟪residual μ γ M E D, U⟫ +
        t ^ 2 * (μ / 2 * ‖U‖ ^ 2 + γ / 2 * ⟪E, U⟫ ^ 2) := by
  simp only [objective, residual, inner_sub_left, inner_add_left, inner_add_right,
    real_inner_smul_left, inner_smul_right, ← real_inner_self_eq_norm_sq]
  rw [real_inner_comm U D]
  ring

private theorem linear_term_nonneg {a b : ℝ} (hb : 0 ≤ b)
    (h : ∀ t : ℝ, 0 < t → t ≤ 1 → 0 ≤ t * a + t ^ 2 * b) : 0 ≤ a := by
  by_contra ha
  have ha : a < 0 := lt_of_not_ge ha
  let t := min 1 (-a / (2 * (b + 1)))
  have hden : 0 < 2 * (b + 1) := by positivity
  have ht : 0 < t := lt_min zero_lt_one (div_pos (neg_pos.mpr ha) hden)
  have ht1 : t ≤ 1 := min_le_left _ _
  have htb : t * (2 * (b + 1)) ≤ -a :=
    (le_div_iff₀ hden).mp (min_le_right _ _)
  have hp := h t ht ht1
  have hc : 0 ≤ a + t * b := by
    apply nonneg_of_mul_nonneg_right
    · nlinarith [hp]
    · exact ht
  nlinarith

theorem solves_vi {K : Set H} (hK : Convex ℝ K) {μ γ : ℝ}
    (hμ : 0 ≤ μ) (hγ : 0 ≤ γ) {M E D : H} (hD : Solves K μ γ M E D) :
    VI K μ γ M E D := by
  refine ⟨hD.1, fun V hV => ?_⟩
  apply linear_term_nonneg (b := μ / 2 * ‖V - D‖ ^ 2 + γ / 2 * ⟪E, V - D⟫ ^ 2)
  · positivity
  · intro t ht ht1
    have hm : D + t • (V - D) ∈ K := by
      have heq : D + t • (V - D) = (1 - t) • D + t • V := by module
      rw [heq]
      exact hK hD.1 hV (sub_nonneg.mpr ht1) ht.le (by ring)
    have h := hD.2 _ hm
    rw [← objective_line]
    linarith

theorem vi_solves {K : Set H} {μ γ : ℝ} (hμ : 0 ≤ μ) (hγ : 0 ≤ γ)
    {M E D : H} (hD : VI K μ γ M E D) : Solves K μ γ M E D := by
  refine ⟨hD.1, fun V hV => ?_⟩
  have hi := hD.2 V hV
  have he := objective_expansion μ γ M E D V
  have hq : 0 ≤ μ / 2 * ‖V - D‖ ^ 2 + γ / 2 * ⟪E, V - D⟫ ^ 2 := by positivity
  linarith

theorem solves_iff_vi {K : Set H} (hK : Convex ℝ K) {μ γ : ℝ}
    (hμ : 0 ≤ μ) (hγ : 0 ≤ γ) (M E D : H) :
    Solves K μ γ M E D ↔ VI K μ γ M E D :=
  ⟨solves_vi hK hμ hγ, vi_solves hμ hγ⟩

theorem exists_solution {K : Set H} (hK : IsCompact K) (hne : K.Nonempty)
    (μ γ : ℝ) (M E : H) : ∃ D, Solves K μ γ M E D := by
  have hc : Continuous (objective μ γ M E) := by unfold objective; fun_prop
  obtain ⟨D, hD, hmin⟩ := hK.exists_isMinOn hne hc.continuousOn
  exact ⟨D, hD, hmin⟩

theorem strong_gap {K : Set H} {μ γ : ℝ} (hγ : 0 ≤ γ)
    {M E D : H} (hD : VI K μ γ M E D) {V : H} (hV : V ∈ K) :
    μ / 2 * ‖V - D‖ ^ 2 ≤ objective μ γ M E V - objective μ γ M E D := by
  have he := objective_expansion μ γ M E D V
  have hi := hD.2 V hV
  have hq : 0 ≤ γ / 2 * ⟪E, V - D⟫ ^ 2 := by positivity
  linarith

theorem solution_unique {K : Set H} (hK : Convex ℝ K) {μ γ : ℝ}
    (hμ : 0 < μ) (hγ : 0 ≤ γ) {M E D V : H}
    (hD : Solves K μ γ M E D) (hV : Solves K μ γ M E V) : D = V := by
  have hg := strong_gap hγ (solves_vi hK hμ.le hγ hD) hV.1
  have hm := hV.2 D hD.1
  have hz : ‖V - D‖ ^ 2 = 0 := by nlinarith [sq_nonneg ‖V - D‖]
  have : V - D = 0 := norm_eq_zero.mp (sq_eq_zero_iff.mp hz)
  exact (sub_eq_zero.mp this).symm

theorem firm_stability {K : Set H} {μ γ : ℝ} {M N E D V : H}
    (hD : VI K μ γ M E D) (hV : VI K μ γ N E V) :
    μ * ‖D - V‖ ^ 2 + γ * ⟪E, D - V⟫ ^ 2 ≤ ⟪M - N, D - V⟫ := by
  have hd := hD.2 V hV.1
  have hv := hV.2 D hD.1
  simp only [residual, inner_sub_left, inner_add_left, real_inner_smul_left,
    inner_sub_right] at hd hv
  simp only [inner_sub_left, inner_sub_right, ← real_inner_self_eq_norm_sq]
  simp only [real_inner_comm V D] at hd hv ⊢
  nlinarith

theorem lipschitz_signal {K : Set H} {μ γ : ℝ} (_hμ : 0 < μ) (hγ : 0 ≤ γ)
    {M N E D V : H} (hD : VI K μ γ M E D) (hV : VI K μ γ N E V) :
    μ * ‖D - V‖ ≤ ‖M - N‖ := by
  have hf := firm_stability hD hV
  have hc := real_inner_le_norm (M - N) (D - V)
  have hq : 0 ≤ γ * ⟪E, D - V⟫ ^ 2 := by positivity
  by_cases hz : ‖D - V‖ = 0
  · simp [hz]
  · have hp : 0 < ‖D - V‖ := lt_of_le_of_ne (norm_nonneg _) (Ne.symm hz)
    nlinarith

theorem alignment {K : Set H} (hzero : (0 : H) ∈ K) {μ γ : ℝ}
    {M E D : H} (hD : VI K μ γ M E D) :
    μ * ‖D‖ ^ 2 + γ * ⟪E, D⟫ ^ 2 ≤ ⟪M, D⟫ := by
  have h := hD.2 0 hzero
  simp only [residual, zero_sub, inner_neg_right, inner_sub_left, inner_add_left,
    real_inner_smul_left, real_inner_self_eq_norm_sq] at h
  nlinarith

theorem disagreement_antitone {K : Set H} {μ γ₁ γ₂ : ℝ}
    (hγ : γ₁ < γ₂) {M E D V : H}
    (hD : Solves K μ γ₁ M E D) (hV : Solves K μ γ₂ M E V) :
    ⟪E, V⟫ ^ 2 ≤ ⟪E, D⟫ ^ 2 := by
  have hd := hD.2 V hV.1
  have hv := hV.2 D hD.1
  unfold objective at hd hv
  nlinarith

end Rasp
