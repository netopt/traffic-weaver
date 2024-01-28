import numpy as np
import pytest
from numpy.testing import assert_array_equal

from traffic_weaver.interval import IntervalArray


@pytest.fixture
def any_ia():
    return IntervalArray(list(range(10)), 4)


@pytest.mark.parametrize(
    "ia, elem, res",
    [
        (IntervalArray(list(range(10)), 4), 1, 1),
        (IntervalArray(list(range(10)), 4), (1, 0), 4),
        (IntervalArray(list(range(10)), 4), (1, 2), 6),
        (IntervalArray(list(range(10)), 1), 1, 1),
    ],
)
def test_getitem(ia, elem, res):
    assert ia[elem] == res


def test_fail_getitem(any_ia):
    with pytest.raises(IndexError):
        _ = any_ia[(1, 2, 3)]


@pytest.mark.parametrize(
    "ia, elem, val, res",
    [
        (IntervalArray(list(range(10)), 4), 1, 5, 5),
        (IntervalArray(list(range(10)), 4), (1, 0), 5, 5),
        (IntervalArray(list(range(10)), 4), (1, 2), 5, 5),
        (IntervalArray(list(range(10)), 1), 1, 5, 5),
    ],
)
def test_setitem(ia, elem, val, res):
    ia[elem] = val
    assert ia[elem] == res


def test_fail_setitem(any_ia):
    with pytest.raises(IndexError):
        any_ia[(1, 2, 3)] = 0


def test_iterator(any_ia):
    assert_array_equal(list(iter(any_ia)), any_ia.a)


@pytest.mark.parametrize(
    "ia, res",
    [
        (IntervalArray(list(range(10)), 4), list(np.arange(-4.0, 14.0))),
        (IntervalArray(list(range(10)), 1), list(np.arange(-1.0, 11.0))),
    ],
)
def test_extend_linspace(ia, res):
    ia.extend_linspace()
    assert_array_equal(ia.array, res)


@pytest.mark.parametrize(
    "ia, res",
    [
        (
            IntervalArray(list(range(10)), 4),
            [0, 0, 0, 0] + list(np.arange(10.0)) + [9, 9, 9, 9],
        ),
        (IntervalArray(list(range(10)), 1), [0] + list(np.arange(10.0)) + [9]),
    ],
)
def test_extend_constant(ia, res):
    ia.extend_constant()
    print(ia.a)
    assert_array_equal(ia.array, res)


@pytest.mark.parametrize(
    "ia, res",
    [
        (IntervalArray(list(range(10)), 4), 2),
        (IntervalArray(list(range(12)), 4), 3),
        (IntervalArray(list(range(13)), 4), 3),
        (IntervalArray(list(range(10)), 1), 10),
    ],
)
def test_number_of_full_intervals(ia, res):
    assert ia.nr_of_full_intervals() == res


def test_len(any_ia):
    assert len(any_ia) == 10


@pytest.mark.parametrize(
    "ia, res",
    [
        (
            IntervalArray(list(range(10)), 4),
            np.array(
                [[0.0, 1.0, 2.0, 3.0], [4.0, 5.0, 6.0, 7.0], [8.0, 9.0, np.nan, np.nan]]
            ),
        ),
        (IntervalArray(list(range(10)), 1), np.array([np.arange(10)]).reshape(-1, 1)),
    ],
)
def test_as_intervals(ia, res):
    assert_array_equal(ia.as_intervals(), res)


@pytest.mark.parametrize(
    "ia, res",
    [
        (
            IntervalArray(list(range(10)), 4),
            np.array([[0.0, 1.0, 2.0, 3.0, 4.0], [4.0, 5.0, 6.0, 7.0, 8.0]]),
        ),
        (
            IntervalArray(list(range(4)), 1),
            np.array([[0.0, 1.0], [1.0, 2.0], [2.0, 3.0]]),
        ),
    ],
)
def test_as_closed_intervals(ia, res):
    assert_array_equal(ia.as_closed_intervals(drop_last=True), res)


@pytest.mark.parametrize(
    "ia, n, res",
    [
        (IntervalArray(list(range(4)), 2), 2, np.arange(0, 3.5, step=0.5)),
        (IntervalArray(list(range(4)), 1), 4, np.arange(0, 3.25, step=0.25)),
    ],
)
def test_oversample_lispace(ia, n, res):
    ia = ia.oversample_linspace(n)
    assert_array_equal(ia.array, res)


@pytest.mark.parametrize(
    "ia, n, res",
    [
        (IntervalArray(list(range(4)), 2), 2, np.arange(0, 4).repeat(2)[:-1]),
        (IntervalArray(list(range(4)), 1), 4, np.arange(0, 4).repeat(4)[:-3]),
    ],
)
def test_oversample_piecewise(ia, n, res):
    ia = ia.oversample_piecewise(n)
    assert_array_equal(ia.array, res)


def test_repr(any_ia):
    recreated = eval(any_ia.__repr__())
    assert str(recreated) == str(any_ia)
