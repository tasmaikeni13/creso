import Rasp

/-! CRESO's exact finite spectral decision problem. The feasible operator is
the actual rectangular matrix operator; no scalar replacement is used. -/
noncomputable section
namespace Creso
open scoped RealInnerProductSpace BigOperators Matrix.Norms.L2Operator

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

def mix (t : ℝ) (A B : H) : H := (1 - t) • A + t • B

def progress (μ : ℝ) (g D : H) : ℝ := ⟪g, D⟫ - μ / 2 * ‖D‖ ^ 2

def certificate (μ : ℝ) (v A B : H) (bA bB t : ℝ) : ℝ :=
  progress μ v (mix t A B) - ((1 - t) * bA + t * bB)

def gain (a q t : ℝ) : ℝ := a * t - q / 2 * t ^ 2

def bestFraction (a q : ℝ) : ℝ :=
  if q = 0 then (if a ≤ 0 then 0 else 1) else max 0 (min 1 (a / q))

theorem mix_zero (A B : H) : mix 0 A B = A := by simp [mix]
theorem mix_one (A B : H) : mix 1 A B = B := by simp [mix]

theorem mix_feasible {m n : ℕ} {r t : ℝ} {A B : Rasp.Mat m n}
    (hA : A ∈ Rasp.spectralBall m n r) (hB : B ∈ Rasp.spectralBall m n r)
    (ht : t ∈ Set.Icc (0 : ℝ) 1) : mix t A B ∈ Rasp.spectralBall m n r :=
  (Rasp.spectralBall_convex m n r) hA hB (sub_nonneg.mpr ht.2) ht.1 (by ring)

theorem progress_mix (μ t : ℝ) (g A B : H) :
    progress μ g (mix t A B) = (1 - t) * progress μ g A +
      t * progress μ g B + μ / 2 * t * (1 - t) * ‖A - B‖ ^ 2 := by
  simp only [progress, mix, inner_add_right, inner_smul_right,
    ← real_inner_self_eq_norm_sq, inner_add_left, real_inner_smul_left,
    inner_sub_left, inner_sub_right]
  rw [real_inner_comm B A]
  ring

theorem certificate_quadratic (μ bA bB t : ℝ) (v A B : H) :
    certificate μ v A B bA bB t = progress μ v A - bA +
      gain (⟪v - μ • A, B - A⟫ - (bB - bA)) (μ * ‖B - A‖ ^ 2) t := by
  rw [certificate, progress_mix]
  simp only [progress, gain, inner_sub_left, inner_sub_right, real_inner_smul_left,
    ← real_inner_self_eq_norm_sq]
  rw [real_inner_comm B A]
  ring

theorem bestFraction_mem {a q : ℝ} (_hq : 0 ≤ q) :
    bestFraction a q ∈ Set.Icc (0 : ℝ) 1 := by
  by_cases hz : q = 0
  · simp [bestFraction, hz]; split_ifs <;> norm_num
  · simp only [bestFraction, hz, ↓reduceIte, Set.mem_Icc]
    exact ⟨le_max_left _ _, max_le (by norm_num) (min_le_left _ _)⟩

