import numpy as np
import pytest
from numpy.ma.testutils import assert_array_equal, assert_array_almost_equal

from traffic_weaver.process import (
    repeat, trend, linear_trend, noise_gauss, average,
    _piecewise_constant_interpolate,
)


@pytest.fixture
def xy():
    return np.arange(5), np.array([1, 3, 4, 1, 2])


def test_repeat(xy):
    nx, ny = repeat(xy[0], xy[1], 3)
    assert_array_equal(ny, list(xy[1]) * 3)
    assert_array_equal(nx, np.arange(15))


def test_trend(xy):
    shift = [0, 1 / 16, 1 / 4, 9 / 16, 1]
    nx, ny = trend(xy[0], xy[1], lambda x: x ** 2)
    assert_array_equal(nx, xy[0])
    assert_array_equal(ny, xy[1] + shift)


def test_linear_trend(xy):
    shift = [0, 0.25, 0.5, 0.75, 1]
    nx, ny = linear_trend(xy[0], xy[1], 1)
    assert_array_equal(nx, xy[0])
    assert_array_equal(ny, xy[1] + shift)


@pytest.fixture
def mock_normal_generator(mocker):
    def dummy_random_generator(loc=0, scale=1, size=1):
        if np.isscalar(scale):
            if size == 1:
                return loc + scale
            else:
                return [loc + scale] * size[0]
        else:
            return np.asarray(scale) + loc

    mocker.patch(
        "numpy.random.normal",
        side_effect=lambda loc, scale, size: dummy_random_generator(
            loc=loc, scale=scale, size=size
        ),
    )
    return mocker


def test_noise(mock_normal_generator):
    y = [1, 1, 1, 1, 1]
    snr = [1, 2, 3, 4, 5]
    stds = np.asarray([0.89125094, 0.79432823, 0.70794578, 0.63095734, 0.56234133])

    ny = noise_gauss(y, snr)
    assert_array_almost_equal(ny, y + stds)

    snr_not_in_db = [1, 1, 1, 1, 1]
    ny = noise_gauss(y, snr_not_in_db, snr_not_in_db)
    assert_array_almost_equal(ny, [2] * 5)

    stds = np.asarray([1, 2, 3, 4, 5])
    ny = noise_gauss(y, std=stds)
    assert_array_almost_equal(ny, y + stds)


def test_average(xy):
    ax, ay = average(xy[0], xy[1], 2)
    expected_x = [0, 2, 4]
    expected_y = [2, 2.5, 2]
    assert_array_equal(ax, expected_x)
    assert_array_equal(ay, expected_y)


@pytest.mark.parametrize(
    "x, y, new_x, expected",
    [
        ([0, 1, 2], [2, 3, 4], [0.5, 1.0, 1.5, 2.0, 2.5], [2, 3, 3, 4, 4]),
        ([2, 3, 4], [5, 4, 3], [0, 1, 2, 5, 8], [5, 5, 5, 3, 3]),
    ],
)
def test_piecewise_constant_interpolate(x, y, new_x, expected):
    new_y = _piecewise_constant_interpolate(x, y, new_x)
    assert_array_equal(new_y, expected)
