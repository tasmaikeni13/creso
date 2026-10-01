import Creso.Core

/-! Explicit finite probability masses. Concentration premises are moments,
not assumed success events. Directions must be frozen before these draws. -/
noncomputable section
namespace Creso
open scoped BigOperators RealInnerProductSpace
attribute [local instance] Classical.propDecidable

theorem finite_chebyshev {Ω : Type*} [Fintype Ω] (p x : Ω → ℝ)
    (hp : ∀ ω, 0 ≤ p ω) {b : ℝ} (hb : 0 < b) :
    (∑ ω, if b ≤ |x ω| then p ω else 0) ≤ (∑ ω, p ω * x ω ^ 2) / b ^ 2 := by
  classical
  have hpoint (ω : Ω) : (if b ≤ |x ω| then p ω else 0) * b ^ 2 ≤ p ω * x ω ^ 2 := by
    by_cases h : b ≤ |x ω|
    · simp only [h, ↓reduceIte]
      have hs : b ^ 2 ≤ x ω ^ 2 := by nlinarith [sq_abs (x ω), abs_nonneg (x ω)]
      exact mul_le_mul_of_nonneg_left hs (hp ω)
    · simp only [h, ↓reduceIte, zero_mul]
      exact mul_nonneg (hp ω) (sq_nonneg _)
  have hs := Finset.sum_le_sum (s := Finset.univ) (fun ω _ => hpoint ω)
  rw [← Finset.sum_mul] at hs
  exact (le_div_iff₀ (by positivity : (0 : ℝ) < b ^ 2)).mpr hs

theorem finite_union_bound {Ω ι : Type*} [Fintype Ω] [Fintype ι]
    (p : Ω → ℝ) (hp : ∀ ω, 0 ≤ p ω) (bad : ι → Ω → Prop) :
    (∑ ω, if ∃ i, bad i ω then p ω else 0) ≤
      ∑ i, ∑ ω, if bad i ω then p ω else 0 := by
  classical
  calc
    _ ≤ ∑ ω, ∑ i, if bad i ω then p ω else 0 := by
      apply Finset.sum_le_sum
      intro ω _
      by_cases h : ∃ i, bad i ω
      · rw [ite_eq_left h]
        obtain ⟨i, hi⟩ := h
        have hle := Finset.single_le_sum
          (fun j (_ : j ∈ Finset.univ) => show 0 ≤ (if bad j ω then p ω else 0) by
            split_ifs; exact hp ω; exact le_rfl)
          (Finset.mem_univ i)
        simpa only [ite_eq_left hi] using hle
      · simp only [ite_eq_right h]
        exact Finset.sum_nonneg (fun i _ => by split_ifs; exact hp ω; exact le_rfl)
    _ = _ := Finset.sum_comm

theorem simultaneous_moment_bound {Ω ι : Type*} [Fintype Ω] [Fintype ι]
    (p : Ω → ℝ) (hp : ∀ ω, 0 ≤ p ω) (x : ι → Ω → ℝ)
    (b v : ι → ℝ) (hb : ∀ i, 0 < b i)
    (hv : ∀ i, (∑ ω, p ω * x i ω ^ 2) ≤ v i) :
    (∑ ω, if ∃ i, b i ≤ |x i ω| then p ω else 0) ≤ ∑ i, v i / b i ^ 2 := by
  apply (finite_union_bound p hp (fun i ω => b i ≤ |x i ω|)).trans
  apply Finset.sum_le_sum
  intro i _
  exact (finite_chebyshev p (x i) hp (hb i)).trans
    (div_le_div_of_nonneg_right (hv i) (sq_nonneg _))

theorem relative_trace_upper {q estimate a : ℝ} (_hq : 0 ≤ q)
    (_ha : 0 ≤ a) (ha1 : a < 1) (h : |estimate - q| ≤ a * q) :
    q ≤ estimate / (1 - a) := by
  apply (le_div_iff₀ (by linarith : 0 < 1 - a)).mpr
  have hl := (abs_le.mp h).1
  nlinarith

