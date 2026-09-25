import Rasp.Core

/-! Finite-support iid sampling, with joint mass p(i)p(j). The direction U
is fixed before the two samples. The result deliberately says nothing about
the adaptively chosen RASP direction or the covariance of momentum. -/

noncomputable section
namespace Rasp
open scoped BigOperators RealInnerProductSpace

theorem iid_split_second_moment {ι : Type*} [Fintype ι]
    (p x : ι → ℝ) (_hp : ∀ i, 0 ≤ p i)
    (hs : ∑ i, p i = 1) (hm : ∑ i, p i * x i = 0) :
    (∑ i, ∑ j, p i * p j * ((x i - x j) / 2) ^ 2) =
      (∑ i, p i * (x i) ^ 2) / 2 ∧
    (∑ i, ∑ j, p i * p j * ((x i + x j) / 2) ^ 2) =
      (∑ i, p i * (x i) ^ 2) / 2 := by
  have he (s : ℝ) :
      (∑ i, ∑ j, p i * p j * ((x i + s * x j) / 2) ^ 2) =
        (∑ i, p i * (x i) ^ 2) * (1 + s ^ 2) / 4 := by
    calc
      _ = ∑ i, ∑ j, ((p i * (x i) ^ 2) * p j / 4 +
          s ^ 2 * p i * (p j * (x j) ^ 2) / 4 +
          s * (p i * x i) * (p j * x j) / 2) := by
        apply Finset.sum_congr rfl
        intro i _
        apply Finset.sum_congr rfl
        intro j _
        ring
      _ = _ := by
        simp only [Finset.sum_add_distrib, ← Finset.sum_div,
          ← Finset.mul_sum, ← Finset.sum_mul, hs, hm]
        ring
  constructor
  · have h := he (-1)
    norm_num only [neg_one_mul, ← sub_eq_add_neg, neg_one_sq] at h
    convert h using 1; ring
  · have h := he 1
    norm_num only [one_mul, one_pow] at h
    convert h using 1; ring

theorem directional_noise_identity {H ι : Type*}
    [NormedAddCommGroup H] [InnerProductSpace ℝ H] [Fintype ι]
    (p : ι → ℝ) (ε : ι → H) (U : H)
    (hp : ∀ i, 0 ≤ p i) (hs : ∑ i, p i = 1)
    (hm : ∑ i, p i * ⟪ε i, U⟫ = 0) :
    (∑ i, ∑ j, p i * p j * ⟪(1 / 2 : ℝ) • (ε i - ε j), U⟫ ^ 2) =
      (∑ i, p i * ⟪ε i, U⟫ ^ 2) / 2 ∧
    (∑ i, ∑ j, p i * p j * ⟪(1 / 2 : ℝ) • (ε i + ε j), U⟫ ^ 2) =
      (∑ i, p i * ⟪ε i, U⟫ ^ 2) / 2 := by
  have h := iid_split_second_moment p (fun i => ⟪ε i, U⟫) hp hs hm
  simpa only [real_inner_smul_left, inner_sub_left, inner_add_left, div_eq_mul_inv,
    one_mul, mul_comm (2 : ℝ)⁻¹] using h

end Rasp
