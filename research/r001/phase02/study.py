"""Fixed paired mechanism experiment; writes immutable raw research artifacts."""

import argparse
import hashlib
import json
import pathlib
import platform
import subprocess
import time
from datetime import datetime, timezone

import numpy as np
import scipy
from laws import independent_evaluation, make_case, progress
from numerics import (
    inner,
    inverse_then_project,
    matched,
    norm,
    ns5,
    polar,
    project,
    soft_clip,
    solve,
    spectral,
)
from scipy.stats import t

HERE = pathlib.Path(__file__).resolve().parent
PROTOCOL = json.loads((HERE / "protocol.json").read_text())
PEERS = [
    "sgd",
    "adamw_step1",
    "ideal_polar",
    "finite_ns5_float64",
    "hard_spectral",
    "soft_spectral",
    "ht_svd",
    "soap_step1_skip",
]


def summary(values, confidence=0.95):
    values = np.asarray(values)
    n = len(values)
    mean = float(values.mean())
    mcse = float(values.std(ddof=1) / np.sqrt(n))
    half = float(t.ppf((1 + confidence) / 2, n - 1) * mcse)
    return {
        "n": n,
        "mean": mean,
        "mcse": mcse,
        "confidence": confidence,
        "lower": mean - half,
        "upper": mean + half,
    }


def peer_direction(name, m, index):
    thresholds = PROTOCOL["spectral_threshold_grid"]
    if name == "sgd":
        return m.copy()
    if name == "adamw_step1":
        epsilon = [1e-8, 1e-3, 1e-2, 0.1, 1.0, 10.0][index]
        return m / (np.abs(m) + epsilon)
    if name == "ideal_polar":
        return polar(m)
    if name == "finite_ns5_float64":
        return ns5(m)
    if name == "hard_spectral":
        return project(m, thresholds[index])
    if name == "soft_spectral":
        return soft_clip(m, thresholds[index])
    if name == "ht_svd":
        u, s, vt = np.linalg.svd(m, full_matrices=False)
        exponent = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0][index]
        values = np.where(s > 1e-12 * np.maximum(s[:, :1], 1e-30), s**exponent, 0)
        return (u * values[:, None, :]) @ vt
    if name == "soap_step1_skip":
        return np.zeros_like(m)
    raise ValueError(name)


def hashes():
    files = sorted(HERE.glob("*.py")) + [HERE / "protocol.json", HERE / "protocol.md"]
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def freeze_check(target):
    expected = json.loads((target / "freeze.json").read_text())
    if expected["hashes"] != hashes():
        raise ValueError(
            "Code/protocol changed after development; create a new revision"
        )


def development(target):
    target.mkdir(parents=True, exist_ok=False)
    rng = np.random.default_rng(PROTOCOL["seeds"]["development"])
    selection, records = {}, []
    for cfg in PROTOCOL["regimes"]:
        case = make_case(rng, cfg, PROTOCOL["development_trials_per_regime"])
        methods = ["rasp"] + PEERS
        selection[cfg["id"]] = {}
        for method in methods:
            trials = []
            for index in range(6):
                if method == "rasp":
                    gamma = PROTOCOL["gamma_grid"][index]
                    d = solve(case["m"], case["e"], gamma=gamma)["direction"]
                else:
                    d = peer_direction(method, case["m"], index)
                for eta in PROTOCOL["stepsize_grid"]:
                    values = progress(d, case["g"], eta)
                    result = {
                        "regime": cfg["id"],
                        "method": method,
                        "index": index,
                        "stepsize": eta,
                        **summary(values),
                    }
                    trials.append(result)
                    records.append(result)
            best = max(trials, key=lambda item: item["mean"])
            selection[cfg["id"]][method] = {k: best[k] for k in ("index", "stepsize")}
        print("development", cfg["id"], selection[cfg["id"]]["rasp"], flush=True)
    (target / "development.json").write_text(json.dumps(records, indent=2) + "\n")
    (target / "selection.json").write_text(json.dumps(selection, indent=2) + "\n")
    (target / "freeze.json").write_text(
        json.dumps(
            {
                "at": datetime.now(timezone.utc).isoformat(),
                "hashes": hashes(),
                "source_commit": subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=HERE, text=True
                ).strip(),
            },
            indent=2,
        )
        + "\n"
    )


