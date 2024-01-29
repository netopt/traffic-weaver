r"""get y = f(x) based on pair of two points using given function shape.

This is the internal module to help point values calculation.
"""


def lin_fit(x, xy_0: tuple, xy_1: tuple):
    r"""Get value of point using linear function

    Get :math:`y = f(x)` using linear function of form
    :math:`y = ax`
    on range :math:`(x_0, x_1)`

    Parameters
    ----------
    x: scalar
        Point for which return value of `y`
    xy_0: tuple of two floats
        Starting point `(x0, y0)`
    xy_1: tuple of two floats
        Ending point `(x0, y0)`

    Returns
    -------
    float
        Value of `y` at point `x`.
    """
    x_0, y_0 = xy_0
    x_1, y_1 = xy_1
    return y_0 + (y_1 - y_0) * (x - x_0) / (x_1 - x_0)


def exp_fit(x, xy_0: tuple, xy_1: tuple, alpha: float = 2.0):
    r"""Get value of point using exponential function

    Get :math:`y = f(x)` using exp function of form
    :math:`y = ax^\alpha`
    on range :math:`(0, 1)` scaled to :math:`(x_0, x_1)`

    Parameters
    ----------
    x: float
        Point for which return value of `y`
    xy_0: tuple of two floats
        Starting point `(x0, y0)`
    xy_1: tuple of two floats
        Ending point `(x0, y0)`
    alpha: float, optional
        Exponent factor. Default is 2.

    Returns
    -------
    float
        Value of `y` at point `x`.
    """
    (x_0, y_0) = xy_0
    x_1, y_1 = xy_1
    return y_0 + (y_1 - y_0) * ((x - x_0) / (x_1 - x_0)) ** alpha


def exp_xy_fit(x, xy_0: tuple, xy_1: tuple, alpha: float = 2.0):
    r"""Get value of point using exponential function mirrored over y=x

    Get :math:`y = f(x)` using exp function mirrored over :math:`x = y` line of form
    :math:`y = a (1 - (1-x)^\alpha)`
    on range :math:`(0, 1)` scaled to :math:`(x_0, x_1)`

    Parameters
    ----------
    x: float
        Point for which return value of `y`
    xy_0: tuple of two floats
        Starting point `(x0, y0)`
    xy_1: tuple of two floats
        Ending point `(x0, y0)`
    alpha: float, optional
        Exponent factor. Default is 2.

    Returns
    -------
    float
        Value of `y` at point `x`.
    """
    x_0, y_0 = xy_0
    x_1, y_1 = xy_1
    return y_0 + (y_1 - y_0) * (1 - ((x_1 - x) / (x_1 - x_0)) ** alpha)


def exp_lin_fit(x, xy_0: tuple, xy_1: tuple, alpha=2):
    r"""Get value of point using combination of linear and exponential function

    Get :math:`y = f(x)` using linear and exp function line of form
    :math:`y = a ((1- b) \cdot x + b \cdot x^\alpha)`
    on range :math:`(0, 1)` scaled to :math:`(x_0, x_1)`
    where :math:`b = (x - x_0)`

    It is a linear combination of values returned be :func:`exp_fit` and
    :func:`lin_fit`.

    Parameters
    ----------
    x: float
        Point for which return value of `y`
    xy_0: tuple of two floats
        Starting point `(x0, y0)`
    xy_1: tuple of two floats
        Ending point `(x0, y0)`
    alpha: float, optional
        Exponent factor. Default is 2.

    Returns
    -------
    float
        Value of `y` at point `x`.
    """
    x_0, y_0 = xy_0
    x_1, y_1 = xy_1
    return lin_fit(x, xy_0, xy_1) * (x - x_0) / (x_1 - x_0) + exp_fit(
        x, xy_0, xy_1, alpha
    ) * (x_1 - x) / (x_1 - x_0)


def lin_exp_xy_fit(x, xy_0: tuple, xy_1: tuple, alpha=2):
    r"""Get value of point using combination of linear and exponential function
    mirrored over xy line

    Get :math:`y = f(x)` using linear and exp function line mirrored over xy of form
    :math:`y = a (x + 1 - (1-x)^\alpha)`
    on range :math:`(0, 1)` scaled to :math:`(x_0, x_1)`

    It is a linear combination of values returned be :func:`lin_fit` and
    :func:`exp_xy_fit`.

    Parameters
    ----------
    x: float
        Point for which return value of `y`
    xy_0: tuple of two floats
        Starting point `(x0, y0)`
    xy_1: tuple of two floats
        Ending point `(x0, y0)`
    alpha: float, optional
        Exponent factor. Default is 2.

    Returns
    -------
    float
        Value of `y` at point `x`.
    """
    x_0, y_0 = xy_0
    x_1, y_1 = xy_1
    return exp_xy_fit(x, xy_0, xy_1, alpha) * (x - x_0) / (x_1 - x_0) + lin_fit(
        x, xy_0, xy_1
    ) * (x_1 - x) / (x_1 - x_0)
