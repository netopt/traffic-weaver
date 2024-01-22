import pytest

from traffic_weaver.funfit import (
    lin_fit,
    exp_fit,
    exp_lin_fit,
    exp_xy_fit,
    lin_exp_xy_fit,
)


@pytest.fixture
def xy_0():
    return 1.0, 1.0


@pytest.fixture
def xy_1():
    return 2.0, 3.0


@pytest.mark.parametrize(
    "x, expected_y",
    [
        (1, 1),
        (1.25, 1.5),
        (1.5, 2.0),
        (2.0, 3.0),
    ],
)
def test_lin_fit(x, expected_y, xy_0, xy_1):
    y = lin_fit(x, xy_0, xy_1)
    assert y == expected_y


@pytest.mark.parametrize(
    "x, expected_y",
    [
        (1, 1),
        (1.25, 1.125),  # 1/4 ** 2 * 2 = 0.125
        (1.5, 1.5),  # 1/2 ** 2 * 2 = 0.5
        (2, 3),
    ],
)
def test_exp_fit(x, expected_y, xy_0, xy_1):
    y = exp_fit(x, xy_0, xy_1)
    assert y == expected_y


@pytest.mark.parametrize(
    "x, expected_y",
    [
        (1, 1),
        (1.25, 1.875),  # (1 - (3/4) ** 2) * 2 = 0.875
        (1.5, 2.5),  # (1 - (1/2) ** 2) * 2 = 1.5
        (2, 3),
    ],
)
def test_exp_xy_fit(x, expected_y, xy_0, xy_1):
    y = exp_xy_fit(x, xy_0, xy_1)
    assert y == expected_y


@pytest.mark.parametrize(
    "x, expected_y",
    [
        (1, 1),
        (1.25, 1.21875),
        # 1/4 ** 2 * 2 = 0.125 (exp part), 0.5 (lin part), 0.125 * 3/4 + 0.5 * 1/4 (lin
        # combin.)
        (1.5, 1.75),
        # 1/2 ** 2 * 2 = 0.5 (exp part), 1 (lin part), 0.5 * 1/2 + 1 * 1/2 (lin combin.)
        (2, 3),
    ],
)
def test_lin_exp_fit(x, expected_y, xy_0, xy_1):
    y = exp_lin_fit(x, xy_0, xy_1)
    assert y == expected_y


@pytest.mark.parametrize(
    "x, expected_y",
    [
        (1, 1),
        (1.25, 1.59375),
        # (1 - (3/4) ** 2) * 2 = 0.875 (exp part), 0.5 (lin part), 0.875 * 1/4 + 0.5 *
        # 3/4 (lin combin.)
        (1.5, 2.25),
        # (1 - (1/2) ** 2) * 2 = 1.5 (exp part), 1 (lin part), 1.5 * 1/2 + 1 * 1/2 (lin
        # combin.)
        (2, 3),
    ],
)
def test_lin_exp_xy_fit(x, expected_y, xy_0, xy_1):
    y = lin_exp_xy_fit(x, xy_0, xy_1)
    assert y == expected_y
