import pytest
from numpy.testing import assert_array_equal

from traffic_weaver.array_utils import (
    oversample_linspace,
    oversample_piecewise_constant,
    extend_linspace,
    extend_constant,
    append_one_sample,
)


@pytest.mark.parametrize(
    "x, y, make_periodic, expected_x, expected_y",
    [
        ([1, 2, 4], [1, 2, 3], False, [1, 2, 4, 6], [1, 2, 3, 3]),
        ([1, 2, 4], [1, 2, 3], True, [1, 2, 4, 6], [1, 2, 3, 1]),
    ],
)
def test_add_one_sample(x, y, make_periodic, expected_x, expected_y):
    x, y = append_one_sample(x, y, make_periodic)
    assert_array_equal(x, expected_x)
    assert_array_equal(y, expected_y)


@pytest.mark.parametrize(
    "x, num, expected",
    [
        ([1], 2, 1),
        ([1, 1], 3, [1, 1, 1, 1]),
        ([1, 2, 3], 4, [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0]),
        ([1, 2, 3], 1, [1, 2, 3]),  # test when num <= 2
    ],
)
def test_oversample_linspace(x, num, expected):
    xs = oversample_linspace(x, num)
    assert_array_equal(xs, expected)


@pytest.mark.parametrize(
    "x, num, expected",
    [
        ([1], 2, 1),
        ([1, 1], 3, [1, 1, 1, 1]),
        ([1, 2, 3], 4, [1, 1, 1, 1, 2, 2, 2, 2, 3]),
        ([1, 2, 3], 1, [1, 2, 3]),
        # test when num <= 2
    ],
)
def test_oversample_piecewise(x, num, expected):
    xs = oversample_piecewise_constant(x, num)
    assert_array_equal(xs, expected)


@pytest.mark.parametrize(
    "x, num, direction, lstart, rstop, expected",
    [
        ([1, 2, 3], 2, "both", None, None, [-1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0]),
        ([1, 2, 3], 4, "right", 0, 4, [1.0, 2.0, 3.0, 3.25, 3.5, 3.75, 4.0]),
        ([1, 2, 3], 4, "left", 0, 4, [0.0, 0.25, 0.5, 0.75, 1.0, 2.0, 3.0]),
    ],
)
def test_extend_linspace(x, num, direction, lstart, rstop, expected):
    xs = extend_linspace(x, num, direction, lstart, rstop)
    assert_array_equal(xs, expected)


@pytest.mark.parametrize(
    "x, num, direction, expected",
    [
        ([1, 2, 3], 2, "both", [1, 1, 1, 2, 3, 3, 3]),
        ([1, 2, 3], 4, "right", [1, 2, 3, 3, 3, 3, 3]),
        ([1, 2, 3], 4, "left", [1, 1, 1, 1, 1, 2, 3]),
    ],
)
def test_extend_constant(x, num, direction, expected):
    xs = extend_constant(x, num, direction)
    assert_array_equal(xs, expected)
