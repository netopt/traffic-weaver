import numpy as np

from .match import integral_matching_reference_stretch
from .oversample import AbstractOversample, ExpAdaptiveOversample
from .process import repeat, trend, spline_smooth, noise_gauss


class Weaver:
    r"""Interface for recreating time series.

    Parameters
    ----------
    x: 1-D array-like of size n, optional
        Independent variable in strictly increasing order.
    y: 1-D array-like of size n
        Dependent variable.

    Examples
    --------
    >>> from traffic_weaver import Weaver
    >>> from traffic_weaver.array_utils import append_one_sample
    >>> from traffic_weaver.datasets import load_mobile_video
    >>> x, y = load_mobile_video()
    >>> x, y = append_one_sample(x, y, make_periodic=True)
    >>> wv = Weaver(x, y)
    >>> # chain some command
    >>> _ = wv.oversample(10).integral_match().smooth(s=0.2)
    >>> # at any moment get newly created and processed time series' points
    >>> res_x, res_y = wv.get()
    >>> # chain some other commands
    >>> _ = wv.trend(lambda x: 0.5 * x).noise(40)
    >>> # either get created points
    >>> res_x, res_y = wv.get()
    >>> # or get them as spline to sample at any arbitrary point
    >>> f = wv.to_function()
    >>> # to sample at, e.g., x=0.5, do
    >>> _ = f(0.5)

    """

    def __init__(self, x, y):
        if x is None:
            self.x = np.arange(stop=len(y))
        else:
            self.x = np.asarray(x)
        self.y = np.asarray(y)

        self.original_x = self.x
        self.original_y = self.y

    def get(self):
        r"""Return function x,y tuple after performed processing."""
        return self.x, self.y

    def get_original(self):
        r"""Return the original function x,y tuple provided for the class."""
        return self.original_x, self.original_y

    def restore_original(self):
        r"""Restore original function passed before processing."""
        self.x = self.original_x
        self.y = self.original_y
        return self

    def oversample(
        self,
        n: int,
        oversample_class: type[AbstractOversample] = ExpAdaptiveOversample,
        **kwargs,
    ):
        r"""Oversample function using provided strategy.

        Parameters
        ----------
        n: int
            Number of samples between each point.
        oversample_class: subclass of AbstractOversample
            Oversample strategy.
        **kwargs
            Additional parameters passed to `oversample_class`.

        Returns
        -------
        self

        See Also
        --------
        :func:`~traffic_weaver.oversample.AbstractOversample`
        """
        self.x, self.y = oversample_class(self.x, self.y, n, **kwargs).oversample()
        return self

    def integral_match(self, **kwargs):
        r"""Match function integral to piecewise constant approximated integral of the
        original function.

        Parameters
        ----------
        **kwargs
            Additional parameters passed to integral matching function.

        Returns
        -------
        self

        See Also
        --------
        :func:`~traffic_weaver.match.integral_matching_reference_stretch`
        """
        self.y = integral_matching_reference_stretch(
            self.x, self.y, self.original_x, self.original_y, **kwargs
        )
        return self

    def noise(self, snr, **kwargs):
        r"""Add noise to function.

        Parameters
        ----------
        snr: scalar or array-like
            Target signal-to-noise ratio for a function.
        **kwargs
            Parameters passed to noise creation.

        Returns
        -------
        self

        See Also
        --------
        :func:`~traffic_weaver.process.noise_gauss`
        """

        self.y = noise_gauss(self.y, snr=snr, **kwargs)
        return self

    def repeat(self, n):
        r"""Repeat function.

        Parameters
        ----------
        n: scalar
            Number of repetitions.

        Returns
        -------
        self

        See Also
        --------
        :func:`~traffic_weaver.process.repeat`
        """
        self.x, self.y = repeat(self.x, self.y, repeats=n)
        return self

    def trend(self, trend_func: lambda x: x):
        r"""Apply trend to function.

        Parameters
        ----------
        trend_func: Callable
            Shift value for dependent variable based on value of independent variable
            normalized to `(0, 1)` range.

        Returns
        -------
        self

        See Also
        --------
        :func:`~traffic_weaver.process.trend`
        """
        self.x, self.y = trend(self.x, self.y, fun=trend_func)
        return self

    def smooth(self, s):
        r"""Smoothen the function.

        Parameters
        ----------
        s: float
            Smoothing parameter.

        Returns
        -------
        self

        See Also
        --------
        :func:`~traffic_weaver.process.spline_smooth`
        """
        self.y = spline_smooth(self.x, self.y, s=s)(self.x)
        return self

    def to_function(self, s=0):
        r"""Create spline function.

        Allows for sampling function at any point.

        Parameters
        ----------
        s: float
            Smoothing parameter

        Returns
        -------
        Callable
            Function that returns function value for any input point.

        See Also
        --------
        :func:`~traffic_weaver.process.spline_smooth`
        """
        return spline_smooth(self.x, self.y, s=s)
