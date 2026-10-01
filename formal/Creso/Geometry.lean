import Mathlib

noncomputable section
namespace Creso
open scoped RealInnerProductSpace Matrix.Norms.L2Operator

abbrev Mat (m n : ℕ) := EuclideanSpace ℝ (Fin m × Fin n)

def matrixEquiv (m n : ℕ) : Mat m n ≃ₗ[ℝ] Matrix (Fin m) (Fin n) ℝ where
  toFun A i j := A (i, j)
  invFun A := WithLp.toLp 2 (fun ij => A ij.1 ij.2)
  left_inv A := by ext ij; rfl
  right_inv A := by ext i j; rfl
  map_add' A B := by ext i j; rfl
  map_smul' c A := by ext i j; rfl

def asOperator (m n : ℕ) :
    Mat m n ≃L[ℝ] (EuclideanSpace ℝ (Fin n) →L[ℝ] EuclideanSpace ℝ (Fin m)) :=
  (((matrixEquiv m n).trans Matrix.toEuclideanLin).trans
    LinearMap.toContinuousLinearMap).toContinuousLinearEquiv

def spectralBall (m n : ℕ) (r : ℝ) : Set (Mat m n) :=
  (asOperator m n) ⁻¹' Metric.closedBall 0 r

theorem mem_spectralBall {m n : ℕ} {r : ℝ} {D : Mat m n} :
    D ∈ spectralBall m n r ↔ ‖asOperator m n D‖ ≤ r := by
  simp [spectralBall, Metric.mem_closedBall, dist_zero_right]

theorem spectralBall_convex (m n : ℕ) (r : ℝ) : Convex ℝ (spectralBall m n r) :=
  (convex_closedBall (0 : EuclideanSpace ℝ (Fin n) →L[ℝ]
    EuclideanSpace ℝ (Fin m)) r).linear_preimage (asOperator m n).toLinearMap

theorem spectralBall_compact (m n : ℕ) (r : ℝ) : IsCompact (spectralBall m n r) :=
  (asOperator m n).toHomeomorph.isCompact_preimage.mpr (isCompact_closedBall 0 r)

theorem zero_mem_spectralBall (m n : ℕ) {r : ℝ} (hr : 0 ≤ r) :
    (0 : Mat m n) ∈ spectralBall m n r := by
  rw [mem_spectralBall, map_zero, norm_zero]
  exact hr

theorem asOperator_apply {m n : ℕ} (A : Mat m n)
    (v : EuclideanSpace ℝ (Fin n)) (i : Fin m) :
    asOperator m n A v i = ∑ j, A (i, j) * v j := rfl

theorem entry_le_opNorm {m n : ℕ} (A : Mat m n) (i : Fin m) (j : Fin n) :
    A (i, j) ≤ ‖asOperator m n A‖ := by
  let v : EuclideanSpace ℝ (Fin n) := EuclideanSpace.single j 1
  have ha : asOperator m n A v i = A (i, j) := by
    rw [asOperator_apply]
    simp [v]
  have hn : ‖v‖ = 1 := by simp [v]
  have h := (PiLp.norm_apply_le (asOperator m n A v) i).trans
    ((asOperator m n A).le_opNorm v)
  rw [ha, hn, mul_one, Real.norm_eq_abs] at h
  exact (le_abs_self _).trans h

theorem frobenius_inner {m n : ℕ} (A B : Mat m n) :
    ⟪A, B⟫ = ∑ i, ∑ j, A (i, j) * B (i, j) := by
  simp [PiLp.inner_apply, Fintype.sum_prod_type, mul_comm]

def diag₂ (a b : ℝ) : Mat 2 2 :=
  (matrixEquiv 2 2).symm (Matrix.diagonal ![a, b])

theorem diag₂_feasible {a b : ℝ} (ha : |a| ≤ 1) (hb : |b| ≤ 1) :
    diag₂ a b ∈ spectralBall 2 2 1 := by
  rw [mem_spectralBall]
  change ‖(Matrix.diagonal ![a, b] : Matrix (Fin 2) (Fin 2) ℝ)‖ ≤ 1
  rw [Matrix.l2_opNorm_diagonal]
  apply (pi_norm_le_iff_of_nonneg (by norm_num : (0 : ℝ) ≤ 1)).mpr
  intro i
  fin_cases i
  · simpa [Real.norm_eq_abs] using ha
  · simpa [Real.norm_eq_abs] using hb

theorem inner_diag₂ (a b : ℝ) (V : Mat 2 2) :
    ⟪diag₂ a b, V⟫ = a * V (0, 0) + b * V (1, 1) := by
  simp [frobenius_inner, diag₂, matrixEquiv, Matrix.diagonal,
    Fin.sum_univ_two]


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

end Creso
