r"""Oversample average function with given recreation strategy.

"""

from abc import ABC, abstractmethod

import numpy as np
from scipy.interpolate import CubicSpline

from .funfit import lin_fit, lin_exp_xy_fit, exp_lin_fit
from .interval import IntervalArray
from .array_utils import (
    oversample_linspace,
    oversample_piecewise_constant,
)


class AbstractOversample(ABC):
    r"""Abstract class for oversampling `n` times. a function `y` measured in `x`.

    To perform oversampling, call `oversample()` method, which returns newly created
    points.

    By default, `x` axis is oversampled with `n` linearly space values between each
    point. To change this behaviour, override `_initial_x_oversample` method.

    By default, `y` axis is oversampled with `n` piecewise constant values between each
    point. To change this behaviour, override `_initial_y_oversample` method.

    The `oversample()` method returns oversampled values for x and y.

    In the following derived classes, term 'interval' refers to the distance
    between two consecutive observations (values in `y` based on `x`).
    Each interval contains `n` samples obtained by oversampling.

    Parameters
    ----------
    x: 1-D array-like
        Independent variable in strictly increasing order.
    y: 1-D array-like
        Dependent variable.
    n: int
        Number of points oversampled and recreated in the function for each interval.
        Cannot be lower than 2.
    **kwargs: dict
        Arbitrary keyword arguments for concrete implementations.

    See Also
    --------
    :func:`~traffic_weaver.interval.IntervalArray`
    """

    def __init__(self, x, y, n, **kwargs):
        self.x = np.asarray(x, dtype=float)
        self.y = np.asarray(y, dtype=float)
        self.n = n
        if n < 2:
            raise ValueError("n cannot be lower than 2.")

    @abstractmethod
    def oversample(self):
        """Perform oversample on `x` and `y` variables.

        Returns
        -------
        xs: ndarray
            Oversampled independent variable `x`.
        ys: ndarray
            Oversampled dependent variable `y`.
        """
        pass

    def _initial_oversample(self):
        r"""Returns initially oversampled tuple"""
        return (
            self._initial_x_oversample(),
            self._initial_y_oversample(),
        )

    def _initial_x_oversample(self):
        r"""Initial oversample of `x` axis with linearly spaced function.

        Returns:
            ndarray
                Oversampled `x`.
        """
        return oversample_linspace(self.x, num=self.n)

    def _initial_y_oversample(self):
        r"""Initial oversample of `y` axis with piecewise constant function.

        Returns:
            ndarray
                Oversampled `y`.
        """
        return oversample_piecewise_constant(self.y, num=self.n)


class PiecewiseConstantOversample(AbstractOversample):
    r"""Oversample function using piecewise constant values."""

    def oversample(self):
        return self._initial_oversample()


class FunctionOversample(AbstractOversample):
    r"""Oversample using created sampling function.

    Created sampling function should take `x` as an argument and return corresponding
    `y` value.

    Sampling function can be specified by overriding :func:`_get_sampling_function()`
    method. If method is not override `sampling_function_supplier` factory is used to
    produce a sampling function.

    Parameters
    ----------
    x: 1-D array-like
        Independent variable in strictly increasing order.
    y: 1-D array-like
        Dependent variable.
    n: int
        Number of points oversampled and recreated in the function.
    sampling_function_supplier: Callable[[np.ndarray, np.ndarray], Callable]
        Factory that takes an input `x` and `y` points and creates a new function
        `f(float) -> float`. New function takes any arbitrary point as an input,
        and returning its corresponding value as an output.
    sampling_function_supplier_kwargs: dict, optional
        Kwargs passed to `sampling_function_supplier`.
    """

    def __init__(
        self,
        x,
        y,
        n,
        sampling_function_supplier=None,
        sampling_function_supplier_kwargs=None,
    ):
        super().__init__(x, y, n)
        self.sampling_function_supplier = sampling_function_supplier
        self.sampling_function_supplier_kwargs = (
            sampling_function_supplier_kwargs
            if sampling_function_supplier_kwargs is not None
            else {}
        )

    def oversample(self):
        function = self._get_sampling_function()
        xs, ys = self._initial_oversample()
        ys = [function(x) for x in xs]
        return xs, ys

    def _get_sampling_function(self):
        """Get sampling function.

        Returns sampling function that takes arbitrary point and returns
        its corresponding dependent value f(x).
        """
        if self.sampling_function_supplier:
            return self.sampling_function_supplier(
                self.x, self.y, **self.sampling_function_supplier_kwargs
            )
        else:
            raise ValueError("Sampling function not specified")


