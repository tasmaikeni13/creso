"""Recompute evidence from lossless raw inputs with an independent readout."""

import csv
import hashlib
import json
import pathlib

import matplotlib
import numpy as np
from scipy.stats import beta
from study import Context

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "run-v1" / "final"


def readout(d, gradient):
    return np.einsum("bij,bij->b", d, gradient) - 0.5 * np.einsum("bij,bij->b", d, d)


def analyze():
    saved = json.loads((OUT / "results.json").read_text())
    manifest = json.loads((OUT / "manifest.json").read_text())
    rows, replay, samples = [], [], {}
    for law, result in saved["laws"].items():
        files = [row for row in manifest["files"] if row["path"].startswith(law + "-")]
        sample = {method: [] for method in result["methods"]}
        max_error, max_readout, max_feasibility = 0.0, 0.0, 0.0
        trace_failures, oracle_failures, interpolation_count = 0, 0, 0
        for row in files:
            path = OUT / row["path"]
            if hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
                raise ValueError("Raw hash mismatch")
            with np.load(path) as raw:
                context = Context({"replicas": raw["replicas"]})
                creso, diagnostic = context.direction(
                    "creso", result["selection"]["creso"]
                )
                for method in result["methods"]:
                    direction = raw[f"{method}_direction"]
                    actual = readout(direction, raw["g"])
                    observed = readout(direction, raw["evaluation_mean"])
                    sample[method].append(actual)
                    max_readout = max(
                        max_readout,
                        float(np.max(np.abs(actual - raw[f"{method}_progress"]))),
                        float(np.max(np.abs(observed - raw[f"{method}_assessment"]))),
                    )
                    op = np.linalg.norm(direction, ord=2, axis=(-2, -1))
                    max_feasibility = max(max_feasibility, float(np.max(op - 0.5)))
                    if method in result["selection"]:
                        reproduced = (
                            creso
                            if method == "creso"
                            else context.direction(method, result["selection"][method])[
                                0
                            ]
                        )
                        max_error = max(
                            max_error, float(np.max(np.abs(reproduced - direction)))
                        )
                basis = diagnostic["basis"]
                vectors = raw["vectors"].reshape(len(creso), 2, -1)
                coordinates = np.einsum("bkd,bld->bkl", basis, vectors)
                qp = np.sum(raw["sigma"] ** 2 * np.sum(coordinates**2, axis=1), axis=1)
                rank = np.sum(basis**2, axis=(-2, -1))
                qp += raw["isotropic"] ** 2 * rank
                total = (
                    np.sum(raw["sigma"] ** 2, axis=1)
                    + raw["isotropic"] ** 2 * vectors.shape[-1]
                )
                qr = np.maximum(0, total - qp)
                trace_failures += int(
                    np.sum(
                        (qp > raw["diagnostic_upper_span"] + 1e-8)
                        | (qr > raw["diagnostic_upper_rest"] + 1e-8)
                    )
                )
                points = raw["candidate_points"]
                true_vertex = np.einsum(
                    "bkij,bij->bk", points, raw["g"]
                ) - 0.5 * np.sum(points**2, axis=(-2, -1))
                lower = np.max(true_vertex - 2 * raw["candidate_allowances"], axis=1)
                oracle_failures += int(np.sum(lower > readout(creso, raw["g"]) + 1e-10))
                fraction = raw["diagnostic_fraction"]
                interpolation_count += int(
                    np.sum((fraction > 1e-8) & (fraction < 1 - 1e-8))
                )
        sample = {k: np.concatenate(v) for k, v in sample.items()}
        samples[law] = sample
        for method, values in sample.items():
            if abs(float(values.mean()) - result["methods"][method]["mean"]) > 1e-12:
                raise ValueError("Saved aggregate mismatch")
            rows.append(
                {
                    "law": law,
                    "method": method,
                    "mean_progress": float(values.mean()),
                    "active_fraction_creso": result["active_fraction"],
                    "certificate_failures_creso": result["certificate_failures"],
                }
            )
        if max_error > 1e-12 or max_readout > 1e-12 or max_feasibility > 1e-10:
            raise ValueError("Replay/readout/feasibility disagreement")
        replay.append(
            {
                "law": law,
                "files": len(files),
                "contexts": len(sample["creso"]),
                "max_direction_replay_error": max_error,
                "max_independent_readout_error": max_readout,
                "max_operator_excess": max_feasibility,
                "trace_upper_failures": trace_failures,
                "in_library_oracle_violations": oracle_failures,
                "interior_interpolations": interpolation_count,
            }
        )
        print(
            "verified", law, "replay", max_error, "traces", trace_failures, flush=True
        )

    # Prespecified paired bootstrap sensitivity, never used to select a method.
    rng = np.random.default_rng(saved["protocol"]["seeds"]["bootstrap"])
    bootstrap = []
    for law in saved["protocol"]["primary_laws"]:
        for method in saved["protocol"]["primary_peers"]:
            effect = samples[law]["creso"] - samples[law][method]
            means = np.concatenate(
                [
                    effect[rng.integers(0, len(effect), size=(100, len(effect)))].mean(
                        axis=1
                    )
                    for _ in range(20)
                ]
            )
            lower, upper = np.quantile(means, [0.05 / 18, 1 - 0.05 / 18])
            bootstrap.append(
                {
                    "law": law,
                    "peer": method,
                    "replicates": 2000,
                    "family_adjusted_lower": float(lower),
                    "family_adjusted_upper": float(upper),
                }
            )
    with (HERE / "summary.csv").open("w") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "contexts": sum(row["contexts"] for row in replay),
        "raw_files": len(manifest["files"]),
        "raw_bytes": sum(row["bytes"] for row in manifest["files"]),
        "replay": replay,
        "bootstrap": bootstrap,
        "coverage_error_upper_zero_failures_per_law": float(
            beta.ppf(1 - 0.05 / 10, 1, 4096)
        ),
    }
    (HERE / "reproduction-checks.json").write_text(json.dumps(report, indent=2) + "\n")

    labels = list(saved["laws"])
    width = 0.17
    fig, axis = plt.subplots(figsize=(13, 6))
    for index, method in enumerate(
        ["creso", "muon_polar", "muon_ns5_feasible", "hard_spectral", "tonga_project"]
    ):
        values = [saved["laws"][law]["methods"][method]["mean"] for law in labels]
        axis.bar(
            np.arange(len(labels)) + (index - 2) * width, values, width, label=method
        )
    axis.axhline(0, color="black", linewidth=0.6)
    axis.set_xticks(np.arange(len(labels)), labels, rotation=40, ha="right")
    axis.set_ylabel("Population quadratic progress (higher is better)")
    axis.set_title(
        "CRESO: frozen one-step study; each peer may average all 648 replicas"
    )
    axis.legend(ncol=3, fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "results.svg")
    fig.savefig(HERE / "results.png", dpi=180)


if __name__ == "__main__":
    analyze()