theorem bestFraction_maximizes {a q : ℝ} (hq : 0 ≤ q)
    {t : ℝ} (ht : t ∈ Set.Icc (0 : ℝ) 1) :
    gain a q t ≤ gain a q (bestFraction a q) := by
  by_cases hz : q = 0
  · by_cases ha : a ≤ 0
    · simp only [bestFraction, hz, ha, ↓reduceIte, gain]
      nlinarith [mul_nonpos_of_nonpos_of_nonneg ha ht.1]
    · simp only [bestFraction, hz, ha, ↓reduceIte, gain]
      have h := mul_le_mul_of_nonneg_left ht.2 (le_of_lt (lt_of_not_ge ha))
      nlinarith
  · have hqp : 0 < q := lt_of_le_of_ne hq (Ne.symm hz)
    by_cases ha : a ≤ 0
    · have hd : a / q ≤ 0 := div_nonpos_of_nonpos_of_nonneg ha hq
      have hm : min 1 (a / q) ≤ 0 := (min_le_right _ _).trans hd
      simp only [bestFraction, hz, ↓reduceIte, max_eq_left hm, gain]
      nlinarith [mul_nonpos_of_nonpos_of_nonneg ha ht.1]
    · by_cases hb : q ≤ a
      · have hd : 1 ≤ a / q := (le_div_iff₀ hqp).mpr (by simpa using hb)
        simp only [bestFraction, hz, ↓reduceIte, min_eq_left hd, max_eq_right zero_le_one,
          gain]
        have hp : 0 ≤ (1 - t) * (a - q / 2 * (1 + t)) :=
          mul_nonneg (sub_nonneg.mpr ht.2)
            (by nlinarith [mul_nonneg hq (sub_nonneg.mpr ht.2)])
        nlinarith
      · have hapos : 0 < a := lt_of_not_ge ha
        have hdiv : 0 ≤ a / q := (div_pos hapos hqp).le
        have hdiv1 : a / q ≤ 1 := (div_le_one hqp).mpr (le_of_lt (lt_of_not_ge hb))
        simp only [bestFraction, hz, ↓reduceIte, min_eq_right hdiv1, max_eq_right hdiv,
          gain]
        have he : (a * t - q / 2 * t ^ 2) -
            (a * (a / q) - q / 2 * (a / q) ^ 2) =
            -(q / 2) * (t - a / q) ^ 2 := by field_simp; ring
        have hn : -(q / 2) * (t - a / q) ^ 2 ≤ 0 :=
          mul_nonpos_of_nonpos_of_nonneg (by linarith) (sq_nonneg _)
        linarith

theorem segment_optimal {μ bA bB : ℝ} (hμ : 0 ≤ μ) (v A B : H)
    {t : ℝ} (ht : t ∈ Set.Icc (0 : ℝ) 1) :
    certificate μ v A B bA bB t ≤ certificate μ v A B bA bB
      (bestFraction (⟪v - μ • A, B - A⟫ - (bB - bA)) (μ * ‖B - A‖ ^ 2)) := by
  rw [certificate_quadratic, certificate_quadratic]
  exact add_le_add_right
    (bestFraction_maximizes (q := μ * ‖B - A‖ ^ 2) (by positivity) ht) _

theorem uniform_certificate {μ bA bB t : ℝ} {g v A B : H}
    (ht : t ∈ Set.Icc (0 : ℝ) 1)
    (hA : |⟪v - g, A⟫| ≤ bA) (hB : |⟪v - g, B⟫| ≤ bB) :
    certificate μ v A B bA bB t ≤ progress μ g (mix t A B) := by
  have ha := (abs_le.mp hA).2
  have hb := (abs_le.mp hB).2
  have hp := mul_le_mul_of_nonneg_left ha (sub_nonneg.mpr ht.2)
  have hq := mul_le_mul_of_nonneg_left hb ht.1
  simp only [certificate, progress, mix, inner_add_right, inner_smul_right,
    inner_sub_left] at *
  linarith

theorem vertex_certificate_error {μ b : ℝ} {g v A : H}
    (h : |⟪v - g, A⟫| ≤ b) :
    progress μ g A - 2 * b ≤ progress μ v A - b := by
  have hl := (abs_le.mp h).1
  simp only [progress, inner_sub_left] at *
  linarith

theorem selected_oracle_bound {μ bA bB bj t ε : ℝ} {g v A B V : H}
    (ht : t ∈ Set.Icc (0 : ℝ) 1)
    (hA : |⟪v - g, A⟫| ≤ bA) (hB : |⟪v - g, B⟫| ≤ bB)
    (hV : |⟪v - g, V⟫| ≤ bj)
    (hsel : progress μ v V - bj ≤ certificate μ v A B bA bB t + ε) :
    progress μ g V - 2 * bj - ε ≤ progress μ g (mix t A B) := by
  have hc := uniform_certificate (μ := μ) ht hA hB
  have hv := vertex_certificate_error (μ := μ) hV
  linarith

