"""Declared synthetic laws; hidden population quantities are evaluator-only."""

import numpy as np


def make_case(rng, config, size, replicas=648, assessment=256):
    rows, cols = config["shape"]
    g = np.zeros((size, rows, cols))
    vectors = np.zeros((size, 2, rows, cols))
    sigma = np.zeros((size, 2))
    g[:, 0, 0] = 1
    vectors[:, 0, 1, 1] = 1
    sigma[:, 0] = config.get("sigma", 20.0)
    kind = config["kind"]
    isotropic = config.get("isotropic", 0.0)
    latent = np.zeros(size, dtype=int)
    if kind == "rank2":
        g[:, 1, 1] = 0.5
        vectors[:] = 0
        vectors[:, 0, 2, 2] = 1
        vectors[:, 1, 3, 3] = 1
        sigma[:] = config["sigma"]
    elif kind == "mixed":
        latent = (rng.random(size) < 0.5).astype(int)
        g[:, 1, 1] = 0.8 * latent
        sigma[:, 0] = np.where(latent, 0.03, 20.0)
    elif kind == "overlap":
        g[:, 1, 1] = 0.8
    elif kind == "zero_signal":
        g[:] = 0
    if config.get("rotate"):
        # Fixed orientation is part of the law, rather than fitted from outcomes.
        orientation = np.random.default_rng(config["rotation_seed"])
        left = np.linalg.qr(orientation.normal(size=(rows, rows)))[0]
        right = np.linalg.qr(orientation.normal(size=(cols, cols)))[0]
        g = left @ g @ right.T
        vectors = left @ vectors @ right.T

    def draws(count, correlated=False):
        if kind == "heavy_tail":
            z = rng.standard_t(3, size=(size, count, 2)) / np.sqrt(3)
        else:
            z = rng.normal(size=(size, count, 2))
        if correlated:
            rho = config["correlation"]
            common = rng.normal(size=(size, 1, 2))
            z = np.sqrt(1 - rho) * z + np.sqrt(rho) * common
        noise = np.einsum("bnk,bk,bkij->bnij", z, sigma, vectors)
        if isotropic:
            noise += isotropic * rng.normal(size=noise.shape)
        return g[:, None] + noise

    observed = draws(replicas, correlated=kind == "dependent")
    evaluation = draws(assessment).mean(axis=1)
    return {
        "replicas": observed,
        "g": g,
        "vectors": vectors,
        "sigma": sigma,
        "isotropic": np.full(size, isotropic),
        "evaluation_mean": evaluation,
        "latent": latent,
    }


def split(case):
    replicas = case["replicas"]
    pilot = replicas[:, :8]
    calibration = (replicas[:, 8:520:2] - replicas[:, 9:520:2]) / np.sqrt(2)
    # All 640 post-proposal replicas contribute to the validation mean.
    # Its correlation with the calibration statistic does not break a union bound.
    return pilot, calibration, replicas[:, 8:].mean(axis=1), replicas.mean(axis=1)