class CubicSplineOversample(FunctionOversample):
    r"""Oversample function using cubic spline between given points."""

    def __init__(
        self,
        x,
        y,
        n,
        sampling_function_supplier=lambda x, y: CubicSpline(x, y),
    ):
        super().__init__(x, y, n, sampling_function_supplier)


class IntervalOversample(AbstractOversample):
    r"""Abstraction for interval based oversampling classes."""
    pass


class LinearFixedOversample(AbstractOversample):
    r"""Linearly moves between points in fixed transition intervals.

    .. image:: /_static/gfx/linear_fixed_oversample.pdf

    Transition linearly between intervals in transition window (part of the interval).
    Transition window is defined in number of samples `a` and divided proportionally
    to the left and right side of the interval. If `a` is not specified, it is obtained
    based on the transition samples factor `alpha` multiplied by the number of inserted
    samples for each interval `n`. `a` cannot be lower, than 2 samples. If it is,
    it's value is changed to correct that.

    Parameters
    ----------
    x: 1-D array-like
        Independent variable in strictly increasing order.
    y: 1-D array-like
        Dependent variable.
    n: int
        Number of points oversampled and recreated in the function.
    alpha: float, default: 1.0
        Transition window samples factor for moving between intervals.
    a: int, optional
        Transition window samples for moving between intervals.
        If not specified, it is equal to `alpha` * `n`. Cannot be lower than 2.

    Notes
    -----
    Let us consider `k`-th interval and :math:`x_{k,i}`, :math:`y{k,i}`
    refer to `i`-th sample of `k`-th interval for `x` and `y`, respectively.
    When omitting value, e.g., :math:`x_{k}`, it refers to the `x_{k,0}`.

    Oversampling creates function :math:`z = g(x)` from :math:`y=f(x)`.

    Let assume, that:

    * the function is going to be oversampled with `n` samples in each interval.
    * :math:`\alpha` is a given transition window factor parameter.
    * :math:`z_{k}` is transition value between interval `k` and `k - 1`.
    * :math:`z_{k+1}` is transition value between interval `k` and `k + 1`.
    * :math:`y_{k}` is original function value in interval `k`.

    Left :math:`a_l` and right :math:`a_r` transition number of samples is calculated
    as:

    .. math::
        a = \alpha \cdot n \\
        a_l = a_r = a / 2

    :math:`z_k` is calculated as a linear combination between :math:`y_{k-1}` and `y_k`,
    proportionally to the distance between the :math:`x_{k-1,n-a_l}` and :math:`x_{k,
    a_r}`, i.e.,

    .. math::
        z_k = y_{k-1} + (y_k - y_{k-1}) \cdot (x_k - x_{k-1, n - a_r}) /
        (x_{k, a_l} - x_{k-1, n - a_r})

    Value for :math:`z_{k+1}` is calculated analogously.

    Based on found transition values, remaining points in function :math:`z = g(x)`
    are calculated as a linear combination of transition point and previous value.

    .. math::
        \begin{cases}
            z_{k, i} = \mbox{lin_fit}(x_{k, i}, (x_{k, 0}, z_{k, 0}), (x_{k, a_l},
            y_{k, 0})) &   i \in \{0, a_l - 1\} \\
            z_{k,i} = y_{k,i} & i \in \{a_l, n - a_r\} \\
            z_{k, i} = \mbox{lin_fit}(x_{k, i}, (x_{k, n - a_r}, y_{k,0}),
            (x_{k, n}, z_{k+1,0})) &  i \in \{n - a_r + 1, n\}
        \end{cases}

    where `linfit` linearly fits value based on two other points.

    See Also
    --------
    :func:`~traffic_weaver.funfit.lin_fit`
    """

    def __init__(self, x, y, n, alpha=1.0, a=None):
        super().__init__(x, y, n)
        if a is None:
            a = alpha * self.n
        self.a = int(a)
        if self.a < 2:
            self.a = 2
        self.a_l = int(self.a / 2)
        self.a_r = self.a_l

    def oversample(self):
        x, y = self._initial_oversample()
        n = self.n
        a_r = self.a_r
        a_l = self.a_l

        # result array
        z = np.array(y, copy=True)

        x = IntervalArray(x, n)
        y = IntervalArray(y, n)
        z = IntervalArray(y.array, n)

        # extend with one period on the left and one on the right to make
        # calculations easier
        x.extend_linspace(direction='both')
        y.extend_constant(direction='both')
        z.extend_constant(direction='both')

        # move through each interval
        for k in range(1, x.nr_of_full_intervals() - 1):
            # calculate transition points
            y_0 = y[k, 0]
            z_0 = lin_fit(
                x[k, 0],
                (x[k, -a_r], y[k - 1, 0]),
                (x[k, a_l], y[k, 0]),
            )
            z_1 = lin_fit(
                x[k + 1, 0],
                (x[k, n - a_r], y_0),
                (x[k + 1, a_l], y[k + 1, 0]),
            )

            for i in range(0, self.a_l):
                z[k, i] = lin_fit(x[k, i], (x[k, 0], z_0), (x[k, self.a_l], y_0))
            for i in range(n - self.a_r + 1, n + 1):
                z[k, i] = lin_fit(
                    x[k, i], (x[k, self.n - self.a_r], y_0), (x[k, self.n], z_1)
                )
        return x.array[n:-n], z.array[n:-n]


