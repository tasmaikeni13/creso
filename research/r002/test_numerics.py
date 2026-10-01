"""Independent tests for actual matrix feasibility, selection and calibration."""

import numpy as np
import pytest
from numerics import (
    allowances,
    candidates,
    inner,
    interpolate,
    progress,
    radial,
    solve,
    spectral,
)
from scipy.optimize import minimize_scalar


@pytest.mark.parametrize("shape", [(2, 2), (2, 5), (5, 2), (4, 4)])
def test_radial_actual_operator_ball(shape):
    rng = np.random.default_rng(20261012)
    matrix = rng.normal(size=(20, *shape))
    repaired = radial(matrix, 0.4)
    assert np.max(spectral(repaired)) <= 0.4 + 1e-12
    assert np.array_equal(radial(matrix, 0), np.zeros_like(matrix))


def test_scalar_segments_against_independent_optimizer():
    rng = np.random.default_rng(20261013)
    points = radial(rng.normal(size=(64, 4, 3, 2)), 0.5)
    mean = rng.normal(size=(64, 3, 2))
    bounds = rng.uniform(size=(64, 4))
    result = interpolate(points, mean, bounds)
    for row in range(64):
        best = -np.inf
        for i in range(4):
            for j in range(i, 4):

                def objective(alpha, row=row, i=i, j=j):
                    d = (1 - alpha) * points[row, i] + alpha * points[row, j]
                    return -float(
                        progress(d, mean[row])
                        - ((1 - alpha) * bounds[row, i] + alpha * bounds[row, j])
                    )

                numerical = minimize_scalar(
                    objective,
                    bounds=(0, 1),
                    method="bounded",
                    options={"xatol": 1e-13},
                )
                best = max(best, -numerical.fun, -objective(0), -objective(1))
        assert abs(result["certificate"][row] - best) < 1e-9
    assert np.max(spectral(result["direction"])) <= 0.5 + 1e-12


def test_uniform_certificate_survives_adaptive_selection():
    rng = np.random.default_rng(20261014)
    points = radial(rng.normal(size=(100, 4, 3, 3)), 0.5)
    g, error = rng.normal(size=(2, 100, 3, 3))
    bounds = np.abs(inner(points, error[:, None]))
    result = interpolate(points, g + error, bounds)
    true = progress(result["direction"], g)
    assert np.min(true - result["certificate"]) > -1e-12
    vertex_true = progress(points, g[:, None])
    assert np.min(true[:, None] - (vertex_true - 2 * bounds)) > -1e-12


def test_degenerate_identical_points_and_zero_curvature():
    points = np.zeros((5, 4, 2, 2))
    result = interpolate(points, np.ones((5, 2, 2)), np.zeros((5, 4)))
    assert np.array_equal(result["direction"], points[:, 0])
    assert np.array_equal(result["selected"], np.zeros((5, 2), dtype=int))


def test_deflation_and_active_rank_one_witness():
    rng = np.random.default_rng(20261015)
    g = np.zeros((64, 2, 2))
    g[:, 0, 0] = 1
    noise = np.zeros_like(g)
    noise[:, 1, 1] = 1
    pilot = g[:, None] + 20 * rng.normal(size=(64, 8, 1, 1)) * noise[:, None]
    calibration = 20 * rng.normal(size=(64, 256, 1, 1)) * noise[:, None]
    validation = g + rng.normal(size=(64, 1, 1)) * noise
    result = solve(pilot, calibration, validation, 128)
    expected = np.zeros_like(g)
    expected[:, 0, 0] = 0.5
    assert np.max(np.abs(result["direction"] - expected)) < 1e-12
    assert np.max(np.abs(progress(expected, g) - 0.375)) < 1e-12
    assert np.max(np.abs(spectral(expected) - 0.5)) < 1e-12


def test_basis_orthogonality_and_projection():
    rng = np.random.default_rng(20261016)
    pilot = rng.normal(size=(10, 8, 4, 3))
    points, basis = candidates(pilot, 3, 0.5, 1)
    gram = basis @ basis.swapaxes(-1, -2)
    assert np.max(np.abs(gram - np.eye(3))) < 1e-12
    flattened = points[:, 3].reshape(10, -1)
    assert np.max(np.abs(np.einsum("bkd,bd->bk", basis, flattened))) < 1e-12


def test_trace_zero_and_calibration_guard():
    points = np.zeros((2, 4, 2, 2))
    basis = np.zeros((2, 1, 4))
    bound, _ = allowances(points, basis, np.zeros((2, 256, 2, 2)), 128, 0.05, 2)
    assert np.array_equal(bound, np.zeros((2, 4)))
    with pytest.raises(ValueError):
        allowances(points, basis, np.zeros((2, 16, 2, 2)), 128, 0.05, 2)


def test_nonfinite_input_rejected():
    pilot = np.zeros((2, 8, 2, 2))
    pilot[0, 0, 0, 0] = np.nan
    with pytest.raises(ValueError):
        solve(pilot, np.zeros((2, 256, 2, 2)), np.zeros((2, 2, 2)), 128)
