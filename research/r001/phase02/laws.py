"""Known finite-variance attack laws and independent loss observations."""

import numpy as np
from numerics import inner, matched, norm


def scalar_noise(rng, shape, law):
    if law == "normal":
        return rng.normal(size=shape)
    if law == "student5":
        return rng.standard_t(5, size=shape) * np.sqrt(3 / 5)
    if law == "outlier":
        p = 0.04
        return (rng.binomial(1, p, size=shape) - p) / np.sqrt(p * (1 - p))
    raise ValueError(law)


def orthogonal_units(rng, g, rank):
    result = []
    for _ in range(rank):
        v = rng.normal(size=g.shape)
        v -= inner(v, g)[:, None, None] * g
        for old in result:
            v -= inner(v, old)[:, None, None] * old
        result.append(matched(v))
    return np.stack(result, axis=1)


def draw_errors(rng, case):
    cfg, bases, scales = case["config"], case["bases"], case["scales"]
    shape = scales.shape
    a = scalar_noise(rng, shape, cfg["law"])
    independent = scalar_noise(rng, shape, cfg["law"])
    rho = cfg.get("correlation", 0.0)
    b = rho * a + np.sqrt(1 - rho**2) * independent
    b *= cfg.get("half_b_scale", 1.0)
    noise_a = np.sum((scales * a)[..., None, None] * bases, axis=1)
    noise_b = np.sum((scales * b)[..., None, None] * bases, axis=1)
    noise_a += cfg.get("bias_a", 0.0) * case["g"]
    noise_b += cfg.get("bias_b", 0.0) * case["g"]
    return noise_a, noise_b


def make_case(rng, cfg, n, donors=True):
    rows, cols = cfg["shape"]
    g = np.zeros((n, rows, cols))
    for j in range(min(rows, cols)):
        value = 1.0
        if cfg.get("signal") == "rank_one" and j:
            value = 0.0
        if cfg.get("signal") == "near_singular" and j:
            value = 10.0 ** (-3 * (j + 1))
        g[:, j, j] = value
    g = matched(g)
    rank = cfg.get("rank", 1)
    bases = orthogonal_units(rng, g, rank)
    alignment = cfg.get("alignment", 0.0)
    bases[:, 0] = alignment * g + np.sqrt(1 - alignment**2) * bases[:, 0]
    relative = np.array(cfg.get("relative_scales", [1.0]))
    scales = np.broadcast_to(cfg["sigma"] * relative, (n, rank)).copy()
    case = {"g": g, "bases": bases, "scales": scales, "config": cfg}
    a, b = draw_errors(rng, case)
    case.update({"a": a, "b": b, "m": g + (a + b) / 2, "e": (a - b) / 2})
    beta = cfg.get("beta", 0.0)
    if beta:
        rotation = cfg["signal_rotation_radians"]
        old_g = np.cos(rotation) * g + np.sin(rotation) * bases[:, 0]
        momentum = np.zeros_like(g)
        for _ in range(cfg["history_steps"] - 1):
            previous_a, previous_b = draw_errors(rng, case)
            momentum = beta * momentum + (1 - beta) * (
                old_g + (previous_a + previous_b) / 2
            )
        case["m"] = beta * momentum + (1 - beta) * case["m"]
        case["momentum_signal"] = (
            beta * (1 - beta ** (cfg["history_steps"] - 1)) * old_g + (1 - beta) * g
        )
    if donors:
        donor = make_case(rng, cfg, n, donors=False)
        permutation = rng.permutation(n)
        case["shuffled"] = donor["e"][permutation]
        case["donor_permutation"] = permutation
        random_basis = orthogonal_units(rng, g, 1)[:, 0]
        random_basis = alignment * g + np.sqrt(1 - alignment**2) * random_basis
        case["random"] = norm(case["e"])[:, None, None] * random_basis
    return case


def independent_evaluation(rng, case):
    a, b = draw_errors(rng, case)
    # Bias is deliberately included in raw observations, then removed using
    # the known attack law. This supplies an unbiased loss oracle even when
    # training replicas are biased; it never enters optimizer selection.
    bias = (case["config"].get("bias_a", 0.0) + case["config"].get("bias_b", 0.0)) / 2
    return (a + b) / 2 - bias * case["g"]


def progress(direction, g, stepsize, evaluation_noise=None):
    gradient = g if evaluation_noise is None else g + evaluation_noise
    return (
        stepsize * inner(gradient, direction)
        - stepsize**2 * inner(direction, direction) / 2
    )