def oracle(case, gamma):
    cfg = case["config"]
    bscale, rho = cfg.get("half_b_scale", 1.0), cfg.get("correlation", 0.0)
    covariance_factor = (1 + bscale**2 + 2 * rho * bscale) / 4
    vectors = case["bases"]
    variances = covariance_factor * case["scales"] ** 2
    if vectors.shape[1] == 1:
        e = np.sqrt(variances[:, 0])[:, None, None] * vectors[:, 0]
        result = solve(case["m"], e, gamma=gamma)
        return result["direction"], {
            "svds": int(result["svds"].sum()),
            "conic_solves": 0,
        }
    d = case["m"].copy()
    for k in range(vectors.shape[1]):
        v = vectors[:, k]
        coefficient = gamma * variances[:, k] / (1 + gamma * variances[:, k])
        d -= (coefficient * inner(case["m"], v))[:, None, None] * v
    active = np.flatnonzero(spectral(d) > 1)
    if len(active):
        import cvxpy as cp

        rows, cols = d.shape[-2:]
        for index in active:
            variable = cp.Variable((rows, cols))
            cost = cp.sum_squares(variable) / 2 - cp.sum(
                cp.multiply(case["m"][index], variable)
            )
            for k in range(vectors.shape[1]):
                loading = cp.sum(cp.multiply(vectors[index, k], variable))
                cost += gamma * variances[index, k] * cp.square(loading) / 2
            block = cp.bmat([[np.eye(rows), variable], [variable.T, np.eye(cols)]])
            problem = cp.Problem(cp.Minimize(cost), [block >> 0])
            problem.solve(solver="CLARABEL", tol_gap_abs=1e-9, tol_feas=1e-9)
            if problem.status not in ("optimal", "optimal_inaccurate"):
                raise RuntimeError("Oracle conic solve failed")
            d[index] = variable.value
    return d, {"svds": len(d), "conic_solves": len(active)}


