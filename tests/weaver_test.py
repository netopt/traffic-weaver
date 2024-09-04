import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_array_equal

from traffic_weaver import Weaver, PiecewiseConstantOversample


@pytest.fixture
def xy():
    return np.arange(5), np.array([1, 3, 4, 1, 2])


@pytest.fixture
def expected_xy():
    return np.arange(0, 4.5, 0.5), np.array([2, 2, 6, 6, 8, 8, 2, 2, 4])


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
    weaver.scale_x(1)
    weaver.scale_y(2)
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


def test_weaver_factories(xy):
    weaver = Weaver(xy[0], xy[1])

    weaver2 = Weaver.from_dataframe(pd.DataFrame({"x": xy[0], "y": xy[1]}))
    weaver3 = Weaver.from_2d_array(np.column_stack(xy))
    weaver4 = Weaver(x=None, y=xy[1])

    assert_array_equal(weaver.get()[0], weaver2.get()[0])
    assert_array_equal(weaver.get()[1], weaver2.get()[1])

    assert_array_equal(weaver.get()[0], weaver3.get()[0])
    assert_array_equal(weaver.get()[1], weaver3.get()[1])

    assert_array_equal(weaver.get()[0], weaver4.get()[0])
    assert_array_equal(weaver.get()[1], weaver4.get()[1])


def test_raise_exception_on_wrong_input_dimension():
    with pytest.raises(ValueError):
        Weaver([1, 2], [1, 2, 3])

    with pytest.raises(ValueError):
        Weaver.from_2d_array(np.zeros((3, 2, 2)))
