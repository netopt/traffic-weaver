r"""Other time series processing."""
from typing import Callable, Tuple, Union, List

import numpy as np
from scipy.interpolate import BSpline, splrep

from traffic_weaver.interval import IntervalArray


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
    x, y, fun: Callable[[np.ndarray], np.ndarray]
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
        `x` independent variable axis normalized to (0, 1) range and
        `y_shift` is independent variable shift for that `x`.

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
        y[i] += fun(x[i] / range_x)
    return x, y


def linear_trend(x, y, a):
    r"""Adding linear trend to time series.

    Parameters
    ----------
    x: 1-D array-like of size n
        Independent variable in strictly increasing order.
    y: 1-D array-like of size n
        Dependent variable.
    a: float
        Linear coefficient.

    Returns
    -------
    ndarray
        x, independent variable.
    ndarray
        y, shifted dependent variable.
    """
    return trend(x, y, lambda x: a * x)


def spline_smooth(x: np.ndarray, y: np.ndarray, s=None):
    r"""Smooth a function y=x using smoothing splines

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
