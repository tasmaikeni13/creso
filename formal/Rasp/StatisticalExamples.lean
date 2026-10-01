import Rasp.Statistics

/-! Exact finite arithmetic behind the Phase 02 adaptive-risk counterexample.
The four cells represent independent uniform half-errors in {-1, 1}. This
does not replace the rectangular matrix existence or feasibility theorems. -/

noncomputable section
namespace Rasp

def fourAverage (f : ℝ → ℝ → ℝ) : ℝ :=
  (f (-1) (-1) + f (-1) 1 + f 1 (-1) + f 1 1) / 4

def adaptiveExampleStep (a b : ℝ) : ℝ :=
  ((a + b) / 2) / (1 + ((a - b) / 2) ^ 2)

theorem adaptive_example_realized_zero :
    fourAverage (fun a b => (((a - b) / 2) * adaptiveExampleStep a b) ^ 2) = 0 := by
  norm_num [fourAverage, adaptiveExampleStep]

theorem adaptive_example_step_second_moment :
    fourAverage (fun a b => (adaptiveExampleStep a b) ^ 2) = 1 / 2 := by
  norm_num [fourAverage, adaptiveExampleStep]

/-- Fresh independent mean-error risk is the product of two finite averages;
it is positive while the realized surrogate above is identically zero. -/
theorem adaptive_example_fresh_risk_quarter :
    fourAverage (fun a b => ((a + b) / 2) ^ 2) *
      fourAverage (fun a b => (adaptiveExampleStep a b) ^ 2) = 1 / 4 := by
  norm_num [fourAverage, adaptiveExampleStep]

end Rasp