class LinearAdaptiveOversample(AbstractOversample):
    r"""Linearly moves between points in adaptive transition intervals.

    .. image:: /_static/gfx/linear_adaptive_oversample.pdf

    Transition linearly between intervals in transition window (part of the interval).
    Transition window is defined in number of samples `a` and divided according to the
    `adaptive_factor`. `adaptive_factor` is inversely proportionally to the change of
    function value on both edges of the interval, i.e., if function value has higher
    change on the right side of the interval, than on the left side, the right side
    transition window is smaller than the left one.

    The impact of the `adaptive_factor` can be decreased by adjusting `adaptive_smooth`.

    If `a` is not specified, it is obtained based on the transition samples factor
    `alpha` multiplied by the number of inserted samples for each interval `n`.
    `a` cannot be lower, than 2 samples. If it is, it's value is changed to correct
    that.

    Parameters
    ----------
    x: 1-D array-like
        Independent variable in strictly increasing order.
    y: 1-D array-like
        Dependent variable.
    n: int
        Number of points oversampled and recreated in the function.
    alpha: float, default: 1.0
        Transition window samples factor for moving between intervals.
    a: int, optional
        Transition window samples for moving between intervals.
        If not specified, it is equal to `alpha` * `n`. Cannot be lower than 2.
    adaptive_smooth: float, default: 1.0
        Decreasing impact of `adaptive_factor` by raising it to the power
        `1/adaptive_smooth`.


    Notes
    -----
    Let us consider `k`-th interval and :math:`x_{k,i}`, :math:`y{k,i}`
    refer to `i`-th sample of `k`-th interval for `x` and `y`, respectively.
    When omitting value, e.g., :math:`x_{k}`, it refers to the `x_{k,0}`.

    Oversampling creates function :math:`z = g(x)` from :math:`y=f(x)`.

    Let assume, that:

    * the function is going to be oversampled with `n` samples in each interval.
    * :math:`\alpha` is a given transition window factor parameter.
    * :math:`s` is a given `adaptive_smooth` parameter
    * :math:`z_{k}` is transition value between interval `k` and `k - 1`.
    * :math:`z_{k+1}` is transition value between interval `k` and `k + 1`.
    * :math:`y_{k}` is original function value in interval `k`.

    Transition ranges depend on the change in function value between intervals.

    1. When function changes between intervals, i.e., :math:`y_{k-1} \neq y_k \neq
    y_{k+1}`,
    an `adaptive_factor` :math:`\gamma_k` and left and right transition windows
    :math:`a_k,l` and :math:`a_k,r` are calculated, as:

    .. math::
        \gamma_k = \frac{|y_{1} - y_{0}|}{|y_{0} - y_{-1}|} ^ \frac{1/s} \\
        \frac{a_{k,l}}{a_{k,r}} = \gamma_k \\
        a_{k,l} = \min(\max(\frac{\gamma_k \cdot a}{1 + \gamma_k}, 1), a) \\
        a_{k,r} = \min(\max(\frac{a}{1 + \gamma_k}, 1), a)

    The transition values are kept between `1` and `n`, thus:

    .. math::
        a_{k,l} = \min(\max(a_{k,l}, 1) n) \\
        a_{k,r} = \min(\max(a_{k,r}, 1) n) \\

    2. If function value is left and right side constant, i.e.,  :math:`y_{k-1} = y_k
    = y_{k+1}`,
    transition windows are calculated as:

    .. math::
        a_{k, l} = a_{k, r} = 0

    3. If function value is changing only on right side of the interval, i.e.,
    :math:`y_{k-1} \neq y_k = y_{k+1}`,

    .. math::
        a_{k, l} = 0
        a_{k, r} = \frac{a}{2}

    4. If function value is changing only on left side of the interval, i.e.,
    :math:`y_{k-1} = y_k \neq y_{k+1}`,

    .. math::
        a_{k, l} = \frac{a}{2}
        a_{k, r} = 0

    Transition points and remaining points inside the interval are calculated same as
    in :func:`LinearFixedOversample`.

    .. math::
        \begin{cases}
            z_{k, i} = \mbox{lin_fit}(x_{k, i}, (x_{k, 0}, z_{k, 0}), (x_{k, a_{k,
            l}}, y_{k, 0})) &   i \in \{0, a_l - 1\} \\
            z_{k,i} = y_{k,i} & i \in \{a_{k,l}, n - a_r\} \\
            z_{k, i} = \mbox{lin_fit}(x_{k, i}, (x_{k, n - a_{k, r}}, y_{k, 0}),
            (x_{k, n}, z_{k+1,0}))
            &  i \in \{n - a_{k,r} + 1, n\}
        \end{cases}

    See Also
    --------
    :func:`LinearFixedOversample`
    """

    def __init__(self, x, y, n, alpha=1.0, a=None, adaptive_smooth=1.0):
        super().__init__(x, y, n)
        if a is None:
            a = alpha * self.n
        self.a = int(a)
        if self.a < 2:
            self.a = 2
        self.adaptive_smooth = adaptive_smooth

    @staticmethod
    def get_adaptive_transition_points(x, y, a, adaptive_smooth):
        """Calculate transition points

        Parameters
        ----------
        x: IntervalArray
            independent variable
        y: IntervalArray
            dependent variable
        a: int
            transition window in samples
        adaptive_smooth: float
            smoothing of adaptive_factor

        Returns
        -------
        list of floats
            Left transition window for each interval.
        list of floats
            Right transition window for each interval.
        list of floats
            Adaptive factor for each interval.
        """
        gammas = [None]
        a_ls = [1]
        a_rs = [1]
        for k in range(1, x.nr_of_full_intervals() - 1):
            nom = abs(y[k + 1, 0] - y[k, 0])
            denom = abs(y[k, 0] - y[k - 1, 0])
            if nom == 0 and denom == 0:
                a_ls.append(0)
                a_rs.append(0)
                gammas.append(None)
            elif nom == 0:  # left side interval is changing
                a_ls.append(int(a / 2))
                a_rs.append(0)
            elif denom == 0:  # right side interval is changing
                a_ls.append(0)
                a_rs.append(int(a / 2))
                gammas.append(None)
            else:
                gamma = nom / denom
                gamma = gamma**adaptive_smooth
                a_l = gamma * a / (1 + gamma)
                a_r = a / (1 + gamma)
                a_l = int(min(max(a_l, 1), a))
                a_r = int(min(max(a_r, 1), a))

                a_ls.append(a_l)
                a_rs.append(a_r)
                gammas.append(gamma)

        a_ls.extend([1])
        a_rs.extend([1])
        gammas.extend([None])
        return a_ls, a_rs, gammas

    def oversample(self):
        x, y = self._initial_oversample()
        n = self.n

        # result array
        z = np.array(y, copy=True)

        x = IntervalArray(x, n)
        y = IntervalArray(y, n)
        z = IntervalArray(y.array, n)

        # extend with one period on the left and one on the right to make
        # calculations easier
        x.extend_linspace(direction='both')
        y.extend_constant(direction='both')
        z.extend_constant(direction='both')

        a_ls, a_rs, gammas = self.get_adaptive_transition_points(
            x, y, self.a, self.adaptive_smooth
        )

        for k in range(1, x.nr_of_full_intervals() - 1):
            y_0 = y[k, 0]

            # find transition points
            if a_rs[k - 1] == 0 and a_ls[k] == 0:  # no left transition window
                z_0 = y[k - 1, 0]
            else:
                z_0 = lin_fit(
                    x[k, 0], (x[k, -a_rs[k - 1]], y[k - 1, 0]), (x[k, a_ls[k]], y[k, 0])
                )
            if a_rs[k] == 0 and a_ls[k + 1] == 0:  # no right transition window
                z_1 = y[k + 1]
            else:
                z_1 = lin_fit(
                    x[k + 1, 0],
                    (x[k, n - a_rs[k]], y_0),
                    (x[k + 1, a_ls[k + 1]], y[k + 1, 0]),
                )

            # fit remaining points
            for i in range(0, a_ls[k]):
                z[k, i] = lin_fit(x[k, i], (x[k, 0], z_0), (x[k, a_ls[k]], y_0))
            for i in range(n - a_rs[k] + 1, n + 1):
                z[k, i] = lin_fit(x[k, i], (x[k, n - a_rs[k]], y_0), (x[k, n], z_1))

        return x.array[n:-n], z.array[n:-n]


