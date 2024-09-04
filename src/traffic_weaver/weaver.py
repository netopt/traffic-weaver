import numpy as np

from .array_utils import append_one_sample
from .match import integral_matching_reference_stretch
from .oversample import AbstractOversample, ExpAdaptiveOversample
from .process import repeat, trend, spline_smooth, noise_gauss


class Weaver:
    r"""Interface for recreating time series.

    Parameters
    ----------
    x: 1-D array-like of size n, optional
        Independent variable in strictly increasing order.
        If x is None, then x is a set of integers from 0 to `len(y) - 1`
    y: 1-D array-like of size n
        Dependent variable.

    Raises:
    -------
    ValueError
        If `x` and `y` are not of the same length.

    Examples
    --------
    >>> from traffic_weaver import Weaver
    >>> from traffic_weaver.array_utils import append_one_sample
    >>> from traffic_weaver.datasets import load_sandvine_mobile_video
    >>> data = load_sandvine_mobile_video()
    >>> x, y = data.T
    >>> wv = Weaver(x, y)
    >>> _ = wv.append_one_sample(make_periodic=True)
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
        if x is not None and len(x) != len(y):
            raise ValueError("x and y should be of the same length")
        if x is None:
            self.x = np.arange(stop=len(y))
        else:
            self.x = np.asarray(x)
        self.y = np.asarray(y)

        self.original_x = self.x
        self.original_y = self.y

        self.x_scale = 1
        self.y_scale = 1

    @staticmethod
    def from_2d_array(xy: np.ndarray):
        """Create Weaver object from 2D array.

        Parameters
        ----------
        xy: np.ndarray of shape (nr_of_samples, 2)
            2D array with each row representing one point in time series.
            The first column is the x-variable and the second column is the y-variable.

        Returns
        -------
        Weaver
            Weaver object with x and y values from 2D array.

        Raises
        ------
        ValueError
            If `xy` is not a 2D array or does not have 2 columns

        """
        shape = xy.shape
        if len(shape) != 2 or shape[1] != 2:
            raise ValueError("xy should be 2D array with 2 columns")
        return Weaver(xy[:, 0], xy[:, 1])

    @staticmethod
    def from_dataframe(df, x_col=0, y_col=1):
        """Create Weaver object from DataFrame.

        Parameters
        ----------
        df: pandas DataFrame
            DataFrame with data.
        x_col: int or str, default=0
            Name of column with x values.
        y_col: int or str, default=1
            Name of column with y values.

        Returns
        -------
        Weaver
            Weaver object with x and y values from DataFrame.

        """
        return Weaver(df[x_col].values, df[y_col].values)

    @staticmethod
    def from_csv(file_name: str):
        """Create Weaver object from CSV file.

        CSV has to contain two columns without headers.
        The first column contains 'x' values,
        the second column contains 'y' values.

        Parameters
        ----------
        file_name: str
            Path to CSV file.
        Returns
        -------
        Weaver
            Weaver object from CSV file.
        """
        return Weaver.from_2d_array(np.loadtxt(file_name, delimiter=',', dtype=np.float64))

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

    def append_one_sample(self, make_periodic=False):
        """Add one sample to the end of time series.

        Add one sample to `x` and `y` array. Newly added point `x_i` point is distant from
        the last point of `x` same as the last from the one before the last point.
        If `make_periodic` is False, newly added `y_i` point is the same as the last  point
        of `y`. If `make_periodic` is True, newly added point is the same as the first point
        of `y`.

        Parameters
        ----------
        make_periodic: bool, default: False
            If false, append the last `y` point to `y` array.
            If true, append the first `y` point to `y` array.

        Returns
        -------
        self

        See Also
        --------
        :func:`~traffic_weaver.array_utils.append_one_sample`
        """
        self.x, self.y = append_one_sample(self.x, self.y, make_periodic=make_periodic)
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
            self.x, self.y, self.original_x * self.x_scale, self.original_y * self.y_scale, **kwargs
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

    def scale_x(self, scale):
        r"""Scale x-axis."""
        self.x_scale = self.x_scale * scale
        self.x = self.x * scale
        return self

    def scale_y(self, scale):
        r"""Scale y-axis."""
        self.y_scale = self.y_scale * scale
        self.y = self.y * scale
        return self
