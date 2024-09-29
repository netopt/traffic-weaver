r"""Other time series processing."""
from typing import Callable, Tuple, Union, List

import numpy as np
from scipy.interpolate import BSpline, splrep, CubicSpline

from traffic_weaver.interval import IntervalArray
from traffic_weaver.sorted_array_utils import find_closest_lower_equal_element_indices_to_values, \
    find_closest_higher_equal_element_indices_to_values


def _piecewise_constant_interpolate(x, y, new_x, left=None):
    """Piecewise constant filling for monotonically increasing sample points.

    Returns the one-dimensional piecewise constant array with given discrete data points (x, y), evaluated at new_x.

    Parameters
    ----------
    x: np.ndarray
        The x-coordinates of the data points, must be increasing.
    y: np.ndarray
        The y-coordinates of the data points, same length as x.
    new_x
        The x-coordinates at which to evaluate the interpolated values.
    left: float, optional
        Value to return for new_x < x[0], default is y[0].

    Returns
    -------
        The interpolated values, same shape as new_x.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    new_x = np.asarray(new_x)

    new_y = np.zeros(len(new_x))

    indices = find_closest_lower_equal_element_indices_to_values(x, new_x)

    greater_equal_than_first_value_mask = new_x >= x[0]
    lower_than_first_value_mask = new_x < x[0]

    new_y[greater_equal_than_first_value_mask] = y[indices[greater_equal_than_first_value_mask]]
    new_y[lower_than_first_value_mask] = left if left is not None else y[0]
    return new_y


def interpolate(x, y, new_x, method='linear', **kwargs):
    """Interpolate function over new set of points.

    Supports linear, cubic and spline interpolation.

    Parameters
    ----------
    x: array-like
        The x-coordinates of the data points, must be increasing.
    y: array-like
        The y-coordinates of the data points, same length as x.
    new_x: array-like
        New x-coordinates at which to evaluate the interpolated values.
    method: str, default='linear'
        Interpolation method. Supported methods are 'linear', 'constant', 'cubic' and
        'spline'.
    kwargs: dict
        Additional keyword arguments passed to the interpolation function.
        For more details, see kwargs of numpy and scipy interpolation functions.

    Returns
    -------

    See Also
    --------
    `https://numpy.org/doc/stable/reference/generated/numpy.interp.html
    <https://numpy.org/doc/stable/reference/generated/numpy.interp.html>`_
    `https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CubicSpline.html
    <https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CubicSpline.html>`_
    `https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.splrep.html#scipy.interpolate.splrep
    <https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.splrep.html#scipy.interpolate.splrep>`_
    """
    if method == 'linear':
        return np.interp(new_x, x, y, **kwargs)
    if method == 'constant':
        return _piecewise_constant_interpolate(x, y, new_x, **kwargs)
    elif method == 'cubic':
        return CubicSpline(x, y, **kwargs)(new_x)
    elif method == 'spline':
        return BSpline(*splrep(x, y, **kwargs))(new_x)


def repeat(x, y, repeats: int) -> tuple[np.ndarray, np.ndarray]:
    """Extend time series.

    Independent variable is appended with the same spacing,
    dependent variable is copied.

    Parameters
    ----------
    x: 1-D array-like of size n
        Independent variable in strictly increasing order.
    y: 1-D array-like of size n
        Dependent variable.
    repeats: int
        How many times repeat time series.

    Returns
    -------
    ndarray
        x, repeated independent variable.
    ndarray
        y, repeated dependent variable.
    """
    x = np.asanyarray(x, dtype=float)
    y = np.asanyarray(y, dtype=float)
    n = len(x)
    y = np.tile(y, repeats)
    x = np.tile(x, repeats)
    for i in range(1, repeats):
        previous_range_diff = x[n * i - 1] - x[0] + (x[n * i - 1] - x[n * i - 2])
        x[n * i : n * (i + 1)] += previous_range_diff
    return x, y


def trend(
    x, y, fun: Callable[[np.ndarray], np.ndarray], normalized=False
) -> Tuple[np.ndarray, np.ndarray]:
    r"""Apply long-term trend to time series data using provided function.

    Parameters
    ----------
    x: 1-D array-like of size n
        Independent variable in strictly increasing order.
    y: 1-D array-like of size n
        Dependent variable.
    fun: Callable
        Long term trend applied to the data in form of a function.
        Callable signature is `(x) -> y_shift` where
        `x` independent variable axis and
        `y_shift` is independent variable shift for that `x`.
    normalized: bool, default: False
        If true, `x` variable in `fun` is normalized to the range of [0, 1].

    Returns
    -------
    ndarray
        x, independent variable.
    ndarray
        y, shifted dependent variable.
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    range_x = x[-1] - x[0]
    for i in range(len(x)):
        if normalized:
            y[i] += fun(x[i] / range_x)
        else:
            y[i] += fun(x[i])
    return x, y


def linear_trend(x, y, a, normalized=False):
    r"""Adding linear trend to time series.

    Parameters
    ----------
    x: 1-D array-like of size n
        Independent variable in strictly increasing order.
    y: 1-D array-like of size n
        Dependent variable.
    a: float
        Linear coefficient.
    normalized: bool, default: False
        If true, `x` variable in `fun` is normalized to the range of [0, 1].

    Returns
    -------
    ndarray
        x, independent variable.
    ndarray
        y, shifted dependent variable.
    """
    return trend(x, y, lambda x: a * x, normalized)


