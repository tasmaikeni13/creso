"""Post-study numerical cost attack; preserves the frozen bisection evidence.

Brent interpolation is established numerical analysis. This is a small-matrix
research alternative, not a TPU kernel or a change to the RASP objective.
"""

import hashlib
import json
import pathlib
import sys

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "phase02"))
from laws import progress
from numerics import certificate, inner, matched, norm, project, spectral

HERE = pathlib.Path(__file__).resolve().parent


def brent_solve(m, e, gamma, tolerance=1e-9):
    z = gamma * inner(e, m) / (1 + gamma * inner(e, e))
    d = m - z[:, None, None] * e
    inactive = spectral(d) <= 1
    work = np.ones(len(m), dtype=int)
    for i in np.flatnonzero(~inactive):
        calls = 0

        def feedback(value, mi=m[i], ei=e[i]):
            nonlocal calls
            calls += 1
            point = project(mi - value * ei)
            return float(value - gamma * inner(ei, point))

        f0 = feedback(0)
        bound = abs(f0)
        if bound == 0:
            root = 0.0
        else:
            # Full bisection keeps its stronger explicit residual bound; here
            # interpolation tolerance is followed by an independent VI check.
            root = brentq(
                feedback,
                -bound,
                bound,
                xtol=1e-14,
                rtol=4 * np.finfo(float).eps,
                maxiter=90,
            )
        d[i] = project(m[i] - root * e[i])
        work[i] += calls + 1
    check = certificate(d, m, e, gamma=gamma)
    work += 2
    if np.any(check["vi_gap"] > 5 * tolerance * (1 + norm(m))):
        raise RuntimeError("Brent alternative failed the independent VI check")
    if np.any(check["operator_norm"] > 1 + 1e-11):
        raise RuntimeError("Brent alternative is infeasible")
    return d, work, check["vi_gap"]


def main():
    output = HERE / "solver-attack.json"
    if output.exists():
        raise FileExistsError("Preserve previous numerical cost attacks")
    final = HERE / "phase02/run-v1/final"
    results = json.loads((final / "results.json").read_text())
    report = {
        "label": "exploratory solver cost repair, objective unchanged",
        "source_sha256": hashlib.sha256(
            pathlib.Path(__file__).read_bytes()
        ).hexdigest(),
        "cases": {},
    }
    for name in [
        "rotating_rank_one_gaussian",
        "rank_deficient_signal",
        "near_zero_singular_values",
        "multirank_anisotropic",
    ]:
        raw = np.load(final / (name + ".npz"))
        # Fixed first 512 contexts, selected only by run order, never by effect.
        m, e = raw["m"][:512], raw["e"][:512]
        d, work, vi = brent_solve(m, e, results[name]["gamma"])
        old = raw["direction_rasp"][:512]
        distance = norm(d - old)
        if distance.max() > 1e-7:
            raise RuntimeError("Alternative changes the numerical direction")
        report["cases"][name] = {
            "contexts": 512,
            "bisection_mean_svds": float(raw["solver_svds"][:512].mean()),
            "brent_mean_svds": float(work.mean()),
            "brent_p95_svds": float(np.quantile(work, 0.95)),
            "max_direction_distance": float(distance.max()),
            "max_vi_gap": float(vi.max()),
            "raw_bisection_svds": raw["solver_svds"][:512].tolist(),
            "raw_brent_svds": work.tolist(),
            "raw_direction_distances": distance.tolist(),
        }
    # Mathematical attack from anticorrelated replicas: A=g+e, B=g-e.
    # Mean is noiseless while disagreement removes a useful signal component.
    g, e = np.diag([0.6, 0.8]), np.diag([1.0, 0.0])
    d = np.diag([0.15, 0.8])  # unconstrained gamma=3 solution, already feasible
    check = certificate(d, g, e, gamma=3)
    report["anticorrelated_replica_attack"] = {
        "label": "deterministic numerical counterexample, not iid replica regime",
        "g": g.tolist(),
        "e": e.tolist(),
        "a": (g + e).tolist(),
        "b": (g - e).tolist(),
        "gamma": 3,
        "direction": d.tolist(),
        "vi_gap": float(check["vi_gap"]),
        "matched_true_loss_decrease_difference": float(
            progress(matched(d), g, 0.3) - progress(g, g, 0.3)
        ),
        "mean_noise_variance": 0,
        "disagreement_second_moment": 1,
    }
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(
        {
            name: {
                key: value for key, value in result.items() if not key.startswith("raw")
            }
            for name, result in report["cases"].items()
        }
    )


if __name__ == "__main__":
    main()