def evaluation(target):
    freeze_check(target)
    output = target / "final"
    output.mkdir(exist_ok=False)
    selection = json.loads((target / "selection.json").read_text())
    rng = np.random.default_rng(PROTOCOL["seeds"]["evaluation"])
    eval_rng = np.random.default_rng(PROTOCOL["seeds"]["independent_loss"])
    reports = {}
    primary_gamma = PROTOCOL["gamma_grid"][
        selection[PROTOCOL["primary_regime"]]["rasp"]["index"]
    ]
    start = time.monotonic()
    for cfg in PROTOCOL["regimes"]:
        case = make_case(rng, cfg, PROTOCOL["final_trials_per_regime"])
        evaluation_noise = independent_evaluation(eval_rng, case)
        chosen = selection[cfg["id"]]
        gamma = PROTOCOL["gamma_grid"][chosen["rasp"]["index"]]
        root = solve(case["m"], case["e"], gamma=gamma)
        plain = solve(case["m"], case["e"], gamma=0)
        shuffled = solve(case["m"], case["shuffled"], gamma=gamma)
        random = solve(case["m"], case["random"], gamma=gamma)
        oracle_d, oracle_work = oracle(case, primary_gamma)
        fixed = solve(case["m"], case["e"], gamma=primary_gamma)
        directions = {
            "rasp": root["direction"],
            "gamma0": plain["direction"],
            "shuffled": shuffled["direction"],
            "random": random["direction"],
            "inverse_then_project": inverse_then_project(
                case["m"], case["e"], gamma=gamma
            ),
            "oracle_unattainable": oracle_d,
            "transfer_primary_gamma": fixed["direction"],
        }
        for name in PEERS:
            directions[name] = peer_direction(name, case["m"], chosen[name]["index"])
        raw = {
            k: case[k]
            for k in [
                "g",
                "a",
                "b",
                "m",
                "e",
                "bases",
                "scales",
                "shuffled",
                "random",
                "donor_permutation",
            ]
        }
        raw["evaluation_noise"] = evaluation_noise
        raw["solver_svds"], raw["solver_iterations"], raw["solver_vi_gap"] = (
            root["svds"],
            root["iterations"],
            root["vi_gap"],
        )
        result = {
            "gamma": gamma,
            "primary_gamma_transfer": primary_gamma,
            "selection": chosen,
            "outcomes": {},
            "contrasts": {},
            "cost": {
                "mean_svds": float(root["svds"].mean()),
                "p95_svds": float(np.quantile(root["svds"], 0.95)),
                "max_svds": int(root["svds"].max()),
                "inactive_fraction": float(root["inactive"].mean()),
                "max_vi_gap": float(root["vi_gap"].max()),
                "oracle": oracle_work,
            },
        }
        eta_fixed = PROTOCOL["primary_stepsize"]
        for name, d in directions.items():
            eta = (
                chosen["rasp"]["stepsize"]
                if name not in PEERS
                else chosen[name]["stepsize"]
            )
            dm = matched(d)
            exact, observed = (
                progress(d, case["g"], eta),
                progress(d, case["g"], eta, evaluation_noise),
            )
            exact_m = progress(dm, case["g"], eta_fixed)
            observed_m = progress(dm, case["g"], eta_fixed, evaluation_noise)
            surrogate = inner(case["e"], dm) ** 2
            independent_risk = inner(evaluation_noise, dm) ** 2
            raw.update(
                {
                    "direction_" + name: d,
                    "true_" + name: exact,
                    "observed_" + name: observed,
                    "matched_true_" + name: exact_m,
                    "matched_observed_" + name: observed_m,
                    "adaptive_surrogate_" + name: surrogate,
                    "independent_risk_" + name: independent_risk,
                }
            )
            result["outcomes"][name] = {
                "true": summary(exact),
                "independent": summary(observed),
                "matched_true": summary(exact_m),
                "matched_independent": summary(observed_m),
                "adaptive_surrogate": summary(surrogate),
                "independent_risk": summary(independent_risk),
                "mean_direction_norm": float(norm(d).mean()),
                "stepsize": eta,
            }
        for name in ["gamma0", "shuffled", "random"] + PEERS:
            paired = raw["matched_observed_rasp"] - raw["matched_observed_" + name]
            true_paired = raw["matched_true_rasp"] - raw["matched_true_" + name]
            confidence = (
                1 - 0.05 / 3
                if cfg["id"] == PROTOCOL["primary_regime"]
                and name in ("gamma0", "shuffled", "random")
                else 0.95
            )
            result["contrasts"][name] = {
                "independent": summary(paired, confidence),
                "true": summary(true_paired, confidence),
            }
        fixed_u = matched(case["g"] + case["bases"][:, 0])
        calibration_e = inner(case["e"], fixed_u) ** 2
        calibration_g = inner((case["a"] + case["b"]) / 2, fixed_u) ** 2
        raw.update(
            {
                "fixed_u": fixed_u,
                "fixed_disagreement": calibration_e,
                "fixed_mean_error": calibration_g,
            }
        )
        result["calibration"] = {
            "disagreement": summary(calibration_e),
            "mean_error": summary(calibration_g),
            "paired_difference": summary(calibration_e - calibration_g),
        }
        if "momentum_signal" in case:
            momentum_noise = case["m"] - case["momentum_signal"]
            raw["momentum_noise"] = momentum_noise
            result["momentum_noise_norm_square"] = summary(
                inner(momentum_noise, momentum_noise)
            )
        np.savez_compressed(output / (cfg["id"] + ".npz"), **raw)
        reports[cfg["id"]] = result
        (output / "results.json").write_text(json.dumps(reports, indent=2) + "\n")
        print(
            "final",
            cfg["id"],
            "gamma",
            gamma,
            "matched advantage",
            result["contrasts"]["gamma0"]["independent"]["mean"],
            flush=True,
        )
    primary = reports[PROTOCOL["primary_regime"]]
    threshold = PROTOCOL["mechanism_threshold_absolute_loss_decrease"]
    passed = all(
        primary["contrasts"][name]["independent"]["lower"] > threshold
        for name in ("gamma0", "shuffled", "random")
    )
    manifest = {
        "at": datetime.now(timezone.utc).isoformat(),
        "hashes": hashes(),
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=HERE, text=True
        ).strip(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "cpu_wall_seconds": time.monotonic() - start,
        "primary_gate_passed": passed,
        "primary_gamma": primary_gamma,
        "raw_files": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(output.glob("*.npz"))
        },
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("PRIMARY GATE", passed, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["develop", "evaluate"])
    parser.add_argument("--output", type=pathlib.Path, default=HERE / "run-v1")
    args = parser.parse_args()
    if args.action == "develop":
        development(args.output)
    else:
        evaluation(args.output)


if __name__ == "__main__":
    main()
