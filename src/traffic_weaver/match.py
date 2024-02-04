import numpy as np

from .array_utils import left_piecewise_integral
from .process import spline_smooth


def integral_matching_reference_stretch(x, y, x_ref, y_ref, alpha=1.0, s=None):
    """Stretch function to match integrals in reference.

    Stretch function to match integrals piecewise constant function over the
    same domain.

    .. image:: /_static/gfx/integral_matching_reference.pdf

    Reference function is piecewise linear function that can contain only a
    subset of points in original function `x`.
    The target function is stretched according to the integral values and
    intervals provided by the reference function.

    Parameters
    ----------
    x: 1-D array-like of size n
        Independent variable in strictly increasing order.
    y: 1-D array-like of size n
        Dependent variable.
    x_ref: 1-D array-like of size m
        Independent variable in strictly increasing order of the reference function.
        Its size should be lower than size of `x`, and it should contain only subset
        of points of `x`.
    y_ref: 1-D array-like of size m
        Dependent variable of reference function.
    alpha: scalar, default: 1
        Stretching exponent factor.
        Scales how points are stretched if they are closer to the center point.
        If it is greater than 1, they are more stretched in the interval center,
        and less stretched in the boundaries.
        If it is lower than 1, they are more evenly stretched over whole function.
    s: float, optional
        A smoothing condition for spine smoothing.
        If None, no smoothing is applied.

    Raises
    ------
    ValueError
        if `x_ref` contains some point that are not present in `x`.

    Returns
    -------
    ndarray
        of shape (n, ).
        Stretched function matching integral value of reference function.

    Examples
    --------
    >>> import numpy as np
    >>> from traffic_weaver.match import integral_matching_reference_stretch
    >>> y = np.array([1, 1.5, 2, 2.5, 3, 3.5, 4])
    >>> x = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3])
    >>> y_ref = np.array([2.5, 2.5, 4, 3.5])
    >>> x_ref = np.array([0, 1, 2, 3])
    >>> integral_matching_reference_stretch(x, y, x_ref, y_ref, s=0.0)
    array([1. , 3.5, 2. , 2.5, 3. , 4.5, 4. ])

    """
    interval_point_indices = np.where(np.in1d(x, x_ref))[
        0
    ]  # get indices of elements in x array that are in x_ref array
    if len(interval_point_indices) != len(x_ref):
        raise ValueError("`x_ref` contains some points that are not in the `x`")
    integral_values = left_piecewise_integral(x_ref, y_ref)
    res_y = interval_integral_matching_stretch(
        x,
        y,
        integral_values=integral_values,
        interval_point_indices=interval_point_indices,
        alpha=alpha,
    )
    return res_y if s is None else spline_smooth(x, res_y, s)(x)


def integral_matching_stretch(x, y, integral_value=0, dx=1.0, alpha=1.0, s=None):
    r"""Stretches function y=f(x) to match integral value.

    .. image:: /_static/gfx/integral_matching.pdf

    This method creates function :math:`z=g(x)` from :math:`y=f(x)` such that the
    integral of :math:`g(x)` is equal to the provided integral value, and points
    are transformed inversely proportionally to the distance from the
    function domain center. Function integral is numerically approximated using
    trapezoidal rule on provided points.

    Parameters
    ----------
    x: 1-D array-like of size n, optional
        Independent variable in strictly increasing order.
        If passed None, it is evenly spaced `dx` apart.
    y: 1-D array-like of size n
        Dependent variable.
    integral_value: float, default: 0
        Target integral value.
    dx : scalar, optional
        The spacing between sample points when `x` is None. By default, it is 1.
    alpha: scalar, default: 1
        Stretching exponent factor.
        Scales how points are stretched if they are closer to the center point.
        If it is greater than 1, they are more stretched in the center, and less
        stretched in the boundaries.
        If it is lower than 1, they are more evenly stretched over whole function.
    s: float, optional
        A smoothing condition for spine smoothing.
        If None, no smoothing is applied.

    Returns
    -------
    ndarray
        of shape (n, ).
        Stretched function matching integral value.

    Notes
    ----------
    Let assume that:

    * function contains n+1 values
    * :math:`\Delta x = x_n - x_0`
    * :math:`\Delta x_{i} = x_i - x_{i-1}`
    * :math:`x_{n/2}=(x_n + x_0) / 2`
    * :math:`\Delta P` - difference between
      target integral value and current function integral
    * :math:`\alpha` - is stretching exponent factor

    Beginning and end of function :math:`g(x)` (i.e., :math:`z_0 = y_0` and
    :math:`z_n = y_n`) are fixed.
    All the remaining points are shifted inversely proportionally to the distance of
    :math:`x_{n/2}`.

    The shifting factor :math:`w_i` for each point :math:`x_i` is calculated as:

    .. math::
        w_i = 1 - (2 * abs(x_{n/2} - x_{i})) / \Delta x) ^ \alpha

    where :math:`\alpha` is shifting exponent factor (by default equal to 1).

    Each point is :math:`z_i` is shifted by :math:`\hat{y} \cdot w_i`
    where :math:`\hat{y}` is a shift scaling factor to match desired integral value.

    Difference in integral between target function and current function
    is calculated as:

    .. math::
        \Delta P = \sum_{i=1}^N \left[\frac{w_{i-1} + w_i}{2} \hat{y}
        \cdot \Delta x_i \right]

    Shift scaling factor :math:`\hat{y}` can be calculated as:

    .. math::
        \hat{y} = 2 \Delta P / \sum_{i=1}^N \left[(w_{i-1} + w_i) \Delta x_i \right]

    Next, if :math:`s` is given, created function is estimated with
    spline function :math:`h(x)` which satisfies:

    .. math::
        \sum_{i} [h(x_i) - g(x)]^2 \le s

    """
    y = np.array(y)
    if x is None:
        x = np.arange(len(y) * dx, step=dx)
    else:
        x = np.array(x)

    current_integral = np.trapz(y, x)
    delta_p = integral_value - current_integral
    x_n2 = (x[-1] + x[0]) / 2

    delta_x = x[-1] - x[0]
    delta_xi = np.diff(x)

    w = 1 - (2 * np.abs(x_n2 - x) / delta_x) ** alpha
    y_hat = 2 * delta_p / np.sum((w[1:] + w[:-1]) * delta_xi)

    res_y = y + y_hat * w
    return res_y if s is None else spline_smooth(x, res_y, s)(x)


