"""CRESO float64 matrix reference; no accelerator or training timing claims."""

import numpy as np


def inner(a, b):
    return np.sum(a * b, axis=(-2, -1))


def norm(a):
    return np.sqrt(np.maximum(inner(a, a), 0))


def spectral(a):
    return np.linalg.svd(a, compute_uv=False)[..., 0]


def radial(a, radius):
    """One SVD gives radial feasibility without changing the vectorized span."""
    bound = spectral(a)
    factor = np.minimum(1.0, radius / np.maximum(bound, 1e-300))
    return factor[..., None, None] * a


def project(a, radius):
    u, s, vt = np.linalg.svd(a, full_matrices=False)
    return (u * np.minimum(s, radius)[..., None, :]) @ vt


def polar(a, radius):
    u, s, vt = np.linalg.svd(a, full_matrices=False)
    keep = s > 1e-12 * np.maximum(s[..., :1], 1e-30)
    return radius * (u * keep[..., None, :]) @ vt


def ns5(a, radius):
    """Published Muon quintic in float64, with explicit radial repair."""
    transpose = a.shape[-2] > a.shape[-1]
    x = np.swapaxes(a, -2, -1).copy() if transpose else a.copy()
    x /= norm(x)[..., None, None] + 1e-7
    for _ in range(5):
        gram = x @ np.swapaxes(x, -2, -1)
        x = 3.4445 * x + (-4.775 * gram + 2.0315 * gram @ gram) @ x
    x = np.swapaxes(x, -2, -1) if transpose else x
    return radial(radius * x, radius)


def progress(d, g, mu=1.0):
    return inner(g, d) - mu * inner(d, d) / 2


def noise_basis(differences, rank):
    flat = differences.reshape(*differences.shape[:2], -1)
    _, s, vt = np.linalg.svd(flat, full_matrices=False)
    count = min(rank, vt.shape[1])
    basis = vt[:, :count].copy()
    valid = s[:, :count] > 1e-10 * np.maximum(s[:, :1], 1e-30)
    return basis * valid[..., None]


def projected(a, basis):
    flat = a.reshape(a.shape[0], -1)
    coefficients = np.einsum("bkd,bd->bk", basis, flat)
    return np.einsum("bk,bkd->bd", coefficients, basis).reshape(a.shape)


def candidates(pilot, rank, radius, mu):
    if pilot.ndim != 4 or pilot.shape[1] % 2:
        raise ValueError("Expected an even number of proposal replicas")
    mean = pilot.mean(axis=1)
    differences = (pilot[:, ::2] - pilot[:, 1::2]) / np.sqrt(2)
    basis = noise_basis(differences, rank)
    denoised = mean - projected(mean, basis)
    points = np.stack(
        [
            np.zeros_like(mean),
            radial(mean / mu, radius),
            polar(mean, radius),
            radial(denoised / mu, radius),
        ],
        axis=1,
    )
    return points, basis


def allowances(points, basis, calibration, validation_count, delta, kurtosis):
    """Finite-moment Chebyshev bounds; kurtosis bounds Var(||P E||²)/trace².

    Fresh calibration differences E=(A-B)/sqrt(2) have the covariance
    of one replica. For Gaussian replicas, kurtosis=2 is a valid worst case.
    Both trace estimates use the same calibration set and a union bound.
    The validation mean may include calibration pair sums: a union of failures
    against true, proposal-conditional moments does not require independence
    between the estimated envelope and this mean. Proposal directions are frozen.
    """
    ncal = calibration.shape[1]
    fraction = np.sqrt(4 * kurtosis / (ncal * delta))
    if not (0 < delta < 1 and fraction < 1 and validation_count > 0):
        raise ValueError("Calibration count cannot certify this confidence")
    flat = calibration.reshape(calibration.shape[0], ncal, -1)
    coordinates = np.einsum("bkd,bnd->bnk", basis, flat)
    in_span = np.einsum("bnk,bkd->bnd", coordinates, basis)
    q_span = np.mean(np.sum(in_span**2, axis=-1), axis=1)
    q_rest = np.mean(np.sum((flat - in_span) ** 2, axis=-1), axis=1)
    upper_span = q_span / (1 - fraction)
    upper_rest = q_rest / (1 - fraction)
    point_flat = points.reshape(points.shape[0], points.shape[1], -1)
    point_coordinates = np.einsum("bkd,bjd->bjk", basis, point_flat)
    point_span = np.einsum("bjk,bkd->bjd", point_coordinates, basis)
    variance_upper = 2 * (
        upper_span[:, None] * np.sum(point_span**2, axis=-1)
        + upper_rest[:, None] * np.sum((point_flat - point_span) ** 2, axis=-1)
    )
    allowance = np.sqrt(
        np.maximum(variance_upper, 0)
        * points.shape[1]
        / (validation_count * (delta / 2))
    )
    return allowance, {
        "upper_span": upper_span,
        "upper_rest": upper_rest,
        "q_span": q_span,
        "q_rest": q_rest,
        "variance_upper": variance_upper,
        "calibration_fraction": fraction,
    }


def interpolate(points, validation_mean, bound, mu=1.0):
    """Exhaustive finite pair search; each scalar quadratic is solved exactly."""
    if mu <= 0 or np.any(bound < 0):
        raise ValueError("Expected positive curvature and nonnegative allowances")
    size, count = points.shape[:2]
    best_score = np.full(size, -np.inf)
    direction = np.zeros_like(points[:, 0])
    selected = np.zeros((size, 2), dtype=int)
    fraction = np.zeros(size)
    uncertainty = np.zeros(size)
    for i in range(count):
        for j in range(i, count):
            a, b = points[:, i], points[:, j]
            difference = b - a
            curvature = mu * inner(difference, difference)
            linear = inner(validation_mean - mu * a, difference) - (
                bound[:, j] - bound[:, i]
            )
            alpha = np.where(
                curvature > 1e-24,
                np.clip(linear / np.maximum(curvature, 1e-300), 0, 1),
                (linear > 0).astype(float),
            )
            d = a + alpha[:, None, None] * difference
            penalty = (1 - alpha) * bound[:, i] + alpha * bound[:, j]
            score = progress(d, validation_mean, mu) - penalty
            update = score > best_score + 1e-14
            direction[update] = d[update]
            selected[update] = (i, j)
            fraction[update] = alpha[update]
            uncertainty[update] = penalty[update]
            best_score[update] = score[update]
    return {
        "direction": direction,
        "certificate": best_score,
        "selected": selected,
        "fraction": fraction,
        "selected_allowance": uncertainty,
    }


def solve(
    pilot,
    calibration,
    validation_mean,
    validation_count,
    rank=1,
    radius=0.5,
    mu=1.0,
    delta=0.05,
    kurtosis=2.0,
):
    if mu <= 0 or radius < 0:
        raise ValueError("Invalid spectral problem")
    arrays = (pilot, calibration, validation_mean)
    if any(not np.isfinite(a).all() for a in arrays):
        raise ValueError("Nonfinite replica")
    points, basis = candidates(pilot, rank, radius, mu)
    bounds, diagnostic = allowances(
        points, basis, calibration, validation_count, delta, kurtosis
    )
    output = interpolate(points, validation_mean, bounds, mu)
    output.update(points=points, basis=basis, allowances=bounds, **diagnostic)
    return output