theorem trace_upper_failure_mass {Ω : Type*} [Fintype Ω] (p e : Ω → ℝ)
    (hp : ∀ ω, 0 ≤ p ω) {q a κ n : ℝ} (hq : 0 < q) (ha : 0 < a)
    (ha1 : a < 1) (hn : 0 < n)
    (hm : (∑ ω, p ω * (e ω - q) ^ 2) ≤ κ * q ^ 2 / n) :
    (∑ ω, if e ω / (1 - a) < q then p ω else 0) ≤ κ / (n * a ^ 2) := by
  classical
  have hb : 0 < a * q := mul_pos ha hq
  have ht := finite_chebyshev p (fun ω => e ω - q) hp hb
  have hsubset : (∑ ω, if e ω / (1 - a) < q then p ω else 0) ≤
      ∑ ω, if a * q ≤ |e ω - q| then p ω else 0 := by
    apply Finset.sum_le_sum
    intro ω _
    by_cases h : e ω / (1 - a) < q
    · have he : e ω < q * (1 - a) := (div_lt_iff₀ (by linarith : 0 < 1 - a)).mp h
      have hh : a * q ≤ |e ω - q| := by
        have hl := neg_abs_le (e ω - q)
        nlinarith
      simp only [ite_eq_left h, ite_eq_left hh]
      exact le_rfl
    · simp only [ite_eq_right h]
      split_ifs; exact hp ω; exact le_rfl
  apply hsubset.trans (ht.trans ?_)
  calc
    _ ≤ (κ * q ^ 2 / n) / (a * q) ^ 2 :=
      div_le_div_of_nonneg_right hm (sq_nonneg _)
    _ = κ / (n * a ^ 2) := by field_simp

theorem zero_trace_exact {Ω : Type*} [Fintype Ω] (p e : Ω → ℝ)
    (hp : ∀ ω, 0 < p ω) (he : ∀ ω, 0 ≤ e ω)
    (hz : ∑ ω, p ω * e ω = 0) : ∀ ω, e ω = 0 := by
  intro ω
  have hs := Finset.single_le_sum
    (fun j (_ : j ∈ Finset.univ) => mul_nonneg (hp j).le (he j)) (Finset.mem_univ ω)
  rw [hz] at hs
  have : p ω * e ω = 0 := le_antisymm hs (mul_nonneg (hp ω).le (he ω))
  exact (mul_eq_zero.mp this).resolve_left (ne_of_gt (hp ω))

theorem squared_sum_envelope (x y : ℝ) : (x + y) ^ 2 ≤ 2 * (x ^ 2 + y ^ 2) := by
  nlinarith [sq_nonneg (x - y)]

theorem finite_split_envelope {Ω : Type*} [Fintype Ω] (p x y : Ω → ℝ)
    (hp : ∀ ω, 0 ≤ p ω) :
    (∑ ω, p ω * (x ω + y ω) ^ 2) ≤
      2 * ((∑ ω, p ω * x ω ^ 2) + ∑ ω, p ω * y ω ^ 2) := by
  calc
    _ ≤ ∑ ω, p ω * (2 * (x ω ^ 2 + y ω ^ 2)) :=
      Finset.sum_le_sum (fun ω _ => mul_le_mul_of_nonneg_left
        (squared_sum_envelope (x ω) (y ω)) (hp ω))
    _ = _ := by
      simp_rw [mul_add, Finset.sum_add_distrib]
      ring_nf
      simp only [← Finset.sum_mul]

theorem finite_inner_trace_bound {Ω H : Type*} [Fintype Ω]
    [NormedAddCommGroup H] [InnerProductSpace ℝ H] (p : Ω → ℝ)
    (hp : ∀ ω, 0 ≤ p ω) (e : Ω → H) (d : H) :
    (∑ ω, p ω * ⟪e ω, d⟫ ^ 2) ≤ (∑ ω, p ω * ‖e ω‖ ^ 2) * ‖d‖ ^ 2 := by
  rw [Finset.sum_mul]
  apply Finset.sum_le_sum
  intro ω _
  rw [mul_assoc]
  apply mul_le_mul_of_nonneg_left _ (hp ω)
  have h := abs_real_inner_le_norm (e ω) d
  have hh := mul_self_le_mul_self (abs_nonneg (⟪e ω, d⟫)) h
  simpa only [← sq, sq_abs, mul_pow] using hh

