"""Separate checks of the confidence assumptions and standalone comparator."""

import numpy as np
from numerics import interpolate, progress, solve, spectral
from proximal import solve as proximal_solve
from source_muon_check import source_map


def test_common_noise_cannot_be_certified_by_differences():
    common = np.diag([1.0, 0.0])[None]
    result = solve(
        np.repeat(common[:, None], 8, axis=1), np.zeros((1, 256, 2, 2)), common, 640
    )
    assert result["certificate"][0] == 0.375
    assert progress(result["direction"], np.zeros_like(common))[0] == -0.125


def test_interpolation_improves_an_active_matrix_library():
    points = np.array(
        [
            [
                np.zeros((2, 2)),
                np.diag([0.5, 0.5]),
                np.diag([0.5, -0.5]),
                np.zeros((2, 2)),
            ]
        ]
    )
    g = np.diag([1.0, 0.0])[None]
    result = interpolate(points, g, np.zeros((1, 4)))
    assert result["fraction"][0] == 0.5
    assert spectral(result["direction"])[0] == 0.5
    assert (
        progress(result["direction"], g)[0] - np.max(progress(points, g[:, None]))
        == 0.125
    )


def test_standalone_proximal_against_conic_solver():
    import cvxpy as cp

    rng = np.random.default_rng(20261027)
    for rows, cols in [(2, 2), (2, 3), (3, 2)]:
        for _ in range(4):
            mean, noise = rng.normal(size=(2, rows, cols))
            exact = proximal_solve(mean, noise, radius=0.5)["direction"]
            d = cp.Variable((rows, cols))
            block = cp.bmat([[0.5 * np.eye(rows), d], [d.T, 0.5 * np.eye(cols)]])
            objective = (
                0.5 * cp.sum_squares(d)
                + 0.5 * cp.square(cp.sum(cp.multiply(noise, d)))
                - cp.sum(cp.multiply(mean, d))
            )
            problem = cp.Problem(cp.Minimize(objective), [block >> 0])
            problem.solve(
                solver="CLARABEL", tol_gap_abs=1e-10, tol_feas=1e-10, tol_gap_rel=1e-10
            )
            assert np.max(np.abs(exact - d.value)) < 2e-5


def test_unrepaired_source_ns5_against_scalar_polynomial():
    mean = np.diag([1.0, 0.3])[None]
    momentum = 0.95
    values = (1 - momentum) * (1 + momentum) * np.array([1.0, 0.3])
    values /= np.linalg.norm(values) + 1e-7
    for _ in range(5):
        values = 3.4445 * values - 4.775 * values**3 + 2.0315 * values**5
    expected = np.diag(0.5 * values)
    # Index 4*4+2 selects momentum .95 and learning-rate multiplier 1.
    assert np.max(np.abs(source_map(mean, 18)[0] - expected)) < 1e-12
