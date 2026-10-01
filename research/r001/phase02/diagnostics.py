"""Persist independent evaluator evidence, coverage, and exact finite cases."""

import json
import pathlib
from fractions import Fraction

import numpy as np
from numerics import certificate, dense_solve, norm, objective, solve
from study import PROTOCOL, summary

HERE = pathlib.Path(__file__).resolve().parent


def main():
    target = HERE / "diagnostics.json"
    if target.exists():
        raise FileExistsError("Diagnostic evidence is immutable")
    rng = np.random.default_rng(PROTOCOL["seeds"]["solver"])
    comparisons = []
    for shape in [(1, 7), (7, 1), (2, 2), (3, 5), (5, 3)]:
        for gamma in [0, 0.1, 10, 1000]:
            m, e = rng.normal(size=shape) * 3, rng.normal(size=shape)
            root = solve(m, e, gamma=gamma)
            independent, status = dense_solve(m, e, gamma=gamma)
            difference = float(
                objective(root["direction"], m, e, gamma=gamma)
                - objective(independent, m, e, gamma=gamma)
            )
            comparisons.append(
                {
                    "shape": shape,
                    "gamma": gamma,
                    "m": m.tolist(),
                    "e": e.tolist(),
                    "root_direction": root["direction"].tolist(),
                    "independent_direction": independent.tolist(),
                    "dense_status": status,
                    "objective_difference": difference,
                    "direction_distance": float(norm(root["direction"] - independent)),
                    "vi_gap": float(root["vi_gap"]),
                    "operator_norm": float(root["operator_norm"]),
                    "svds": int(root["svds"]),
                }
            )
    coverage_rng = np.random.default_rng(PROTOCOL["seeds"]["coverage"])
    cfg = PROTOCOL["coverage"]
    known = 4.5
    intervals = []
    for _ in range(cfg["repetitions"]):
        a, b = coverage_rng.normal(0, 3, size=(2, cfg["samples_per_repetition"]))
        result = summary((a - b) ** 2 / 4)
        result["covers_known_expectation"] = result["lower"] <= known <= result["upper"]
        intervals.append(result)
    rate = np.mean([item["covers_known_expectation"] for item in intervals])
    report = {
        "independent_conic_comparisons": comparisons,
        "max_objective_difference": max(
            abs(item["objective_difference"]) for item in comparisons
        ),
        "max_direction_distance": max(
            item["direction_distance"] for item in comparisons
        ),
        "all_solver_checks_pass": all(
            abs(item["objective_difference"]) < 1e-7
            and item["vi_gap"] < 1e-7
            and item["operator_norm"] <= 1 + 1e-10
            for item in comparisons
        ),
        "coverage": {
            "known_expectation": known,
            "repetitions": cfg["repetitions"],
            "rate": float(rate),
            "binomial_mcse": float(np.sqrt(rate * (1 - rate) / cfg["repetitions"])),
            "passed": bool(
                cfg["acceptance_range"][0] <= rate <= cfg["acceptance_range"][1]
            ),
            "raw_intervals": intervals,
        },
        "exact_finite_population": {
            "support": [-2, 1],
            "probabilities": ["1/3", "2/3"],
            "directional_disagreement_second_moment": "1",
            "directional_mean_error_second_moment": "1",
        },
        "exact_adaptive_counterexample": {
            "signal": 0,
            "half_noise": [-1, 1],
            "probabilities": ["1/2", "1/2"],
            "observed_adaptive_surrogate": "0",
            "independent_adaptive_risk": str(Fraction(1, 4)),
        },
    }
    # Ensure the analytic point is also evaluated by the independently coded VI.
    point = np.diag([1.0, 0.0])
    report["analytic_2x2_vi_gap"] = float(
        certificate(point, np.diag([3.0, 1.0]), np.eye(2))["vi_gap"]
    )
    target.write_text(json.dumps(report, indent=2) + "\n")
    if not (report["all_solver_checks_pass"] and report["coverage"]["passed"]):
        raise RuntimeError("Independent diagnostics failed; retain this artifact")
    print(
        "Independent dense comparisons and coverage pass:", report["coverage"]["rate"]
    )


if __name__ == "__main__":
    main()
