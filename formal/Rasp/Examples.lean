import Rasp.Matrix

noncomputable section
namespace Rasp
open scoped RealInnerProductSpace Matrix.Norms.L2Operator

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

theorem counterexample_optimal :
    Solves (spectralBall 2 2 1) 1 1 (diag₂ 3 1) (diag₂ 1 1) (diag₂ 1 0) := by
  apply vi_solves (by norm_num) (by norm_num)
  refine ⟨diag₂_feasible (by norm_num) (by norm_num), fun V hv => ?_⟩
  have h := (entry_le_opNorm V 0 0).trans (mem_spectralBall.mp hv)
  simp only [residual, inner_sub_left, inner_add_left, real_inner_smul_left,
    inner_sub_right, inner_diag₂]
  norm_num [diag₂, matrixEquiv, Matrix.diagonal]
  linarith

/-- The unconstrained metric minimizer for this instance. -/
theorem counterexample_unconstrained :
    Solves Set.univ 1 1 (diag₂ 3 1) (diag₂ 1 1) (diag₂ (5 / 3) (-1 / 3)) := by
  apply vi_solves (by norm_num) (by norm_num)
  refine ⟨Set.mem_univ _, fun V _ => ?_⟩
  simp only [residual, inner_sub_left, inner_add_left, real_inner_smul_left,
    inner_sub_right, inner_diag₂]
  norm_num [diag₂, matrixEquiv, Matrix.diagonal]
  linarith

/-- Euclidean projection of the unconstrained metric solution gives the wrong step. -/
theorem counterexample_projected :
    Solves (spectralBall 2 2 1) 1 0 (diag₂ (5 / 3) (-1 / 3)) 0
      (diag₂ 1 (-1 / 3)) := by
  apply vi_solves (by norm_num) (by norm_num)
  refine ⟨diag₂_feasible (by norm_num) (by norm_num), fun V hv => ?_⟩
  have h := (entry_le_opNorm V 0 0).trans (mem_spectralBall.mp hv)
  simp only [residual, inner_sub_left, inner_add_left, real_inner_smul_left,
    inner_sub_right, inner_diag₂]
  norm_num [diag₂, matrixEquiv, Matrix.diagonal]
  linarith

theorem counterexample_gap :
    objective 1 1 (diag₂ 3 1) (diag₂ 1 1) (diag₂ 1 (-1 / 3)) -
      objective 1 1 (diag₂ 3 1) (diag₂ 1 1) (diag₂ 1 0) = 1 / 9 := by
  simp only [objective, inner_diag₂]
  norm_num [diag₂, matrixEquiv, Matrix.diagonal]

end Rasp
