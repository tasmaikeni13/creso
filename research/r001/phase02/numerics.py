"""Float64 research evaluator, independent of any future training implementation."""

import numpy as np


def inner(a, b):
    return np.sum(a * b, axis=(-2, -1))


def norm(a):
    return np.sqrt(inner(a, a))


def spectral(a):
    return np.linalg.svd(a, compute_uv=False)[..., 0]


def project(a, radius=1.0):
    u, s, vt = np.linalg.svd(a, full_matrices=False)
    return (u * np.minimum(s, radius)[..., None, :]) @ vt


def objective(d, m, e, mu=1.0, gamma=1.0):
    return mu * inner(d, d) / 2 + gamma * inner(e, d) ** 2 / 2 - inner(m, d)


def certificate(d, m, e, mu=1.0, gamma=1.0, radius=1.0):
    """Numerical VI gap via spectral-ball support; not interval arithmetic."""
    residual = mu * d + gamma * inner(e, d)[..., None, None] * e - m
    nuclear = np.linalg.svd(residual, compute_uv=False).sum(axis=-1)
    gap = inner(residual, d) + radius * nuclear
    return {"vi_gap": gap, "operator_norm": spectral(d), "residual": residual}


def inverse_then_project(m, e, mu=1.0, gamma=1.0, radius=1.0):
    z = gamma * inner(e, m) / (mu + gamma * inner(e, e))
    return project((m - z[..., None, None] * e) / mu, radius)


def solve(m, e, mu=1.0, gamma=1.0, radius=1.0, tolerance=1e-9, max_iterations=90):
    """Sherman-Morrison inactive case; otherwise exact-SVD scalar bisection.

    Stopping uses both the exact-projection residual bound and the computed VI.
    Float64 SVD roundoff is checked empirically, not formally certified here.
    Count the feasibility SVD and final certificate SVDs, even on fast paths.
    """
    if not (mu > 0 and gamma >= 0 and radius >= 0 and tolerance > 0):
        raise ValueError("Invalid convex problem or tolerance")
    m, e = np.asarray(m, dtype=float), np.asarray(e, dtype=float)
    single = m.ndim == 2
    if m.shape != e.shape or m.ndim not in (2, 3):
        raise ValueError("Expected equal rectangular matrices or matrix batches")
    if not (np.isfinite(m).all() and np.isfinite(e).all()):
        raise ValueError("Nonfinite inputs")
    if single:
        m, e = m[None], e[None]
    n = len(m)
    work = np.zeros(n, dtype=int)
    iterations = np.zeros(n, dtype=int)
    z = gamma * inner(e, m) / (mu + gamma * inner(e, e))
    d = (m - z[:, None, None] * e) / mu
    inactive = spectral(d) <= radius
    work += 1
    if radius == 0:
        d[:] = 0
        inactive[:] = True
    ids = np.flatnonzero(~inactive)
    if len(ids):
        p0 = project(m[ids] / mu, radius)
        f0 = -gamma * inner(e[ids], p0)
        work[ids] += 1
        bound = np.abs(f0)
        lo, hi = -bound, bound
        for _ in range(max_iterations):
            mid = (lo + hi) / 2
            point = project((m[ids] - mid[:, None, None] * e[ids]) / mu, radius)
            feedback = mid - gamma * inner(e[ids], point)
            d[ids], z[ids] = point, mid
            work[ids] += 1
            iterations[ids] += 1
            error = np.abs(feedback) * norm(e[ids]) / mu
            stop = error <= tolerance
            if stop.any():
                # VI requires another SVD; this independent stopping diagnostic
                # catches inaccurate projections and sign/scale mistakes.
                check = certificate(
                    point[stop], m[ids[stop]], e[ids[stop]], mu, gamma, radius
                )
                work[ids[stop]] += 2
                stop[stop] = check["vi_gap"] <= tolerance * (
                    1 + norm(m[ids[stop]]) * radius
                )
            if stop.all():
                break
            lo = np.where(feedback < 0, mid, lo)[~stop]
            hi = np.where(feedback >= 0, mid, hi)[~stop]
            ids = ids[~stop]
        else:
            raise RuntimeError("Root solver did not meet the fixed certificate")
    check = certificate(d, m, e, mu, gamma, radius)
    work += 2
    scale = 1 + norm(m) * radius
    if np.any(check["vi_gap"] > 5 * tolerance * scale):
        raise RuntimeError("Final VI certificate failed")
    if np.any(check["operator_norm"] > radius + 5e-12 * (1 + radius)):
        raise RuntimeError("Final feasibility failed")
    output = {
        "direction": d,
        "z": z,
        "svds": work,
        "iterations": iterations,
        "inactive": inactive,
        "vi_gap": check["vi_gap"],
        "operator_norm": check["operator_norm"],
    }
    return {key: value[0] for key, value in output.items()} if single else output


def dense_solve(m, e, mu=1.0, gamma=1.0, radius=1.0):
    """Independent conic optimizer: actual operator ball as a block PSD LMI."""
    import cvxpy as cp

    rows, cols = m.shape
    d = cp.Variable(m.shape)
    block = cp.bmat([[radius * np.eye(rows), d], [d.T, radius * np.eye(cols)]])
    risk = cp.sum(cp.multiply(e, d))
    cost = mu * cp.sum_squares(d) / 2 + gamma * cp.square(risk) / 2
    problem = cp.Problem(cp.Minimize(cost - cp.sum(cp.multiply(m, d))), [block >> 0])
    problem.solve(
        solver="CLARABEL",
        tol_gap_abs=1e-10,
        tol_gap_rel=1e-10,
        tol_feas=1e-10,
        max_iter=300,
    )
    if problem.status not in ("optimal", "optimal_inaccurate"):
        raise RuntimeError(problem.status)
    return d.value, problem.status


def matched(d):
    """Unit Frobenius directions remain in the radius-one operator ball."""
    return d / np.maximum(norm(d)[..., None, None], 1e-30)


def polar(a):
    u, s, vt = np.linalg.svd(a, full_matrices=False)
    active = s > 1e-12 * np.maximum(s[..., :1], 1e-30)
    return (u * active[..., None, :]) @ vt


def ns5(a):
    """Source polynomial in float64; deliberately not a bf16 parity claim."""
    transpose = a.shape[-2] > a.shape[-1]
    x = np.swapaxes(a, -2, -1) if transpose else a.copy()
    x /= norm(x)[..., None, None] + 1e-7
    for _ in range(5):
        gram = x @ np.swapaxes(x, -2, -1)
        x = 3.4445 * x + (-4.775 * gram + 2.0315 * gram @ gram) @ x
    return np.swapaxes(x, -2, -1) if transpose else x


def soft_clip(a, threshold):
    u, s, vt = np.linalg.svd(a, full_matrices=False)
    values = threshold * s / np.sqrt(threshold**2 + s**2)
    return (u * values[..., None, :]) @ vt
