"""Exploratory published NS5 map without radial repair, using held-out tuning.

The fixed main study remains unchanged. This supplemental local map replaces
source bf16 with float64 and has no source-parity or trajectory claim.
"""

import json
import pathlib

import numpy as np
from numerics import progress, spectral
from study import PROTOCOL, summary

HERE = pathlib.Path(__file__).resolve().parent


def source_map(mean, index):
    momentum = [0.0, 0.5, 0.8, 0.9, 0.95, 0.99][index // 4]
    scale = PROTOCOL["scale_grid"][index % 4]
    x = ((1 - momentum) * (1 + momentum) * mean).copy()
    transpose = x.shape[-2] > x.shape[-1]
    if transpose:
        x = x.swapaxes(-1, -2)
    x /= np.sqrt(np.sum(x**2, axis=(-2, -1)))[..., None, None] + 1e-7
    for _ in range(5):
        gram = x @ x.swapaxes(-1, -2)
        x = 3.4445 * x + (-4.775 * gram + 2.0315 * gram @ gram) @ x
    if transpose:
        x = x.swapaxes(-1, -2)
    shape_scale = np.sqrt(max(1, mean.shape[-2] / mean.shape[-1]))
    return 0.5 * scale * shape_scale * x


if __name__ == "__main__":
    report, raw = {}, {}
    for law in [cfg["id"] for cfg in PROTOCOL["regimes"]]:
        with np.load(HERE / "run-v1" / f"development-{law}.npz") as dev:
            mean = dev["replicas"].mean(axis=1)
            development = [
                float(progress(source_map(mean, index), dev["g"]).mean())
                for index in range(24)
            ]
        index = int(np.argmax(development))
        effects, outputs, operators = [], [], []
        for path in sorted((HERE / "run-v1" / "final").glob(law + "-*.npz")):
            with np.load(path) as batch:
                d = source_map(batch["replicas"].mean(axis=1), index)
                value = progress(d, batch["g"])
                effects.append(batch["creso_progress"] - value)
                outputs.append(value)
                operators.append(spectral(d))
        effects, outputs, operators = map(np.concatenate, [effects, outputs, operators])
        raw[law + "_effect"] = effects
        raw[law + "_source_progress"] = outputs
        raw[law + "_operator_norm"] = operators
        report[law] = {
            "configuration_selected_on_development": index,
            "development_scores": development,
            "source_progress": summary(outputs),
            "creso_minus_source": summary(effects),
            "operator_radius_exceedance_fraction": float(
                np.mean(operators > 0.5 + 1e-10)
            ),
        }
        print(law, report[law]["creso_minus_source"]["mean"], flush=True)
    np.savez_compressed(HERE / "source-muon-raw.npz", **raw)
    (HERE / "source-muon-check.json").write_text(
        json.dumps(
            {
                "scope": "Exploratory zero-state NS5 map: published coefficients, orientation, EMA/Nesterov and shape scaling; float64 replaces bf16; no radial repair.",
                "primary_source": "https://github.com/KellerJordan/Muon/tree/f98f1cacc0263b04290753e32be8d498c1efc806",
                "tuning": "24 configurations on independent development contexts; no final selection; intervals are descriptive, not an added primary family.",
                "laws": report,
            },
            indent=2,
        )
        + "\n"
    )