def spline_smooth(x: np.ndarray, y: np.ndarray, s=None):
    r"""Smooth a function y=x using smoothing spline

    Value of smoothing `s` needs to be set empirically by trial and error for
    specific data.

    https://docs.scipy.org/doc/scipy/tutorial/interpolate/smoothing_splines.html

    Parameters
    ----------
    x, y : array_like
        The data points defining a curve y = f(x)
    s: float, optional
        A smoothing condition. `s` can be used to control the tradeoff between
        closeness and smoothness of fit. Larger `s` means more smoothing while smaller
        values of `s` indicate less smoothing. If `s` is None, it's 'good' value is
        calculated based on number of samples and standard
        deviation.

    Returns
    -------
    BSpline

    Notes
    -----
    If `s` is not provided, it is calculated as:

    .. math::
        s = m \sigma^2

    where :math:`m` is the number of samples and :math:`\sigma` is the estimated
    standard deviation.
    """
    if s is None:
        s = len(y) * np.std(y) ** 2
    return BSpline(*splrep(x, y, s=s))


def noise_gauss(a: Union[np.ndarray, List], snr=None, snr_in_db=True, std=1.0):
    r"""Add gaussian noise to the signal.

    Add noise targeting provided `snr` value. If `snr` is not specified,
    standard deviation `std` value is used.

    Parameters
    ----------
    a: np.ndarray
        Signal for which noise is inserted.
    snr: float | list[float] | ndarray[float], optional
        Signal-to-noise ratio; if `snr_in_db` is True, either is treated
        in decibels or linear values. It can be provided as scalar or list of floats.
        If list of floats provided, for each input element of `a`, corresponding
        value of `snr`
        is considered.
    snr_in_db: bool, default: True
        Determines whether treat `snr` in decibels or linear.
    std: float, default=1.0
        Standard deviation of the noise. Used if `snr` is not provided.

    Returns
    -------
    np.ndarray
        Noised signal.

    Notes
    -----
    Signal-to-noise ratio is defined as:

    .. math::
        SNR = 10*log_{10}(S/N)

    where `S` is signal power and `N` is noise power.

    Gaussian noise has flat power specturm

    .. math::
        N = var(n) = std(n) ^ 2

    Signal power is calculated as:

    .. math::
        E[S^2] = mean(s^2)

    If `snr` is in decibels:

    .. math::
        std(n) = sqrt(mean(s^2) / (10^{SNR_{db}/10}))

    Else if `snr` is in linear scale:

    .. math::
        std(n) = sqrt(mean(s^2) / SNR)

    See Also
    --------
    `https://en.wikipedia.org/wiki/Signal-to-noise_ratio
    <https://en.wikipedia.org/wiki/Signal-to-noise_ratio>`_

    """
    a = np.asarray(a)
    if snr is not None:
        if not np.isscalar(snr):
            snr = np.asarray(snr)
        sp = np.mean(a**2)  # signal power

        if snr_in_db is True:
            std_n = (sp / (10 ** (snr / 10))) ** 0.5
        else:
            std_n = (sp / snr) ** 0.5  # getting noise std from SNR definition
    else:
        std_n = std

    noise = np.random.normal(loc=0, scale=std_n, size=a.shape)
    return a + noise


def average(x, y, interval):
    r"""Average time series over n samples

    Parameters
    ----------
    x: 1-D array-like of size n
        Independent variable in strictly increasing order.
    y: 1-D array-like of size n
        Dependent variable.
    interval: int
        Interval for which calculate the average value.

    Returns
    -------
    ndarray
        x, independent variable.
    ndarray
        y, dependent variable.
    """
    y = np.nanmean(IntervalArray(y, interval).to_2d_array(), axis=1)
    x = IntervalArray(x, interval).to_2d_array()[:, 0]
    return x, y


def truncate(x, y, x_left, x_right, x_left_as_ratio=False, x_right_as_ratio=False):
    """Truncate time series to specific value range or ratio of the range.

    Parameters
    ----------
    x: 1-D array-like of size n
        Independent variable in strictly increasing order.
    y: 1-D array-like of size n
        Dependent variable
    x_left: float
        Value in x array to which truncate arrays from the left.
        If value is not present in x array, closest lower value is selected.
    x_right: float
        Value in x array to which truncate arrays from the right.
        If value is not present in x array, closest higher value is selected.
    x_left_as_ratio: bool, default: False
        If true, `x_left` is treated as ratio of the x array to truncate from the left,
        where 0.0 is the start and 1.0 is the end of the array.
    x_right_as_ratio: bool, default: False
        Ratio of the x array to truncate from the left, where 0.0 is the start and
        1.0 is the end of the array. Ignored, if x_left is not None.

    Returns
    -------
    ndarray
        x, truncated independent variable.
    ndarray
        y, truncated dependent variable.

    """
    if x_left_as_ratio:
        x_left = x_left * (x[-1] - x[0]) + x[0]
    if x_right_as_ratio:
        x_right = x_right * (x[-1] - x[0]) + x[0]

    if x_left >= x_right:
        raise ValueError("x_left must be less than x_right")

    left_id = find_closest_lower_equal_element_indices_to_values(x, [x_left], fill_not_valid=True)[0]

    right_id = find_closest_higher_equal_element_indices_to_values(x, [x_right], fill_not_valid=True)[0] + 1
    return x[left_id:right_id], y[left_id:right_id]


def normalize(a, min_val=0, max_val=1):
    """Normalize array to specific range.

    Parameters
    ----------
    a: array-like
        Array of values to normalize.
    min_val: float, default: 0
        Min value to which normalize array values.
    max_val: float, default: 1
        Max value to which normalize array values.

    Returns
    -------
    ndarray
        Normalized array.

    """
    a = np.asarray(a)
    a_min = a.min()
    a_max = a.max()
    return (a - a_min) / (a_max - a_min) * (max_val - min_val) + min_val
