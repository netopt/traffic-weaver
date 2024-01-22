r"""Other time series utilities"""

import numpy as np


def add_one_sample(x: np.ndarray, y: np.ndarray, make_periodic=False):
    r"""Add one sample to the end of time series.

    Add one sample to `x` and `y` array. Newly added point `x_i` point is distant from
    the last point of `x` same as the last from the one before last point.
    If `make_periodic` is False, newly added `y_i` point is the same as the last  point
    of `y`. If `make_periodic` is True, newly added point is the same as the first point
    of `y`.

    Parameters
    ----------
    x: 1-D array-like of size n
        Independent variable in strictly increasing order.
    y: 1-D array-like of size n
        Dependent variable.
    make_periodic: bool, default: False
        If false, append the last `y` point to `y` array.
        If true, append the first `y` point to `y` array.

    Returns
    -------
    ndarray
        x, independent variable.
    ndarray
        y, dependent variable.
    """
    x = np.append(x, 2 * x[-1] - x[-2])
    if not make_periodic:
        y = np.append(y, y[-1])
    else:
        y = np.append(y, y[0])
    return x, y
