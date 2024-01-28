import numpy as np
import pytest
from numpy.testing import assert_array_equal

from traffic_weaver import Weaver, PiecewiseConstantOversample


@pytest.fixture
def xy():
    return np.arange(5), np.array([1, 3, 4, 1, 2])


@pytest.fixture
def expected_xy():
    return np.arange(0, 4.5, 0.5), np.array([1, 1, 3, 3, 4, 4, 1, 1, 2])


@pytest.fixture
def mock_weaver_delegates(mocker, xy):
    mocker.patch(
        "traffic_weaver.weaver.integral_matching_reference_stretch",
        side_effect=lambda x, y, orig_x, orig_y: y,
    )

    mocker.patch(
        "traffic_weaver.weaver.repeat", side_effect=lambda x, y, repeats: (x, y)
    )
    mocker.patch(
        "traffic_weaver.weaver.spline_smooth",
        side_effect=lambda x, y, s: lambda xin: y
        if not np.isscalar(xin)
        else y[np.argmax(x == xin)],
    )
    mocker.patch("traffic_weaver.weaver.noise_gauss", side_effect=lambda y, snr: y)
    return mocker


def test_weaver_chain(mock_weaver_delegates, xy, expected_xy):
    weaver = Weaver(xy[0], xy[1])
    weaver.oversample(2, oversample_class=PiecewiseConstantOversample)
    weaver.integral_match()
    weaver.repeat(2)
    weaver.trend(lambda x: 0)
    weaver.smooth(0)
    weaver.noise(0)

    assert_array_equal(weaver.get_original()[0], xy[0])
    assert_array_equal(weaver.get_original()[1], xy[1])

    assert_array_equal(weaver.get()[0], expected_xy[0])
    assert_array_equal(weaver.get()[1], expected_xy[1])

    spline = weaver.to_function()
    function_ys = [spline(x) for x in expected_xy[0]]
    assert_array_equal(function_ys, expected_xy[1])

    weaver.restore_original()
    assert_array_equal(weaver.get_original()[0], weaver.get()[0])
    assert_array_equal(weaver.get_original()[1], weaver.get()[1])