def interval_integral_matching_stretch(
    x, y, dx=1.0, integral_values=None, interval_point_indices=None, alpha=1.0, s=None
):
    r"""Stretches function y=f(x) to match integral value in given intervals.

    This method creates function :math:`z=g(x)` from :math:`y=f(x)` such that the
    integral of :math:`g(x)` is equal to the provided corresponding `integral_values`
    in intervals given by `interval_point_indices`.
    In each interval, points are transformed inversely proportionally to the distance
    from the interval center. Function integral is numerically approximated using
    trapezoidal rule on provided points.

    Each period stretch is delegated to `integral_matching_stretch`.

    Parameters
    ----------
    x: 1-D array-like of size n, optional
        Independent variable in strictly increasing order.
        If passed None, it is evenly spaced `dx` apart.
    y: 1-D array-like of size n
        Dependent variable.
    dx : scalar, optional
        The spacing between sample points when `x` is None. By default, it is 1.
    integral_values: list[float] | ndarray, optional
        Target integral values.
        By default, it is `[0] * (len(interval_points_indices) - 1)`.
        If `interval_point_indices` are not specified, `ValueError` is raised.
    interval_point_indices: list[int] | ndarray, optional
        Indices in `x` array specifying intervals over which function is
        stretched to match corresponding `integral_values`.
        By default, it is evenly spaced, i.e.,
        `[0, len(y) / n, 2 len(y) / n, ..., len(y)]`.
        If `integral_values` are not specified` `ValueError` is raised.
    alpha: scalar, default: 1
        Stretching exponent factor.
        Scales how points are stretched if they are closer to the center point.
        If it is greater than 1, they are more stretched in the interval center,
        and less stretched in the boundaries.
        If it is lower than 1, they are more evenly stretched over whole function.
    s: float, optional
        A smoothing condition for spine smoothing.
        If None, no smoothing is applied.

    Returns
    -------
    ndarray
        of shape (n, ).
        Stretched function matching integral value.
    """

    if x is None:
        x = np.arange(len(y) * dx, step=dx)
    else:
        x = np.asarray(x)

    if integral_values is None and interval_point_indices is None:
        raise ValueError(
            "integral_values and interval_points cannot be None at the same time"
        )
    if integral_values is None:
        integral_values = [0] * (len(interval_point_indices) - 1)
    if interval_point_indices is None:
        interval_point_indices = np.arange(
            0, len(y) + 1, int(len(y) / len(integral_values))
        )

    y = np.array(y, dtype=float)

    for integral_value, start, end in zip(
        integral_values, interval_point_indices[:-1], interval_point_indices[1:]
    ):
        end = end + 1
        y[start:end] = integral_matching_stretch(
            x[start:end], y[start:end], integral_value=integral_value, alpha=alpha
        )
    return y if s is None else spline_smooth(x, y, s)(x)
