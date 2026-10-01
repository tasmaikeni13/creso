"""Independent assumption attacks and host profiles; no method selection."""

import json
import pathlib
import time

import numpy as np
from laws import make_case, split
from numerics import interpolate, ns5, polar, progress, project, solve, spectral
from proximal import solve as proximal_solve

HERE = pathlib.Path(__file__).resolve().parent


def attacks():
    rng = np.random.default_rng(20261025)
    n = 512
    signal = np.zeros((n, 2, 2))
    signal[:, 0, 0] = 1
    noise = np.zeros_like(signal)
    noise[:, 1, 1] = 1
    sign = rng.choice([-1, 1], size=(n, 1, 1))
    shared = sign * signal
    output = solve(
        np.repeat(shared[:, None], 8, axis=1), np.zeros((n, 256, 2, 2)), shared, 640
    )
    truth = progress(output["direction"], np.zeros_like(signal))
    common_fail = output["certificate"] > truth + 1e-10

    pilot = signal[:, None] + 20 * rng.normal(size=(n, 8, 1, 1)) * noise[:, None]
    post = signal[:, None] + 10 * rng.normal(size=(n, 640, 1, 1)) * signal[:, None]
    cal = (post[:, :512:2] - post[:, 1:512:2]) / np.sqrt(2)
    validation = post.mean(axis=1)
    calibrated = solve(pilot, cal, validation, 640)
    omitted = interpolate(
        calibrated["points"], validation, np.zeros_like(calibrated["allowances"])
    )
    calibrated_fail = (
        calibrated["certificate"] > progress(calibrated["direction"], signal) + 1e-10
    )
    omitted_fail = (
        omitted["certificate"] > progress(omitted["direction"], signal) + 1e-10
    )

    a = np.diag([0.5, 0.5])
    b = np.diag([0.5, -0.5])
    points = np.stack([np.zeros((2, 2)), a, b, np.zeros((2, 2))])[None]
    mixture = interpolate(points, signal[:1], np.zeros((1, 4)))
    gain = progress(mixture["direction"], signal[:1])[0] - np.max(
        progress(points, signal[:1, None])
    )
    np.savez_compressed(
        HERE / "diagnostic-raw.npz",
        common_sign=sign,
        common_direction=output["direction"],
        common_certificate=output["certificate"],
        common_true_progress=truth,
        residual_pilot=pilot,
        residual_post=post,
        calibrated_direction=calibrated["direction"],
        omitted_direction=omitted["direction"],
        calibrated_certificate=calibrated["certificate"],
        omitted_certificate=omitted["certificate"],
        mixing_points=points,
        mixing_direction=mixture["direction"],
    )
    return {
        "seed": 20261025,
        "contexts": n,
        "common_noise": {
            "certificate_failures": int(common_fail.sum()),
            "mean_certificate": float(output["certificate"].mean()),
            "mean_true_progress": float(truth.mean()),
        },
        "unlearned_residual_noise": {
            "calibrated_failures": int(calibrated_fail.sum()),
            "omitted_residual_failures": int(omitted_fail.sum()),
            "scope": "post-proposal law is iid Gaussian; proposal law may differ, directions remain frozen",
        },
        "active_interpolation": {
            "progress_gain_over_best_vertex": float(gain),
            "operator_norm": float(spectral(mixture["direction"])[0]),
            "fraction": float(mixture["fraction"][0]),
        },
        "cross_covariance": {
            "true_directional_variance": 1.0,
            "sum_without_factor_two": 0.5,
            "certified_envelope": 1.0,
            "law": "epsilon=Z*diag(1,1); D=diag(.5,.5); P selects first diagonal coordinate",
        },
    }


def profiles():
    rng = np.random.default_rng(20261026)
    result = []
    for side in [8, 32, 64]:
        case = make_case(
            rng,
            {"shape": [side, side], "kind": "isotropic", "sigma": 0, "isotropic": 1},
            4,
        )

        def call(method, case=case):
            if method == "creso":
                pilot, calibration, validation, _ = split(case)
                return solve(pilot, calibration, validation, 640)
            mean = case["replicas"].mean(axis=1)
            if method == "muon_polar":
                return polar(mean, 0.5)
            if method == "muon_ns5_feasible":
                return ns5(mean, 0.5)
            if method == "hard_spectral":
                return project(mean, 0.5)
            e = (case["replicas"][:, 0] - case["replicas"][:, 1]) / 2
            return proximal_solve(mean, e, gamma=1, radius=0.5)

        for method in [
            "creso",
            "muon_polar",
            "muon_ns5_feasible",
            "hard_spectral",
            "rank_one_proximal",
        ]:
            output = call(method)
            samples = []
            for _ in range(7):
                start = time.perf_counter()
                output = call(method)
                samples.append((time.perf_counter() - start) / 4)
            row = {
                "shape": [side, side],
                "method": method,
                "batch": 4,
                "repeats": 7,
                "median_seconds_per_decision": float(np.median(samples)),
                "p95_seconds_per_decision": float(np.quantile(samples, 0.95)),
                "scope": "float64 host, includes replica reductions; excludes gradient generation and communication",
            }
            if method == "rank_one_proximal":
                row["mean_matrix_svds"] = float(np.mean(output["svds"]))
            if method == "creso":
                row.update(matrix_svds=3, sketch_svds=1, scalar_pairs=10)
            result.append(row)
    return result


if __name__ == "__main__":
    (HERE / "diagnostics.json").write_text(
        json.dumps({"attacks": attacks(), "host_profiles": profiles()}, indent=2) + "\n"
    )
