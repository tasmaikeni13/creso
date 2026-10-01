"""Check the exploratory cost repair independently of the frozen simulation."""

import numpy as np
from phase02.numerics import dense_solve, objective
from solver_attack import brent_solve


def test_interpolated_root_against_independent_conic_solver():
    rng = np.random.default_rng(20261005)
    m = rng.normal(size=(6, 3, 5)) * 3
    e = rng.normal(size=m.shape)
    for gamma in (0.0, 1.0, 1000.0):
        d, work, gap = brent_solve(m, e, gamma)
        assert (work >= 3).all()
        assert gap.max() < 1e-7
        for i in range(len(m)):
            independent, _ = dense_solve(m[i], e[i], gamma=gamma)
            assert (
                abs(
                    objective(d[i], m[i], e[i], gamma=gamma)
                    - objective(independent, m[i], e[i], gamma=gamma)
                )
                < 1e-7
            )


def test_anticorrelated_replica_counterexample():
    g, e = np.diag([0.6, 0.8]), np.diag([1.0, 0.0])
    actual, _, gap = brent_solve(g[None], e[None], gamma=3)
    np.testing.assert_allclose(actual[0], np.diag([0.15, 0.8]), atol=1e-12)
    assert gap[0] < 1e-10