theorem finite_directional_envelope {Ω H : Type*} [Fintype Ω]
    [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    (p : Ω → ℝ) (hp : ∀ ω, 0 ≤ p ω) (e eP eR : Ω → H) (d dP dR : H)
    (hsplit : ∀ ω, ⟪e ω, d⟫ = ⟪eP ω, dP⟫ + ⟪eR ω, dR⟫) :
    (∑ ω, p ω * ⟪e ω, d⟫ ^ 2) ≤
      2 * ((∑ ω, p ω * ‖eP ω‖ ^ 2) * ‖dP‖ ^ 2 +
        (∑ ω, p ω * ‖eR ω‖ ^ 2) * ‖dR‖ ^ 2) := by
  simp_rw [hsplit]
  exact (finite_split_envelope p _ _ hp).trans
    (mul_le_mul_of_nonneg_left
      (add_le_add (finite_inner_trace_bound p hp eP dP)
        (finite_inner_trace_bound p hp eR dR)) (by norm_num))

theorem two_stage_failure_bound {Ω ι : Type*} [Fintype Ω] [Fintype ι]
    (p : Ω → ℝ) (hp : ∀ ω, 0 ≤ p ω) (calBad : Ω → Prop)
    (meanBad : ι → Ω → Prop) (selectedBad : Ω → Prop) {δc δv : ℝ}
    (hc : (∑ ω, if calBad ω then p ω else 0) ≤ δc)
    (hv : (∑ ω, if ∃ i, meanBad i ω then p ω else 0) ≤ δv)
    (hsubset : ∀ ω, selectedBad ω → calBad ω ∨ ∃ i, meanBad i ω) :
    (∑ ω, if selectedBad ω then p ω else 0) ≤ δc + δv := by
  classical
  have hs : (∑ ω, if selectedBad ω then p ω else 0) ≤
      ∑ ω, if calBad ω ∨ ∃ i, meanBad i ω then p ω else 0 := by
    apply Finset.sum_le_sum
    intro ω _
    by_cases h : selectedBad ω
    · simp only [ite_eq_left h, ite_eq_left (hsubset ω h)]
      exact le_rfl
    · simp only [ite_eq_right h]
      split_ifs; exact hp ω; exact le_rfl
  have hu := finite_union_bound p hp
    (fun i : Bool => if i then (fun ω => ∃ j, meanBad j ω) else calBad)
  have he : (∑ ω, if calBad ω ∨ ∃ i, meanBad i ω then p ω else 0) ≤
      (∑ ω, if calBad ω then p ω else 0) +
        ∑ ω, if ∃ i, meanBad i ω then p ω else 0 := by
    simpa only [Bool.exists_bool, Bool.false_eq_true, ↓reduceIte,
      Bool.true_eq, Fintype.sum_bool, or_comm, add_comm] using hu
  exact hs.trans (he.trans (add_le_add hc hv))

/-- The candidate indices and interpolation fraction may depend arbitrarily
on validation. Only the finite vertex list is fixed before the draw. -/
theorem adaptive_certificate_failure_mass {Ω ι H : Type*}
    [Fintype Ω] [Fintype ι] [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    (p : Ω → ℝ) (hp : ∀ ω, 0 ≤ p ω) (D : ι → H) (g : H) (v : Ω → H)
    (b : Ω → ι → ℝ) (threshold : ι → ℝ) (i j : Ω → ι) (t : Ω → ℝ)
    (ht : ∀ ω, t ω ∈ Set.Icc (0 : ℝ) 1) (calBad : Ω → Prop) {μ δc δv : ℝ}
    (hc : (∑ ω, if calBad ω then p ω else 0) ≤ δc)
    (hv : (∑ ω, if ∃ k, threshold k < |⟪v ω - g, D k⟫| then p ω else 0) ≤ δv)
    (hb : ∀ ω, ¬ calBad ω → ∀ k, threshold k ≤ b ω k) :
    (∑ ω, if progress μ g (mix (t ω) (D (i ω)) (D (j ω))) <
      certificate μ (v ω) (D (i ω)) (D (j ω)) (b ω (i ω)) (b ω (j ω)) (t ω)
      then p ω else 0) ≤ δc + δv := by
  apply two_stage_failure_bound p hp calBad
    (fun k ω => threshold k < |⟪v ω - g, D k⟫|) _ hc hv
  intro ω hbad
  by_cases hcω : calBad ω
  · exact Or.inl hcω
  · apply Or.inr
    by_contra hn
    have hh : ∀ k, |⟪v ω - g, D k⟫| ≤ b ω k := by
      intro k
      have hk : ¬ threshold k < |⟪v ω - g, D k⟫| := fun hk => hn ⟨k, hk⟩
      exact (le_of_not_gt hk).trans (hb ω hcω k)
    exact (not_lt_of_ge (uniform_certificate (μ := μ) (ht ω) (hh _) (hh _))) hbad

theorem finite_sum_second_moment {Ω ι : Type*} [Fintype Ω] [Fintype ι]
    (p : Ω → ℝ) (x : ι → Ω → ℝ) :
    (∑ ω, p ω * (∑ i, x i ω) ^ 2) = ∑ i, ∑ j, ∑ ω, p ω * x i ω * x j ω := by
  calc
    _ = ∑ ω, ∑ i, ∑ j, p ω * x i ω * x j ω := by
      simp_rw [pow_two, Finset.sum_mul_sum, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro ω _
      apply Finset.sum_congr rfl
      intro i _
      apply Finset.sum_congr rfl
      intro j _
      ring
    _ = _ := by
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro i _
      exact Finset.sum_comm

theorem finite_mean_second_moment {Ω ι : Type*} [Fintype Ω] [Fintype ι]
    [Nonempty ι] (p : Ω → ℝ) (x : ι → Ω → ℝ) {v : ℝ}
    (hoff : ∀ i j, i ≠ j → (∑ ω, p ω * x i ω * x j ω) = 0)
    (hdiag : ∀ i, (∑ ω, p ω * x i ω ^ 2) ≤ v) :
    (∑ ω, p ω * ((∑ i, x i ω) / Fintype.card ι) ^ 2) ≤ v / Fintype.card ι := by
  classical
  have he : (∑ ω, p ω * (∑ i, x i ω) ^ 2) = ∑ i, ∑ ω, p ω * x i ω ^ 2 := by
    rw [finite_sum_second_moment]
    apply Finset.sum_congr rfl
    intro i _
    rw [Finset.sum_eq_single i]
    · simp_rw [pow_two, mul_assoc]
    · intro j _ hji
      exact hoff i j (Ne.symm hji)
    · simp
  have hb : (∑ ω, p ω * (∑ i, x i ω) ^ 2) ≤ (Fintype.card ι : ℝ) * v := by
    rw [he]
    exact (Finset.sum_le_sum (fun i _ => hdiag i)).trans (by simp)
  have hn : (0 : ℝ) < Fintype.card ι := by exact_mod_cast Fintype.card_pos
  calc
    _ = (∑ ω, p ω * (∑ i, x i ω) ^ 2) / (Fintype.card ι : ℝ) ^ 2 := by
      conv_rhs => rw [Finset.sum_div]
      apply Finset.sum_congr rfl
      intro ω _
      rw [div_pow, mul_div_assoc]
    _ ≤ ((Fintype.card ι : ℝ) * v) / (Fintype.card ι : ℝ) ^ 2 :=
      div_le_div_of_nonneg_right hb (sq_nonneg _)
    _ = v / Fintype.card ι := by field_simp

end Creso
