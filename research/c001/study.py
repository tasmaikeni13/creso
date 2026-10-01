"""Paired, immutable one-step study. Population labels never enter a method."""

import argparse
import hashlib
import json
import pathlib
import subprocess
import time
from datetime import datetime, timezone

import numpy as np
from laws import make_case, split
from numerics import (
    interpolate,
    norm,
    ns5,
    polar,
    progress,
    project,
    projected,
    radial,
    solve,
    spectral,
)
from proximal import solve as proximal_solve
from scipy.stats import beta, t

HERE = pathlib.Path(__file__).resolve().parent
PROTOCOL = json.loads((HERE / "protocol.json").read_text())
METHODS = [
    "creso",
    "muon_polar",
    "muon_ns5_feasible",
    "hard_spectral",
    "soft_spectral",
    "sgd_radial",
    "adamw_step1",
    "spectral_power",
    "deflate_fullmean",
    "tonga_project",
    "rank_one_proximal",
    "uncertified",
    "reuse_validation",
]


def hashes():
    files = [
        "study.py",
        "laws.py",
        "numerics.py",
        "test_numerics.py",
        "proximal.py",
        "protocol.json",
        "protocol.md",
    ]
    result = {
        name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in files
    }
    return result


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def summary(values, error=0.05):
    n = len(values)
    mean = float(np.mean(values))
    sd = float(np.std(values, ddof=1))
    se = sd / np.sqrt(n)
    half = float(t.ppf(1 - error / 2, n - 1) * se)
    return {
        "n": n,
        "mean": mean,
        "sd": sd,
        "mcse": se,
        "lower": mean - half,
        "upper": mean + half,
        "error": error,
        "win_fraction": float(np.mean(values > 1e-12)),
        "quantiles": np.quantile(values, [0, 0.01, 0.1, 0.5, 0.9, 0.99, 1]).tolist(),
        "paired_effect_dz": mean / sd if sd > 1e-12 else None,
    }


class Context:
    def __init__(self, case):
        self.pilot, self.cal, self.validation, self.full = split(case)
        self.cache = {}
        self.radius = PROTOCOL["radius"]

    def creso(self, rank):
        if rank not in self.cache:
            self.cache[rank] = solve(
                self.pilot,
                self.cal,
                self.validation,
                PROTOCOL["validation_mean_replicas"],
                rank=rank,
                radius=self.radius,
                delta=PROTOCOL["delta"],
                kurtosis=PROTOCOL["kurtosis_bound"],
            )
        return self.cache[rank]

    def direction(self, name, index):
        if name in {"creso", "deflate_fullmean", "uncertified", "reuse_validation"}:
            rank = PROTOCOL["rank_grid"][index // 6]
            cfg = self.creso(rank)
            if name == "creso":
                multiplier = PROTOCOL["inflation_grid"][index % 6]
                bounds = multiplier * cfg["allowances"]
                output = interpolate(cfg["points"], self.validation, bounds)
                return output["direction"], {**cfg, **output, "allowances": bounds}
            scale = PROTOCOL["control_scale_grid"][index % 6]
            if name == "deflate_fullmean":
                base = self.full - projected(self.full, cfg["basis"])
            else:
                mean = (
                    self.validation
                    if name == "uncertified"
                    else self.pilot.mean(axis=1)
                )
                bounds = (
                    np.zeros_like(cfg["allowances"])
                    if name == "uncertified"
                    else cfg["allowances"]
                )
                base = interpolate(cfg["points"], mean, bounds)["direction"]
            return radial(scale * base, self.radius), {}
        shape = index // 4
        scale = PROTOCOL["scale_grid"][index % 4]
        threshold = PROTOCOL["threshold_grid"][shape]
        m = self.full
        if name == "muon_polar":
            base = polar(m, self.radius)
        elif name == "muon_ns5_feasible":
            # Six zero-state momentum values give only scale-equivalent inputs.
            momentum = [0, 0.5, 0.8, 0.9, 0.95, 0.99][shape]
            base = ns5((1 - momentum) * m, self.radius)
        elif name == "hard_spectral":
            base = project(m, threshold)
        elif name == "soft_spectral":
            u, s, vt = np.linalg.svd(m, full_matrices=False)
            values = threshold * s / np.sqrt(threshold**2 + s**2)
            base = (u * values[:, None, :]) @ vt
        elif name == "sgd_radial":
            base = threshold * m
        elif name == "adamw_step1":
            base = m / (np.abs(m) + PROTOCOL["epsilon_grid"][shape])
        elif name == "spectral_power":
            u, s, vt = np.linalg.svd(m, full_matrices=False)
            power = PROTOCOL["power_grid"][shape]
            values = np.where(s > 1e-12 * np.maximum(s[:, :1], 1e-30), s**power, 0)
            base = (u * values[:, None, :]) @ vt
        elif name == "tonga_project":
            differences = (self.pilot[:, ::2] - self.pilot[:, 1::2]) / np.sqrt(2)
            flat = differences.reshape(len(m), 4, -1)
            _, s, vt = np.linalg.svd(flat, full_matrices=False)
            lam = PROTOCOL["shrinkage_grid"][shape]
            mf = m.reshape(len(m), -1)
            coordinates = np.einsum("bkd,bd->bk", vt, mf)
            shrink = lam * s**2 / 4
            reduction = np.einsum("bk,bkd->bd", coordinates * shrink / (1 + shrink), vt)
            base = project((mf - reduction).reshape(m.shape), self.radius)
        elif name == "rank_one_proximal":
            e = (self.pilot[:, 0] - self.pilot[:, 1]) / 2
            base = proximal_solve(
                m, e, gamma=PROTOCOL["shrinkage_grid"][shape], radius=self.radius
            )["direction"]
        else:
            raise ValueError(name)
        return radial(scale * base, self.radius), {}


def develop(target):
    target.mkdir(parents=True, exist_ok=False)
    rng = np.random.default_rng(PROTOCOL["seeds"]["development"])
    records, selected = [], {}
    for config in PROTOCOL["regimes"]:
        case = make_case(rng, config, PROTOCOL["development_contexts_per_law"])
        context = Context(case)
        selected[config["id"]] = {}
        raw = {**case}
        for method in METHODS:
            trials = []
            for index in range(24):
                direction, _ = context.direction(method, index)
                values = progress(direction, case["g"])
                row = {
                    "law": config["id"],
                    "method": method,
                    "configuration": index,
                    **summary(values),
                }
                trials.append(row)
                records.append(row)
                raw[f"{method}_{index}_progress"] = values
            best = max(trials, key=lambda row: row["mean"])
            selected[config["id"]][method] = best["configuration"]
        np.savez_compressed(target / f"development-{config['id']}.npz", **raw)
        print("development", config["id"], selected[config["id"]]["creso"], flush=True)
    write_json(target / "development.json", records)
    write_json(target / "selection.json", selected)
    write_json(
        target / "freeze.json",
        {
            "at": datetime.now(timezone.utc).isoformat(),
            "hashes": hashes(),
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=HERE, text=True
            ).strip(),
            "selections_sha256": hashlib.sha256(
                (target / "selection.json").read_bytes()
            ).hexdigest(),
        },
    )