class ExpFixedOversample(AbstractOversample):
    r"""Moves between points in fixed transition intervals by combining linear and
    exponential function.

    .. image:: /_static/gfx/exp_fixed_oversample.pdf

    Transition combining linear and exponential function between intervals in
    transition window (part of the interval).
    Transition window is defined in number of samples `a` and divided proportionally
    to the left and right side of the interval.
    If `a` is not specified, it is obtained based on the transition samples factor
    `alpha` multiplied by the number of inserted samples for each interval `n`.
    `a` cannot be lower, than 2 samples. If it is, it's value is changed to correct
    that.

    Left and right transition window is further divided into linear only part and
    combination of
    linear and exponential one. Division is done according to parameter `beta` and
    linear transition window is calculated as `b = beta * a_l`.

    Parameters
    ----------
    x: 1-D array-like
        Independent variable in strictly increasing order.
    y: 1-D array-like
        Dependent variable.
    n: int
        Number of points oversampled and recreated in the function.
    alpha: float, default: 1.0
        Transition window samples factor for moving between intervals.
    beta: float, default: 0.5
        Linear transition window samples factor.
    a: int, optional
        Transition window samples for moving between intervals.
        If not specified, it is equal to `alpha` * `n`. Cannot be lower than 2.
    exp: float, default: 2.0
        Exponent in exponential transition function.

    Notes
    -----
    Let us consider `k`-th interval and :math:`x_{k,i}`, :math:`y{k,i}`
    refer to `i`-th sample of `k`-th interval for `x` and `y`, respectively.
    When omitting value, e.g., :math:`x_{k}`, it refers to the `x_{k,0}`.

    Oversampling creates function :math:`z = g(x)` from :math:`y=f(x)`.

    Let assume, that:
    * the function is going to be oversampled with `n` samples in each interval.
    * :math:`\alpha` is a given transition window factor parameter.
    * :math:`\beta` is a given linear part of transition window factor parameter.
    * :math:`z_{k}` is transition value between interval `k` and `k - 1`.
    * :math:`z_{k+1}` is transition value between interval `k` and `k + 1`.
    * :math:`y_{k}` is original function value in interval `k`.

    Left :math:`a_l` and right :math:`a_r` transition number of samples is calculated
    as:

    .. math::
        a = \alpha \cdot n \\
        a_l = a_r = a / 2

    Let :math:`b` denote  Linear part of transition window, and it is calculated as:

    .. math::
        b = \beta \cdot a_l

    Transition points are calculated the same as in :func:`LinearFixedOversample`.

    Based on found transition values, remaining points in function :math:`z = g(x)`
    are calculated
    as a linear combination of transition point and previous value using linear and
    exponential functions.

    Two additional transition points are calculated, corresponding to :math:`x_{k,
    b}` and :math:`x_{k, n - b}`
    denoted as `z_{k, b}` and `z_{k, n-b}`. They are calculated as linear combination
    between
    :math:`z_{k, 0}` and :math:`y_{k, 0}`, and :math:`z_{k+1, 0}` and :math:`y_{k,
    0}`, respectively.


    .. math::
        \begin{cases}
            z_{k, i} = \mbox{lin_fit}(x_{k, i}, (x_{k, 0}, z_{k, 0}), (x_{k, b},
            z_{k, b})) &   i \in \{0, b - 1\} \\
            z_{k, i} = \mbox{lin_exp_xy_fit}(x_{k, i}, (x_{k, b}, z_{k, b}), (x_{k,
            a_l}, y_{k, 0})) &   i \in \{b, a_l - 1\} \\
            z_{k,i} = y_{k,i} & i \in \{a_l, n - a_r\} \\
            z_{k, i} = \mbox{exp_lin_fit}(x_{k, i}, (x_{k, n - a_r}, y_{k, 0}),
            (x_{k, n -b}, z_{k+1,n-b}))
                &  i \in \{n - a_r + 1, n - b\} \\
            z_{k, i} = \mbox{lin_fit}(x_{k, i}, (x_{k, n - b}, y_{k, n - b}), (x_{k,
            n}, z_{k+1,0}))
                &  i \in \{n - b + 1, n\}
        \end{cases}

    where `linfit` linearly fits value based on two other points; `lin_exp_xy_fit`
    gradually fits combination of linear
    function and exponential function scaled from (0, 1) range and mirrored over y=x
    line;
    `exp_lin_fit` gradually fits combination of exponential function scaled from
    `(0, 1)` range and linear function.

    See Also
    --------
    :func:`LinearFixedOversample`
    :func:`~traffic_weaver.funfit.lin_fit`
    :func:`~traffic_weaver.funfit.lin_exp_xy_fit`
    :func:`~traffic_weaver.funfit.exp_lin_fit`
    """

    def __init__(self, x, y, n, alpha=1.0, beta=0.5, a=None, exp=2.0):
        super().__init__(x, y, n)
        if a is None:
            a = alpha * self.n
        self.a = int(a)
        if self.a < 2:
            self.a = 2
        self.a_l = int(self.a / 2)
        self.a_r = self.a_l
        self.b = int(beta * self.a_l)
        self.exp = exp

    def oversample(self):
        x, y = self._initial_oversample()
        n = self.n
        a_r = self.a_r
        a_l = self.a_l
        b = self.b
        exp = self.exp

        # result array
        z = np.array(y, copy=True)

        x = IntervalArray(x, n)
        y = IntervalArray(y, n)
        z = IntervalArray(y.array, n)

        # extend with one period on the left and one on the right to make
        # calculations easier
        x.extend_linspace(direction='both')
        y.extend_constant(direction='both')
        z.extend_constant(direction='both')

        # move through each interval
        for k in range(1, x.nr_of_full_intervals() - 1):
            # calculate transition points
            y_0 = y[k, 0]
            z_0 = lin_fit(x[k, 0], (x[k, -a_r], y[k - 1, 0]), (x[k, a_l], y[k, 0]))
            z_1 = lin_fit(
                x[k + 1, 0], (x[k, n - a_r], y_0), (x[k + 1, a_l], y[k + 1, 0])
            )

            z_0_lb = lin_fit(x[k, 0 + b], (x[k, 0], z_0), (x[k, a_l], y[k, 0]))

            z_0_rb = lin_fit(x[k, n - b], (x[k, n - a_r], y[k, 0]), (x[k + 1, 0], z_1))

            # calculate remaining points
            for i in range(0, b):
                z[k, i] = lin_fit(x[k, i], (x[k, 0], z_0), (x[k, b], z_0_lb))
            for i in range(b, a_l):
                z[k, i] = lin_exp_xy_fit(
                    x[k, i],
                    (x[k, b], z_0_lb),
                    (x[k, a_l], y_0),
                    alpha=exp,
                )

            for i in range(n - a_r, n - b):
                z[k, i] = exp_lin_fit(
                    x[k, i],
                    (x[k, n - a_r], y_0),
                    (x[k, n - b], z_0_rb),
                    alpha=exp,
                )
            for i in range(n - b, n):
                z[k, i] = lin_fit(x[k, i], (x[k, n - b], z_0_rb), (x[k, n], z_1))

        return x.array[n:-n], z.array[n:-n]


