import Rasp.Solver

/-! Actual rectangular matrices: the ambient norm is Frobenius, while the
constraint uses the induced Euclidean operator norm. Keeping the two types
separate prevents an accidental change of matrix norm instances. -/

noncomputable section
namespace Rasp
open scoped RealInnerProductSpace

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

theorem matrix_exists_unique {m n : ℕ} {r μ γ : ℝ}
    (hr : 0 ≤ r) (hμ : 0 < μ) (hγ : 0 ≤ γ) (M E : Mat m n) :
    ∃! D, Solves (spectralBall m n r) μ γ M E D := by
  obtain ⟨D, hd⟩ := exists_solution (spectralBall_compact m n r)
    ⟨0, zero_mem_spectralBall m n hr⟩ μ γ M E
  exact ⟨D, hd, fun V hv => solution_unique (spectralBall_convex m n r) hμ hγ hv hd⟩

/-- The executable algorithm is future work; this is the uniquely specified step. -/
def matrixStep {m n : ℕ} {r μ γ : ℝ}
    (hr : 0 ≤ r) (hμ : 0 < μ) (hγ : 0 ≤ γ) (M E : Mat m n) : Mat m n :=
  Classical.choose (matrix_exists_unique hr hμ hγ M E)

theorem matrixStep_solves {m n : ℕ} {r μ γ : ℝ}
    (hr : 0 ≤ r) (hμ : 0 < μ) (hγ : 0 ≤ γ) (M E : Mat m n) :
    Solves (spectralBall m n r) μ γ M E (matrixStep hr hμ hγ M E) :=
  (Classical.choose_spec (matrix_exists_unique hr hμ hγ M E)).1

theorem matrixStep_feasible {m n : ℕ} {r μ γ : ℝ}
    (hr : 0 ≤ r) (hμ : 0 < μ) (hγ : 0 ≤ γ) (M E : Mat m n) :
    ‖asOperator m n (matrixStep hr hμ hγ M E)‖ ≤ r :=
  mem_spectralBall.mp (matrixStep_solves hr hμ hγ M E).1

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

end Rasp
