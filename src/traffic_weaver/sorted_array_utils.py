r"""Array utilities.
"""
from typing import Tuple, List, Union

import numpy as np


def append_one_sample(
        x: Union[np.ndarray, List], y: Union[np.ndarray, List], make_periodic=False
) -> Tuple[np.ndarray, np.ndarray]:
    r"""Add one sample to the end of time series.

    Add one sample to `x` and `y` array. Newly added point `x_i` point is distant from
    the last point of `x` same as the last from the one before the last point.
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
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)

    x = np.append(x, 2 * x[-1] - x[-2])
    if not make_periodic:
        y = np.append(y, y[-1])
    else:
        y = np.append(y, y[0])
    return x, y


def oversample_linspace(a: np.ndarray, num: int):
    r"""Oversample array using linspace between each consecutive pair of array elements.

    E.g., Array [1, 2, 3] oversampled by 2 becomes [1, 1.5, 2, 2.5, 3].

    If input array is of size `n`, then resulting array is of size `(n - 1) * num + 1`.

    If `n` is lower than 2, the original array is returned.

    Parameters
    ----------
    a: 1-D array
        Input array to oversample.
    num: int
        Number of elements inserted between each pair of array elements. Larger or
        equal to 2.

    Returns
    -------
    ndarray
        1-D array containing `num` linspaced elements between each array elements' pair.
        Its length is equal to `(len(a) - 1) * num + 1`

    Examples
    --------
    >>> import numpy as np
    >>> from traffic_weaver.sorted_array_utils import oversample_linspace
    >>> oversample_linspace(np.asarray([1, 2, 3]), 4).tolist()
    [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0]

    """
    if num < 2:
        return a
    a = np.asarray(a, dtype=float)
    return np.append(np.linspace(a[:-1], a[1:], num=num + 1)[:-1].T.flatten(), a[-1])


def oversample_piecewise_constant(a: np.ndarray, num: int):
    r"""Oversample array using same left value between each consecutive pair of array
    elements.

    E.g., Array [1, 2, 3] oversampled by 2 becomes [1, 1, 2, 2, 3].

    If input array is of size `n`, then resulting array is of size `(n - 1) * num + 1`.

    If `n` is lower than 2, the original array is returned.

    Parameters
    ----------
    a: 1-D array
        Input array to oversample.
    num: int
        Number of elements inserted between each pair of array elements. Larger or
        equal to 2.

    Returns
    -------
    ndarray
        1-D array containing `num` elements between each array elements' pair.
        Its length is equal to `(len(a) - 1) * num + 1`

    Examples
    --------
    >>> import numpy as np
    >>> from traffic_weaver.sorted_array_utils import oversample_piecewise_constant
    >>> oversample_piecewise_constant(np.asarray([1.0, 2.0, 3.0]), 4).tolist()
    [1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 3.0]

    """
    if num < 2:
        return a
    a = np.asarray(a)
    return a.repeat(num)[: -num + 1]


def extend_linspace(
        a: np.ndarray, n: int, direction="both", lstart: float = None, rstop: float = None
):
    """Extends array using linspace with n elements.

    Extends array `a` from left and/or right with `n` elements each side.

    When extending to the left,
    the starting value is `lstart` (inclusive) and ending value as `a[0]` (exclusive).
    By default, `lstart` is `a[0] - (a[n] - a[0])`.

    When extending to the right,
    the starting value `a[-1]` (exclusive) and ending value is `rstop` (inclusive).
    By default, `rstop` is `a[-1] + (a[-1] - a[-1 - n])`

    `direction` determines whether to extend to `both`, `left` or `right`.
    By default, it is 'both'.

    Parameters
    ----------
    a: 1-D array
    n: int
        Number of elements to extend
    direction: 'both', 'left' or 'right', default: 'both'
        Direction in which array should be extended.
    lstart: float, optional
        Starting value of the left extension.
        By default, it is `a[0] - (a[n] - a[0])`.
    rstop: float, optional
        Ending value of the right extension.
        By default, it is `a[-1] + (a[-1] - a[-1 - n])`.

    Returns
    -------
    ndarray
        1-D extended array.

    Examples
    --------
    >>> import numpy as np
    >>> from traffic_weaver.sorted_array_utils import extend_linspace
    >>> a = np.array([1, 2, 3])
    >>> extend_linspace(a, 2, direction='both').tolist()
    [-1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0]

    >>> extend_linspace(a, 4, direction='right', rstop=4).tolist()
    [1.0, 2.0, 3.0, 3.25, 3.5, 3.75, 4.0]

    """
    a = np.asarray(a, dtype=float)
    if direction == "both" or direction == "left":
        if lstart is None:
            lstart = 2 * a[0] - a[n]
        ext = np.linspace(lstart, a[0], n + 1)[:-1]
        a = np.insert(a, 0, ext)

    if direction == "both" or direction == "right":
        if rstop is None:
            rstop = 2 * a[-1] - a[-n - 1]
        ext = np.linspace(a[-1], rstop, n + 1)[1:]
        a = np.insert(a, len(a), ext)

    return a


def extend_constant(a: np.ndarray, n: int, direction="both"):
    """Extends array with first/last value with n elements.

    Extends array `a` from left and/or right with `n` elements each side.

    When extending to the left, value `a[0]` is repeated.
    When extending to the right, value `a[-1]` is repeated.

    `direction` determines whether to extend to `both`, `left` or `right`.
    By default, it is 'both'.

    Parameters
    ----------
    a: 1-D array
    n: int
        Number of elements to extend
    direction: 'both', 'left' or 'right', optional: 'both'
        Direction in which array should be extended.

    Returns
    -------
    ndarray
        1-D extended array.

    Examples
    --------
    >>> import numpy as np
    >>> from traffic_weaver.sorted_array_utils import extend_constant
    >>> a = np.array([1, 2, 3])
    >>> extend_constant(a, 2, direction='both').tolist()
    [1, 1, 1, 2, 3, 3, 3]

    """
    a = np.asarray(a)
    if direction == "both" or direction == "left":
        a = np.insert(a, 0, [a[0]] * n)
    if direction == "both" or direction == "right":
        a = np.insert(a, len(a), [a[-1]] * n)
    return a


def left_piecewise_integral(x, y):
    r"""Integral values between each pair of points using piecewise constant approx.

    In particular, if function contains average values, then it corresponds to the
    exact value of the integral.

    Parameters
    ----------
    x: 1-D array-like of size n
        Independent variable in strictly increasing order.
    y: 1-D array-like of size n
        Dependent variable.

    Returns
    -------
    1-D array-like of size n-1
        Values of the integral.
    """
    d = np.diff(x)
    return y[:-1] * d


def trapezoidal_integral(x, y):
    """Calculates integral between each pair of points using trapezoidal rule.

    Parameters
    ----------
    x: 1-D array-like of size n
        Independent variable in strictly increasing order.
    y: 1-D array-like of size n
        Dependent variable.

    Returns
    -------
    1-D array-like of size n-1
        Values of the integral.

    """
    return (y[:-1] + y[1:]) / 2 * np.diff(x)


def find_closest_lower_equal_element_indices_to_values(x: Union[np.ndarray, list], lookup: Union[np.ndarray, list],
                                                       fill_not_valid_with_first_element: bool = True):
    """Find indices of closest lower or equal element in x to each element in lookup.

    Parameters
    ----------
    x: np.ndarray
        Array of values to search in.
    lookup: np.ndarray
        Values to search for.
    fill_not_valid_with_first_element: bool, default: True
        If True, fill indices of lookup values that are lower than the first element in 'x' with 0.
    Returns
    -------
    np.ndarray
        Array of indices of closest lower or equal element in x to each element in lookup.
    """
    indices = np.zeros(len(lookup), dtype=np.int64)

    x_it = iter(x)
    x_val = next(x_it)
    x_next_val = next(x_it, None)
    x_idx = 0

    lookup_it = iter(lookup)
    lookup_val = next(lookup_it)
    lookup_idx = 0

    # lookup value lower than x
    # shift lookup until it is higher equal than the first element in x
    while lookup_val is not None and lookup_val < x_val:
        indices[lookup_idx] = x_idx if fill_not_valid_with_first_element else -1
        lookup_val = next(lookup_it, None)
        lookup_idx += 1

    # lookup value is higher than the first element in x
    while lookup_val is not None:
        # if lookup is higher than the next x
        # move x to the right
        while x_next_val is not None and x_next_val <= lookup_val:
            x_next_val = next(x_it, None)
            x_idx += 1
            if x_next_val is None:
                break
        # lookup value is higher than the current x and lower than the next x
        indices[lookup_idx] = x_idx
        lookup_val = next(lookup_it, None)
        lookup_idx += 1
    return indices


def find_closest_higher_equal_element_indices_to_values(x: Union[np.ndarray, list], lookup: Union[np.ndarray, list],
                                                        fill_not_valid_with_last_element: bool = True):
    """Find indices of closest higher or equal element in x to each element in lookup.

    Parameters
    ----------
    x: np.ndarray
        Array of values to search in.
    lookup: np.ndarray
        Values to search for.
    fill_not_valid_with_last_element: bool, default: True
        If True, fill indices of lookup values that are higher than the last element in 'x' with 'len(x) - 1'.

    Returns
    -------
    np.ndarray
        Array of indices of closest higher or equal element in x to each element in lookup.
    """
    indices = np.zeros(len(lookup), dtype=np.int64)

    x_it = iter(x)
    x_val = next(x_it)
    x_next_val = next(x_it, None)
    x_idx = 0

    lookup_it = iter(lookup)
    lookup_val = next(lookup_it)
    lookup_idx = 0

    # lookup value lower than x
    # shift lookup until it is higher than the first element in x
    while lookup_val is not None and lookup_val <= x_val:
        indices[lookup_idx] = x_idx
        lookup_val = next(lookup_it, None)
        lookup_idx += 1

    # lookup value is higher than the first element in x
    while lookup_val is not None:
        # if lookup is higher than the next x
        # move x to the right
        while x_next_val is not None and x_next_val < lookup_val:
            x_next_val = next(x_it, None)
            x_idx += 1
            if x_next_val is None:
                break
            # lookup value is higher than the current x and lower than the next x
        if x_next_val is None:
            indices[lookup_idx] = x_idx if fill_not_valid_with_last_element else len(x)
        else:
            indices[lookup_idx] = x_idx + 1
        lookup_val = next(lookup_it, None)
        lookup_idx += 1
    return indices