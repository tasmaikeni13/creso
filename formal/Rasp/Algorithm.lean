import Rasp.Matrix

noncomputable section
namespace Rasp
open scoped RealInnerProductSpace
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

def halfMean (A B : H) : H := (1 / 2 : ℝ) • (A + B)
def halfDifference (A B : H) : H := (1 / 2 : ℝ) • (A - B)
def momentum (β : ℝ) (previous A B : H) : H :=
  β • previous + (1 - β) • halfMean A B
def parameterUpdate (η : ℝ) (W D : H) : H := W - η • D

def momentumSequence (β : ℝ) (A B : ℕ → H) : ℕ → H
  | 0 => 0
  | t + 1 => momentum β (momentumSequence β A B t) (A (t + 1)) (B (t + 1))

theorem momentumSequence_zero (β : ℝ) (A B : ℕ → H) :
    momentumSequence β A B 0 = 0 := rfl

theorem momentumSequence_succ (β : ℝ) (A B : ℕ → H) (t : ℕ) :
    momentumSequence β A B (t + 1) =
      momentum β (momentumSequence β A B t) (A (t + 1)) (B (t + 1)) := rfl

theorem centered_split (g a b : H) :
    halfMean (g + a) (g + b) - g = halfMean a b ∧
      halfDifference (g + a) (g + b) = halfDifference a b := by
  constructor <;> dsimp [halfMean, halfDifference] <;> module

/-- Swapping the two replica groups has no effect on the exact step. -/
theorem disagreement_sign_invariant {K : Set H} (hK : Convex ℝ K)
    {μ γ : ℝ} (hμ : 0 < μ) (hγ : 0 ≤ γ) {M E D V : H}
    (hD : Solves K μ γ M E D) (hV : Solves K μ γ M (-E) V) : D = V := by
  apply solution_unique hK hμ hγ hD
  simpa only [Solves, objective, inner_neg_left, neg_sq] using hV

end Rasp
