"""Recompute summaries from preserved raw evidence and draw a standalone figure."""

import csv
import hashlib
import json
import pathlib
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "phase02"))
from study import PROTOCOL, summary

HERE = pathlib.Path(__file__).resolve().parent
FINAL = HERE / "phase02/run-v1/final"


def main():
    results = json.loads((FINAL / "results.json").read_text())
    manifest = json.loads((FINAL / "manifest.json").read_text())
    audit = {
        "raw_hashes_match": True,
        "summaries_recomputed": True,
        "primary_gate_passed": manifest["primary_gate_passed"],
        "raw_directory": str(FINAL.relative_to(HERE)),
        "raw_storage": "local workspace, excluded from Git per AGENTS.md; regenerate with frozen commands",
        "raw_bytes": 0,
        "matplotlib": matplotlib.__version__,
        "transfer_primary_gamma": {},
        "peer_raw_contrasts": {},
    }
    rows = []
    for cfg in PROTOCOL["regimes"]:
        name = cfg["id"]
        path = FINAL / (name + ".npz")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != manifest["raw_files"][path.name]:
            raise ValueError("Raw data hash differs: " + name)
        audit["raw_bytes"] += path.stat().st_size
        raw = np.load(path)
        result = results[name]
        for control in result["contrasts"]:
            stored = result["contrasts"][control]["independent"]
            measured = summary(
                raw["matched_observed_rasp"] - raw["matched_observed_" + control],
                stored["confidence"],
            )
            if any(
                abs(measured[key] - stored[key]) > 1e-12
                for key in ("mean", "mcse", "lower", "upper")
            ):
                raise ValueError("Summary differs: " + name + " " + control)
        transfer = (
            raw["matched_observed_transfer_primary_gamma"]
            - raw["matched_observed_gamma0"]
        )
        transfer_true = (
            raw["matched_true_transfer_primary_gamma"] - raw["matched_true_gamma0"]
        )
        audit["transfer_primary_gamma"][name] = {
            "independent": summary(transfer),
            "true": summary(transfer_true),
        }
        audit["peer_raw_contrasts"][name] = {}
        for peer in [
            "sgd",
            "adamw_step1",
            "ideal_polar",
            "finite_ns5_float64",
            "hard_spectral",
            "soft_spectral",
            "ht_svd",
        ]:
            audit["peer_raw_contrasts"][name][peer] = summary(
                raw["observed_rasp"] - raw["observed_" + peer]
            )
        difference = result["contrasts"]["gamma0"]["independent"]
        cost = result["cost"]
        rows.append(
            {
                "regime": name,
                "gamma": result["gamma"],
                "matched_difference": difference["mean"],
                "mcse": difference["mcse"],
                "lower": difference["lower"],
                "upper": difference["upper"],
                "confidence": difference["confidence"],
                "mean_svds": cost["mean_svds"],
                "p95_svds": cost["p95_svds"],
                "inactive_fraction": cost["inactive_fraction"],
            }
        )
    with (HERE / "phase02-summary.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (HERE / "raw-audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    labels = [row["regime"].replace("_", " ") for row in rows]
    y = np.arange(len(rows))
    values = np.array([row["matched_difference"] for row in rows])
    errors = np.array(
        [
            [row["matched_difference"] - row["lower"] for row in rows],
            [row["upper"] - row["matched_difference"] for row in rows],
        ]
    )
    fig, axes = plt.subplots(
        1, 2, figsize=(11.5, 6.8), gridspec_kw={"width_ratios": [2.2, 1]}, sharey=True
    )
    axes[0].errorbar(values, y, xerr=errors, fmt="o", color="#146b81", capsize=3)
    axes[0].axvline(0, color="gray", linewidth=0.8)
    axes[0].axvline(
        0.01, color="#a25919", linestyle="--", linewidth=0.8, label="primary threshold"
    )
    axes[0].set_yticks(y, labels)
    axes[0].invert_yaxis()
    axes[0].set_xlabel(
        "Extra independently observed loss decrease vs γ=0\nEqual direction norm, same step size 0.3"
    )
    axes[0].legend(loc="lower right", fontsize=8)
    axes[0].grid(axis="x", alpha=0.15)
    axes[1].plot(
        [row["mean_svds"] for row in rows], y, "o", color="#922f3c", label="mean"
    )
    axes[1].plot(
        [row["p95_svds"] for row in rows],
        y,
        "s",
        color="#c48852",
        label="95th percentile",
    )
    axes[1].set_xscale("log")
    axes[1].set_xlabel(
        "SVD count in reference solver\nIncludes feasibility and VI checks"
    )
    axes[1].legend(loc="lower right", fontsize=8)
    axes[1].grid(axis="x", alpha=0.15)
    fig.suptitle(
        "RASP controlled quadratic study · 8,192 contexts per regime", fontsize=13
    )
    fig.text(
        0.02,
        0.015,
        "Primary interval: Bonferroni adjusted; secondary intervals: descriptive 95%. CPU reference costs, no TPU timing.",
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.045, 1, 0.96))
    fig.savefig(HERE / "phase02-results.svg")
    svg = HERE / "phase02-results.svg"
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n"
    )
    fig.savefig(HERE / "phase02-results.png", dpi=180)
    print("Raw hashes and paired summaries verified:", audit["raw_bytes"], "bytes")


if __name__ == "__main__":
    main()