def final(target):
    freeze = json.loads((target / "freeze.json").read_text())
    if freeze["hashes"] != hashes():
        raise ValueError("Frozen code changed: archive this attempt; create a new run")
    selections = json.loads((target / "selection.json").read_text())
    if (
        hashlib.sha256((target / "selection.json").read_bytes()).hexdigest()
        != freeze["selections_sha256"]
    ):
        raise ValueError("Frozen selection changed")
    out = target / "final"
    out.mkdir(exist_ok=False)
    rng = np.random.default_rng(PROTOCOL["seeds"]["final"])
    results, manifest = {}, []
    for config in PROTOCOL["regimes"]:
        start = time.perf_counter()
        paired = {method: [] for method in METHODS + ["zero", "matched_fullmean"]}
        noisy = {method: [] for method in paired}
        diagnostic = {
            key: []
            for key in [
                "certificate",
                "certificate_failure",
                "vertex_failure",
                "operator_norm",
                "active",
                "fraction",
                "selected",
                "q_span",
                "q_rest",
                "upper_span",
                "upper_rest",
                "latent",
            ]
        }
        for batch in range(
            PROTOCOL["final_contexts_per_law"] // PROTOCOL["batch_size"]
        ):
            case = make_case(rng, config, PROTOCOL["batch_size"])
            context = Context(case)
            raw = {**case}
            creso_direction, certificate = context.direction(
                "creso", selections[config["id"]]["creso"]
            )
            for method in METHODS + ["zero", "matched_fullmean"]:
                if method == "zero":
                    direction = np.zeros_like(case["g"])
                elif method == "matched_fullmean":
                    factor = norm(creso_direction) / np.maximum(
                        norm(context.full), 1e-30
                    )
                    direction = radial(
                        factor[:, None, None] * context.full, context.radius
                    )
                elif method == "creso":
                    direction = creso_direction
                else:
                    direction, _ = context.direction(
                        method, selections[config["id"]][method]
                    )
                raw[f"{method}_direction"] = direction
                value = progress(direction, case["g"])
                measured = progress(direction, case["evaluation_mean"])
                paired[method].append(value)
                noisy[method].append(measured)
                raw[f"{method}_progress"] = value
                raw[f"{method}_assessment"] = measured
                if np.any(
                    spectral(direction)
                    > context.radius + PROTOCOL["feasibility_tolerance"]
                ):
                    raise RuntimeError(f"Infeasible {method}")
            points = certificate["points"]
            error = context.validation - case["g"]
            observed = np.abs(np.einsum("bij,bkij->bk", error, points))
            operator = spectral(creso_direction)
            values = {
                "certificate": certificate["certificate"],
                "certificate_failure": certificate["certificate"]
                > paired["creso"][-1] + 1e-10,
                "vertex_failure": np.any(
                    observed > certificate["allowances"] + 1e-10, axis=1
                ),
                "operator_norm": operator,
                "active": operator >= context.radius - PROTOCOL["active_tolerance"],
                "fraction": certificate["fraction"],
                "selected": certificate["selected"],
                "q_span": certificate["q_span"],
                "q_rest": certificate["q_rest"],
                "upper_span": certificate["upper_span"],
                "upper_rest": certificate["upper_rest"],
                "latent": case["latent"],
            }
            for key, value in values.items():
                diagnostic[key].append(value)
                raw[f"diagnostic_{key}"] = value
            raw["candidate_points"] = points
            raw["candidate_allowances"] = certificate["allowances"]
            raw["proposal_basis"] = certificate["basis"]
            path = out / f"{config['id']}-{batch:03}.npz"
            np.savez_compressed(path, **raw)
            manifest.append(
                {
                    "path": path.name,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "bytes": path.stat().st_size,
                }
            )
        paired = {k: np.concatenate(v) for k, v in paired.items()}
        noisy = {k: np.concatenate(v) for k, v in noisy.items()}
        diagnostic = {k: np.concatenate(v) for k, v in diagnostic.items()}
        primary_error = 0.05 / (
            len(PROTOCOL["primary_laws"]) * len(PROTOCOL["primary_peers"])
        )
        contrasts = {
            method: summary(paired["creso"] - paired[method], error=primary_error)
            for method in paired
            if method != "creso"
        }
        n = len(paired["creso"])
        failures = int(diagnostic["certificate_failure"].sum())
        # Simultaneous across ten valid-law coverage checks.
        coverage_upper = (
            float(beta.ppf(1 - 0.05 / 10, failures + 1, n - failures))
            if failures < n
            else 1.0
        )
        primary_gate = all(
            contrasts[peer]["lower"] > 0.01 for peer in PROTOCOL["primary_peers"]
        )
        mechanism = summary(paired["creso"] - paired["deflate_fullmean"])
        results[config["id"]] = {
            "configuration": config,
            "selection": selections[config["id"]],
            "methods": {method: summary(values) for method, values in paired.items()},
            "contrasts_family_adjusted": contrasts,
            "independent_assessment": {
                method: summary(noisy["creso"] - noisy[method])
                for method in noisy
                if method != "creso"
            },
            "active_fraction": float(diagnostic["active"].mean()),
            "zero_fraction": float(np.mean(np.abs(paired["creso"]) < 1e-14)),
            "certificate_failures": failures,
            "vertex_failures": int(diagnostic["vertex_failure"].sum()),
            "coverage_failure_upper_simultaneous": coverage_upper,
            "primary_gate": primary_gate
            if config["id"] in PROTOCOL["primary_laws"]
            else None,
            "mechanism_contrast": mechanism
            if config["id"] == PROTOCOL["mechanism_law"]
            else None,
            "host_seconds_including_generation_and_raw_write": time.perf_counter()
            - start,
        }
        print(
            "final",
            config["id"],
            "progress",
            results[config["id"]]["methods"]["creso"]["mean"],
            "primary",
            results[config["id"]]["primary_gate"],
            "failures",
            failures,
            flush=True,
        )
    gates = {
        "primary_effects": all(
            results[law]["primary_gate"] for law in PROTOCOL["primary_laws"]
        ),
        "active_constraint": all(
            results[law]["active_fraction"] >= 0.9 for law in PROTOCOL["primary_laws"]
        ),
        "mixed_signal_validation": results["mixed_signal"]["mechanism_contrast"][
            "lower"
        ]
        > 0.01,
        "valid_law_coverage": all(
            row["coverage_failure_upper_simultaneous"] < 0.05
            for row in results.values()
            if row["configuration"]["certificate_assumptions"]
        ),
        "feasibility": True,
    }
    write_json(
        out / "manifest.json",
        {
            "files": manifest,
            "freeze": freeze,
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=HERE, text=True
            ).strip(),
        },
    )
    write_json(
        out / "results.json", {"protocol": PROTOCOL, "gates": gates, "laws": results}
    )
    print("gates", gates, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["develop", "final"])
    parser.add_argument("--target", type=pathlib.Path, default=HERE / "run-v1")
    args = parser.parse_args()
    (develop if args.action == "develop" else final)(args.target)