theorem exists_finite_best {ι : Type*} [Fintype ι] [Nonempty ι]
    (value : ι → ℝ) : ∃ i, ∀ j, value j ≤ value i := by
  classical
  obtain ⟨i, _, hi⟩ := Finset.exists_max_image Finset.univ value Finset.univ_nonempty
  exact ⟨i, fun j => hi j (Finset.mem_univ j)⟩

theorem exists_matrix_decision {m n k : ℕ} [NeZero k] {r μ : ℝ}
    (hμ : 0 ≤ μ) (D : Fin k → Rasp.Mat m n) (v : Rasp.Mat m n) (b : Fin k → ℝ)
    (hf : ∀ i, D i ∈ Rasp.spectralBall m n r) :
    ∃ i j t, t ∈ Set.Icc (0 : ℝ) 1 ∧ mix t (D i) (D j) ∈ Rasp.spectralBall m n r ∧
      ∀ p q s, s ∈ Set.Icc (0 : ℝ) 1 →
        certificate μ v (D p) (D q) (b p) (b q) s ≤
          certificate μ v (D i) (D j) (b i) (b j) t := by
  let fraction : Fin k × Fin k → ℝ := fun p =>
    bestFraction (⟪v - μ • D p.1, D p.2 - D p.1⟫ - (b p.2 - b p.1))
      (μ * ‖D p.2 - D p.1‖ ^ 2)
  let value : Fin k × Fin k → ℝ := fun p =>
    certificate μ v (D p.1) (D p.2) (b p.1) (b p.2) (fraction p)
  obtain ⟨p, hp⟩ := exists_finite_best value
  have ht : fraction p ∈ Set.Icc (0 : ℝ) 1 := bestFraction_mem (by positivity)
  refine ⟨p.1, p.2, fraction p, ht, mix_feasible (hf _) (hf _) ht, ?_⟩
  intro i j s hs
  exact (segment_optimal hμ v (D i) (D j) hs).trans (hp (i, j))

theorem deflation_recovers_signal (P : H →L[ℝ] H) (g ξ : H)
    (hg : P g = 0) (hξ : P ξ = ξ) : (g + ξ) - P (g + ξ) = g := by
  rw [map_add, hg, hξ]
  module

theorem certified_descent {μ η fnext fnow : ℝ} {g v A B : H} {bA bB t : ℝ}
    (hη : 0 ≤ η) (ht : t ∈ Set.Icc (0 : ℝ) 1)
    (hA : |⟪v - g, A⟫| ≤ bA) (hB : |⟪v - g, B⟫| ≤ bB)
    (hmodel : fnext ≤ fnow - η * progress μ g (mix t A B)) :
    fnext ≤ fnow - η * certificate μ v A B bA bB t := by
  have hc := mul_le_mul_of_nonneg_left (uniform_certificate (μ := μ) ht hA hB) hη
  linarith

theorem active_matrix_muon_gap :
    progress 1 (Rasp.diag₂ 1 0) (Rasp.diag₂ (1 / 2) 0) -
      progress 1 (Rasp.diag₂ 1 0) (Rasp.diag₂ (1 / 2) (1 / 2)) = 1 / 8 := by
  simp only [progress, ← real_inner_self_eq_norm_sq, Rasp.inner_diag₂]
  norm_num [Rasp.diag₂, Rasp.matrixEquiv, Matrix.diagonal]

theorem active_matrix_candidates_feasible :
    Rasp.diag₂ (1 / 2) 0 ∈ Rasp.spectralBall 2 2 (1 / 2) ∧
      Rasp.diag₂ (1 / 2) (1 / 2) ∈ Rasp.spectralBall 2 2 (1 / 2) := by
  constructor <;> rw [Rasp.mem_spectralBall]
  all_goals
    change ‖(Matrix.diagonal _ : Matrix (Fin 2) (Fin 2) ℝ)‖ ≤ (1 / 2 : ℝ)
    rw [Matrix.l2_opNorm_diagonal]
    apply (pi_norm_le_iff_of_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 2)).mpr
    intro i
    fin_cases i <;> norm_num

end Creso
