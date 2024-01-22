import numpy as np
import pytest
from pytest import approx

from traffic_weaver.match import (
    integral_matching_stretch,
    interval_integral_matching_stretch,
)


@pytest.fixture
def y():
    return [1, 2, 2.1, -2, 6, 4, 2, 2, 3, 5, 6]


@pytest.fixture
def x():
    return [-2, -1, 1, 3, 4, 5, 6, 7, 8, 10, 11]


@pytest.mark.parametrize("expected_integral", [10, 23.25, 30])
def test_integral_matching_stretch(expected_integral, x, y):
    y2 = integral_matching_stretch(x, y, expected_integral)
    stretched_integral = np.trapz(y2, x)

    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # ax.plot(x, y)
    # ax.plot(x, y2)
    # plt.show()

    assert stretched_integral == approx(expected_integral)
    assert y2[0] == y[0]
    assert y2[-1] == y[-1]


def test_integral_matching_stretch_with_missing_x(y):
    expected_integral = 10

    y2 = integral_matching_stretch(None, y, integral_value=expected_integral)
    x = np.arange(len(y2))
    stretched_integral = np.trapz(y2, x)

    assert stretched_integral == approx(expected_integral)
    assert y2[0] == y[0]
    assert y2[-1] == y[-1]


def test_integral_matching_stretch_with_missing_expected_integral(x, y):
    y2 = integral_matching_stretch(x, y)

    expected_integral = 0

    stretched_integral = np.trapz(y2, x)

    assert stretched_integral == approx(expected_integral)
    assert y2[0] == y[0]
    assert y2[-1] == y[-1]


def get_integrals_based_on_interval_points(x, y, interval_points):
    return [
        np.trapz(
            y[interval_points[i] : interval_points[i + 1] + 1],
            x[interval_points[i] : interval_points[i + 1] + 1],
        )
        for i in range(len(interval_points) - 1)
    ]


@pytest.mark.parametrize(
    "expected_integrals, interval_points",
    [
        ([20.2, 12, 5], [0, 3, 5, 9]),
        ([23.25, 10, 20], [0, 3, 6, 9]),
        ([30, 6, 2], None),
    ],
)
def test_interval_integral_with_matching_stretch(
    expected_integrals, interval_points, y, x
):
    y2 = interval_integral_matching_stretch(
        x,
        y,
        integral_values=expected_integrals,
        interval_point_indices=interval_points,
    )

    # if no interval points given, they are created evenly
    if interval_points is None:
        interval_points = [0, 3, 6, 9]

    stretched_integrals = get_integrals_based_on_interval_points(x, y2, interval_points)

    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # ax.plot(x, y)
    # ax.plot(x, y2)
    #
    # plt.show()

    assert stretched_integrals == approx(expected_integrals)
    for i in range(len(expected_integrals)):
        assert y2[interval_points[i]] == y[interval_points[i]]
        assert y2[interval_points[i + 1]] == y[interval_points[i + 1]]


def test_interval_integral_matching_stretch_with_missing_x(y):
    expected_integrals = [49.46, 25]
    interval_points = [0, 3, 8]

    y2 = interval_integral_matching_stretch(
        None,
        y,
        integral_values=expected_integrals,
        interval_point_indices=interval_points,
    )
    x = np.arange(len(y2))

    stretched_integrals = get_integrals_based_on_interval_points(x, y2, interval_points)

    assert stretched_integrals == approx(expected_integrals)
    for i in range(len(expected_integrals)):
        assert y2[interval_points[i]] == y[interval_points[i]]
        assert y2[interval_points[i + 1]] == y[interval_points[i + 1]]


def test_interval_integral_matching_stretch_with_missing_expected_integral(x, y):
    interval_points = [0, 3, 10]

    y2 = interval_integral_matching_stretch(
        x, y, interval_point_indices=interval_points
    )

    stretched_integrals = get_integrals_based_on_interval_points(x, y2, interval_points)
    expected_integrals = [0] * (len(interval_points) - 1)

    assert stretched_integrals == approx(expected_integrals)
    for i in range(len(expected_integrals)):
        assert y2[interval_points[i]] == y[interval_points[i]]
        assert y2[interval_points[i + 1]] == y[interval_points[i + 1]]


def test_fail_integral_matching_stretch_with_missing_expected_integral_and_intervals(
    x, y
):
    with pytest.raises(ValueError) as exc_info:
        interval_integral_matching_stretch(x, y)
    assert exc_info.type is ValueError