class ExpAdaptiveOversample(AbstractOversample):
    r"""Moves between points in adaptive transition intervals by combining linear and
    exponential function.

    .. image:: /_static/gfx/exp_adaptive_oversample.pdf

    Transition combining linear and exponential function between intervals in
    transition window (part of the interval).
    Transition window is defined in number of samples `a` and divided according to the
    `adaptive_factor`. `adaptive_factor` is inversely proportionally to the change of
    function
    value on both edges of the interval, i.e., if function value has higher change on
    the
    right side of the interval, than on the left side,
    the right side transition window is smaller than the left one.

    The impact of the `adaptive_factor` can be decreased by adjusting `adaptive_smooth`.

    If `a` is not specified, it is obtained based on the transition samples factor
    `alpha`
    multiplied by the number of inserted samples for each interval `n`.
    `a` cannot be lower, than 2 samples. If it is, it's value is changed to correct
    that.

    Left and right transition window is further divided into linear only part and
    combination of
    linear and exponential one. Division is done according to parameter `beta` and
    linear transition window is calculated as `b = beta * a_l`.

    Parameters
    ----------
    x: 1-D array-like
        Independent variable in strictly increasing order.
    y: 1-D array-like
        Dependent variable.
    n: int
        Number of points oversampled and recreated in the function.
    alpha: float, default: 1.0
        Transition window samples factor for moving between intervals.
    beta: float, default: 0.5
        Linear transition window samples factor.
    a: int, optional
        Transition window samples for moving between intervals.
        If not specified, it is equal to `alpha` * `n`. Cannot be lower than 2.
    adaptive_smooth: float, default: 1.0
        Decreasing impact of `adaptive_factor` by raising it to the power
        `1/adaptive_smooth`.
    exp: float, default: 2.0
        Exponent in exponential transition function.

    Notes
    -----
    This class combines functionality of :func:`LinearAdaptiveOversample` to
    calculate adaptive transition
    window, and :func:`ExpFixedOversample` to combine both linear and exponential
    function to change
    between intervals.

    In particular, for each interval corresponding number of transition samples is
    calculated, respectively,
    and they are denoted as: :math:`a_{k, l}`, :math:`a_{k, r}`, :math:`b_{k, l}`,
    and :math:`b_{k, r}`.


    Based on found transition values, remaining points in function :math:`z = g(x)`
    are calculated
    as a linear combination of transition point and previous value using linear and
    exponential functions.

    Two additional transition points are calculated, corresponding to :math:`x_{k,
    b}` and :math:`x_{k, n - b}`
    denoted as `z_{k, b}` and `z_{k, n-b}`. They are calculated as linear combination
    between
    :math:`z_{k, 0}` and :math:`y_{k, 0}`, and :math:`z_{k+1, 0}` and :math:`y_{k,
    0}`, respectively.

    Then the points in interval are calculated as:

    .. math::
        \begin{cases}
            z_{k, i} = \mbox{lin_fit}(x_{k, i}, (x_{k, 0}, z_{k, 0}), (x_{k, b_{k,
            l}}, z_{k, b_{k, l}})) &   i \in \{0, b_{k, l} - 1\} \\
            z_{k, i} = \mbox{lin_exp_xy_fit}(x_{k, i}, (x_{k, b_{k, l}}, z_{k, b_{k,
            l}}), (x_{k, a_{k, l}}, y_{k, 0})) &   i \in \{b_{k, l}, a_{k, l} - 1\} \\
            z_{k,i} = y_{k,i} & i \in \{a_{k, l}, n - a_{k, r}\} \\
            z_{k, i} = \mbox{exp_lin_fit}(x_{k, i}, (x_{k, n - a_{k, r}}, y_{k, 0}),
            (x_{k, n - b_{k, r}}, z_{k+1,n-b_{k,r}}))
                &  i \in \{n - a_{k, r} + 1, n - b_{k,r}\} \\
            z_{k, i} = \mbox{lin_fit}(x_{k, i}, (x_{k, n - b_{k,r}}, y_{k, n - b_{k,
            r}}), (x_{k, n}, z_{k+1,0}))
                &  i \in \{n - b_{k,r} + 1, n\}
        \end{cases}

    where `linfit` linearly fits value based on two other points; `lin_exp_xy_fit`
    gradually fits combination of linear
    function and exponential function scaled from (0, 1) range and mirrored over y=x
    line;
    `exp_lin_fit` gradually fits combination of exponential function scaled from (0,
    1) range and linear function.

    See Also
    --------
    :func:`LinearFixedOversample`
    :func:`~traffic_weaver.funfit.lin_fit`
    :func:`~traffic_weaver.funfit.lin_exp_xy_fit`
    :func:`~traffic_weaver.funfit.exp_lin_fit`

    """

    def __init__(
        self, x, y, n, alpha=1.0, beta=0.5, a=None, adaptive_smooth=1.0, exp=2.0
    ):
        super().__init__(x, y, n)
        if a is None:
            a = alpha * self.n
        self.a = int(a)
        if self.a < 2:
            self.a = 2
        self.beta = beta
        self.adaptive_smooth = adaptive_smooth
        self.exp = exp

    def oversample(self):
        x, y = self._initial_oversample()
        n = self.n
        beta = self.beta
        exp = self.exp

        # result array
        z = np.array(y, copy=True)

        x = IntervalArray(x, n)
        y = IntervalArray(y, n)
        z = IntervalArray(y.array, n)

        # extend with one period on the left and one on the right to make
        # calculations easier
        x.extend_linspace(direction='both')
        y.extend_constant(direction='both')
        z.extend_constant(direction='both')

        # get adaptive factors
        a_ls, a_rs, gammas = LinearAdaptiveOversample.get_adaptive_transition_points(
            x, y, self.a, self.adaptive_smooth
        )
        b_ls = [int(beta * a_l) for a_l in a_ls]
        b_rs = [int(beta * a_r) for a_r in a_rs]

        # move through each interval
        for k in range(1, x.nr_of_full_intervals() - 1):
            # calculate transition points
            y_0 = y[k, 0]

            if a_rs[k - 1] == 0 and a_ls[k] == 0:  # no left transition window
                z_0 = y[k - 1, 0]
            else:
                z_0 = lin_fit(
                    x[k, 0], (x[k, -a_rs[k - 1]], y[k - 1, 0]), (x[k, a_ls[k]], y[k, 0])
                )
            if a_rs[k] == 0 and a_ls[k + 1] == 0:  # no right transition window
                z_1 = y[k + 1]
            else:
                z_1 = lin_fit(
                    x[k + 1, 0],
                    (x[k, n - a_rs[k]], y_0),
                    (x[k + 1, a_ls[k + 1]], y[k + 1, 0]),
                )

            if b_ls[k] == 0:  # no left linear transition window
                z_0_bl = z_0
            else:
                z_0_bl = lin_fit(
                    x[k, 0 + b_ls[k]], (x[k, 0], z_0), (x[k, a_ls[k]], y[k, 0])
                )

            if b_rs[k] == 0:  # no right linear transition window
                z_0_br = z_1
            else:
                z_0_br = lin_fit(
                    x[k, n - b_rs[k]], (x[k, n - a_rs[k]], y[k, 0]), (x[k + 1, 0], z_1)
                )

            # remaining points
            for i in range(0, b_ls[k]):
                z[k, i] = lin_fit(x[k, i], (x[k, 0], z_0), (x[k, b_ls[k]], z_0_bl))
            for i in range(b_ls[k], a_ls[k]):
                z[k, i] = lin_exp_xy_fit(
                    x[k, i],
                    (x[k, b_ls[k]], z_0_bl),
                    (x[k, a_ls[k]], y_0),
                    alpha=exp,
                )

            for i in range(n - a_rs[k], n - b_rs[k]):
                z[k, i] = exp_lin_fit(
                    x[k, i],
                    (x[k, n - a_rs[k]], y_0),
                    (x[k, n - b_rs[k]], z_0_br),
                    alpha=exp,
                )
            for i in range(n - b_rs[k], n):
                z[k, i] = lin_fit(x[k, i], (x[k, n - b_rs[k]], z_0_br), (x[k, n], z_1))

        return x.array[n:-n], z.array[n:-n]
