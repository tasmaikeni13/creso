"""Independent evaluators and counterexamples required by the phase gates."""

import itertools
from fractions import Fraction

import numpy as np
import pytest
from laws import make_case
from numerics import (
    certificate,
    dense_solve,
    inner,
    inverse_then_project,
    matched,
    norm,
    objective,
    polar,
    project,
    solve,
)


def test_analytic_matrix_counterexample():
    m, e = np.diag([3.0, 1.0]), np.eye(2)
    actual = solve(m, e)["direction"]
    wrong = inverse_then_project(m, e)
    np.testing.assert_allclose(actual, np.diag([1.0, 0.0]), atol=2e-9)
    np.testing.assert_allclose(wrong, np.diag([1.0, -1 / 3]), atol=1e-12)
    assert objective(wrong, m, e) - objective(actual, m, e) == pytest.approx(
        1 / 9, abs=1e-9
    )
    assert certificate(wrong, m, e)["vi_gap"] > 0.1


@pytest.mark.parametrize("shape", [(1, 7), (7, 1), (2, 2), (3, 5), (5, 3)])
@pytest.mark.parametrize("gamma", [0.0, 0.1, 10.0, 1000.0])
def test_independent_dense_constrained_optimizer(shape, gamma):
    rng = np.random.default_rng(20261005)
    m, e = rng.normal(size=shape) * 3, rng.normal(size=shape)
    result = solve(m, e, gamma=gamma)
    dense, status = dense_solve(m, e, gamma=gamma)
    assert status in ("optimal", "optimal_inaccurate")
    assert result["operator_norm"] <= 1 + 1e-11
    assert result["vi_gap"] < 1e-7
    np.testing.assert_allclose(result["direction"], dense, atol=3e-5, rtol=3e-5)
    assert (
        abs(
            objective(result["direction"], m, e, gamma=gamma)
            - objective(dense, m, e, gamma=gamma)
        )
        < 1e-7
    )


def test_zero_rank_and_singular_boundaries():
    for m in [np.zeros((3, 5)), np.eye(4), np.diag([4, 1e-14, 0, 0])]:
        e = np.zeros_like(m)
        np.testing.assert_allclose(solve(m, e)["direction"], project(m), atol=1e-12)
        np.testing.assert_array_equal(
            solve(m, np.ones_like(m), radius=0)["direction"], np.zeros_like(m)
        )
        for scale in (1e-10, 1e6):
            result = solve(scale * m, np.ones_like(m), gamma=0.1)
            assert result["operator_norm"] <= 1 + 1e-11
    assert norm(polar(np.zeros((3, 5)))) == 0
    assert np.linalg.matrix_rank(polar(np.diag([3, 0, 0]))) == 1


def test_swap_and_batch_and_realized_monotonicity():
    rng = np.random.default_rng(20261005)
    m, e = rng.normal(size=(40, 3, 5)), rng.normal(size=(40, 3, 5))
    previous = np.full(40, np.inf)
    for gamma in (0, 0.1, 1, 10, 1000):
        a, b = solve(m, e, gamma=gamma), solve(m, -e, gamma=gamma)
        np.testing.assert_allclose(a["direction"], b["direction"], atol=1e-10)
        risk = inner(e, a["direction"]) ** 2
        assert (risk <= previous + 1e-8).all()
        previous = risk
    np.testing.assert_allclose(
        solve(m[0], e[0], gamma=1000)["direction"], a["direction"][0], atol=1e-10
    )


def test_feasible_vi_gap_and_distance_certificate():
    m, e = np.diag([0.3, 0.2]), np.ones((2, 2))
    exact = solve(m, e)["direction"]
    computed = project(exact + np.diag([0.001, -0.002]))
    gap = certificate(computed, m, e)["vi_gap"]
    assert objective(computed, m, e) - objective(exact, m, e) <= gap + 1e-12
    assert norm(computed - exact) ** 2 <= gap + 1e-12
    residual = certificate(computed, m, e)["residual"]
    perturbation = np.full((2, 2), 1e-5)
    modified = residual + perturbation
    measured_gap = (
        inner(modified, computed) + np.linalg.svd(modified, compute_uv=False).sum()
    )
    diameter = 2 * np.sqrt(2)
    assert gap <= measured_gap + norm(perturbation) * diameter + 1e-12
    # A Frobenius upper bound is conservative but certifiable algebraically.
    bad = np.diag([2.0, 0.1])
    repaired = bad * min(1, 1 / norm(bad))
    assert np.linalg.svd(repaired, compute_uv=False)[0] <= 1


def test_exact_finite_population_and_adaptive_bias():
    values, weights = [Fraction(-2), Fraction(1)], [Fraction(1, 3), Fraction(2, 3)]
    disagreement = mean_error = Fraction(0)
    for i, j in itertools.product(range(2), repeat=2):
        p = weights[i] * weights[j]
        disagreement += p * ((values[i] - values[j]) / 2) ** 2
        mean_error += p * ((values[i] + values[j]) / 2) ** 2
    assert disagreement == mean_error == 1
    # Exact adaptive counterexample: g=0, half errors iid +/-1, gamma arbitrary.
    # E*D is always zero; a fresh mean error has variance 1/2 and E[D^2]=1/2.
    surrogate, direction_square = Fraction(0), Fraction(0)
    for a, b in itertools.product([Fraction(-1), Fraction(1)], repeat=2):
        mean, difference = (a + b) / 2, (a - b) / 2
        d = mean / (1 + difference**2)
        surrogate += (difference * d) ** 2 / 4
        direction_square += d**2 / 4
    assert surrogate == 0
    assert direction_square / 2 == Fraction(1, 4)


def test_momentum_noise_is_not_current_disagreement():
    rng = np.random.default_rng(20261005)
    n, beta, steps, sigma = 30000, 0.9, 32, 3.0
    m = np.zeros(n)
    for _ in range(steps):
        a, b = rng.normal(0, sigma, size=(2, n))
        m = beta * m + (1 - beta) * (a + b) / 2
    e = (a - b) / 2
    expected = sigma**2 / 2 * (1 - beta) / (1 + beta) * (1 - beta ** (2 * steps))
    assert m.var() == pytest.approx(expected, rel=0.06)
    assert e.var() == pytest.approx(sigma**2 / 2, rel=0.06)
    assert e.var() > 15 * m.var()


def test_correlated_unequal_and_normalization_laws():
    rng = np.random.default_rng(20261005)
    cfg = {"shape": [3, 5], "law": "normal", "sigma": 3, "correlation": 0.8}
    case = make_case(rng, cfg, 30000, donors=False)
    v = case["bases"][:, 0]
    assert np.mean(inner(case["e"], v) ** 2) == pytest.approx(0.9, rel=0.06)
    assert np.mean(inner(case["m"] - case["g"], v) ** 2) == pytest.approx(8.1, rel=0.06)
    normalized = matched(case["m"])
    np.testing.assert_allclose(norm(normalized), 1, atol=1e-12)
    assert np.linalg.svd(normalized, compute_uv=False)[:, 0].max() <= 1 + 1e-12


def test_invalid_parameters_and_nontermination():
    for kwargs in ({"mu": 0}, {"gamma": -1}, {"radius": -1}, {"tolerance": 0}):
        with pytest.raises(ValueError):
            solve(np.eye(2), np.eye(2), **kwargs)
    with pytest.raises(RuntimeError):
        solve(np.diag([3.0, 1.0]), np.eye(2), max_iterations=0)
