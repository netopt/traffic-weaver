import numpy as np
import pytest
from numpy.ma.testutils import assert_array_approx_equal

from traffic_weaver import (
    PiecewiseConstantOversample,
    CubicSplineOversample,
    LinearFixedOversample,
    LinearAdaptiveOversample,
    ExpFixedOversample,
    ExpAdaptiveOversample,
)


@pytest.fixture
def xy():
    return np.arange(4), np.array([1, 3, 4, 1])


def test_piecewise_constant_oversample(xy):
    ov_x, ov_y = PiecewiseConstantOversample(xy[0], xy[1], 4).oversample()
    expected = np.array([1, 1, 1, 1, 3, 3, 3, 3, 4, 4, 4, 4, 1], dtype=np.float64)
    assert_array_approx_equal(ov_y, expected)


def test_cubic_spline__oversample(xy):
    ov_x, ov_y = CubicSplineOversample(xy[0], xy[1], 4).oversample()
    # check every forth if in place
    ov_y = ov_y[::4]
    expected = np.array([1, 3, 4, 1], dtype=np.float64)
    assert_array_approx_equal(ov_y, expected)


def test_linear_fixed_oversample(xy):
    ov_x, ov_y = LinearFixedOversample(xy[0], xy[1], 4).oversample()
    expected = np.array(
        [1, 1, 1, 1.5, 2, 2.5, 3, 3.25, 3.5, 3.75, 4, 3.25, 2.5], dtype=np.float64
    )
    assert_array_approx_equal(ov_y, expected)


def test_linear_adaptive_oversample(xy):
    ov_x, ov_y = LinearAdaptiveOversample(xy[0], xy[1], 4).oversample()
    expected = np.array(
        [1, 1, 1, 1.66, 2.33, 3, 3, 3.2, 3.4, 3.6, 3.8, 4, 2.5], dtype=np.float64
    )
    assert_array_approx_equal(ov_y, expected, decimal=2)


def test_exp_fixed_oversample(xy):
    ov_x, ov_y = ExpFixedOversample(xy[0], xy[1], 8).oversample()
    expected = np.array(
        [1, 1, 1, 1, 1, 1.187, 1.5, 1.75]
        + [2.0, 2.25, 2.5, 2.812, 3, 3.093, 3.25, 3.375]
        + [3.5, 3.625, 3.75, 3.906, 4.0, 3.718, 3.25, 2.875, 1.0],
        dtype=np.float64,
    )
    assert_array_approx_equal(ov_y, expected, decimal=2)


def test_exp_adaptive_oversample(xy):
    ov_x, ov_y = ExpAdaptiveOversample(xy[0], xy[1], 8).oversample()
    print(ov_y)
    expected = np.array(
        [1, 1, 1, 1, 1, 1.25, 1.666, 2]
        + [2.333, 2.666, 3.0, 3.0, 3.050, 3.161, 3.272, 3.363]
        + [3.454, 3.545, 3.636, 3.727, 3.838, 3.949, 4, 3, 1.0],
        dtype=np.float64,
    )
    assert_array_approx_equal(ov_y, expected, decimal=2)


def test_fail_too_small_oversample(xy):
    with pytest.raises(ValueError):
        LinearFixedOversample(xy[0], xy[1], 1)


def test_setting_parameters(xy):
    ov = LinearFixedOversample(xy[0], xy[1], 12, alpha=0.0)
    assert ov.a == 2
    ov = LinearAdaptiveOversample(xy[0], xy[1], 12, alpha=0.0)
    assert ov.a == 2
    ov = ExpFixedOversample(xy[0], xy[1], 12, alpha=0.0)
    assert ov.a == 2
    ov = ExpAdaptiveOversample(xy[0], xy[1], 12, alpha=0.0)
    assert ov.a == 2


def test_special_cases_in_oversample():
    # test 0 nominators and denominators
    x, y = np.arange(5), np.array([1, 1, 1, 3, 3])
    LinearAdaptiveOversample(x, y, 4).oversample()
    ExpAdaptiveOversample(x, y, 4, beta=0).oversample()
    assert True
