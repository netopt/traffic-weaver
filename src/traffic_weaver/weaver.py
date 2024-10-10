import numpy as np

from .match import integral_matching_reference_stretch
from .process import repeat, trend, spline_smooth, noise_gauss, interpolate, truncate, normalize
from .rfa import AbstractRFA, ExpAdaptiveRFA
from .sorted_array_utils import append_one_sample


class Weaver:
    r"""Interface for recreating time series.

    Parameters
    ----------
    x: 1-D array-like of size n, optional
        Independent variable in strictly increasing order.
        If x is None, then x is a set of integers from 0 to `len(y) - 1`
    y: 1-D array-like of size n
        Dependent variable.

    Raises
    ------
    ValueError
        If `x` and `y` are not of the same length.

    Notes
    -----
    `x` and `y` fields corresponds to processed time series.
    `original_x` and `original_y` fields corresponds to originally passed values.
    `reference_x` and `reference_y` fields corresponds to processed fields used as a reference
    for integral matching.

    Examples
    --------
    Minimal processing example:

    >>> from traffic_weaver import Weaver
    >>> from traffic_weaver.datasets import load_dataset
    >>> data = load_dataset('sandvine_mobile_video')
    >>> x, y = data.T
    >>> wv = Weaver(x, y)
    >>> _ = wv.append_one_sample(make_periodic=True)
    >>> # chain some command
    >>> _ = wv.recreate_from_average(10).integral_match().smooth(s=0.2)
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

    Loading from user defined values

    >>> import numpy as np
    >>> from traffic_weaver import Weaver
    >>> x = np.linspace(5, 15, 11)
    >>> y = 2 * x
    >>> wv = Weaver(x, y)

    """
    def __init__(self, x, y):
        if x is not None and len(x) != len(y):
            raise ValueError("x and y should be of the same length")
        if x is None:
            self.x = np.arange(stop=len(y))
        else:
            self.x = np.asarray(x)
        self.y = np.asarray(y)

        self.original_x = self.x.copy()
        self.original_y = self.y.copy()
        self.reference_x = self.x.copy()
        self.reference_y = self.y.copy()

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

        Examples
        --------
        >>> # loading from dataset
        >>> import numpy as np
        >>> from traffic_weaver import Weaver
        >>> from traffic_weaver.datasets import load_dataset
        >>> wv = Weaver.from_2d_array(load_dataset('sandvine_mobile_video'))
        >>> # loading from user specified 2D array
        >>> wv = Weaver.from_2d_array(np.array([[5, 10], [6, 12], [7, 14]]))

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

        Examples
        --------
        >>> # loading from Pandas dataframe
        >>> import pandas as pd
        >>> df = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [10, 20, 30, 40]})
        >>> from traffic_weaver import Weaver
        >>> wv = Weaver.from_dataframe(df, x_col='x', y_col='y')
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
        r"""Return function x, y tuple after performed processing.

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.shift_x(10).shift_y(10).get()
        >>> res_x
        array([15., 16., 17., 18., 19., 20., 21., 22., 23., 24., 25.])
        >>> res_y
        array([20., 22., 24., 26., 28., 30., 32., 34., 36., 38., 40.])

        """
        return self.x, self.y

    def get_original(self):
        r"""Return the original function x, y tuple provided for the class.

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.shift_x(10).shift_y(10).get_original()
        >>> res_x
        array([ 5.,  6.,  7.,  8.,  9., 10., 11., 12., 13., 14., 15.])
        >>> res_y
        array([10., 12., 14., 16., 18., 20., 22., 24., 26., 28., 30.])

        """
        return self.original_x, self.original_y

    def get_reference(self):
        r"""Return the reference function x,y tuple.

        Reference function is used to calculate integral match.
        Shifting, truncating, normalizing and scaling are operations that are tracked by the reference function
        while applying them to the target function.
        """
        return self.reference_x, self.reference_y

    def restore_original(self):
        r"""Restore original function passed before processing.

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.shift_x(10).shift_y(10).restore_original().get()
        >>> np.all(res_x == x).item()
        True
        >>> np.all(res_y == y).item()
        True

        """
        self.x = self.original_x.copy()
        self.y = self.original_y.copy()
        return self

    def append_one_sample(self, make_periodic=False):
        """Add one sample to the end of time series.

        Add one sample to `x` and `y` array. Newly added point `x_i` point is distant
        from
        the last point of `x` same as the last from the one before the last point.
        If `make_periodic` is False, newly added `y_i` point is the same as the last
        point
        of `y`. If `make_periodic` is True, newly added point is the same as the
        first point
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
        :func:`~traffic_weaver.sorted_array_utils.append_one_sample`

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> wv = wv.append_one_sample(make_periodic=True)
        >>> res_x, res_y = wv.get()
        >>> res_x[-1].item() == (2 * x[-1] - x[-2]).item()
        True
        >>> y[0].item() == res_y[-1].item()
        True

        """
        self.x, self.y = append_one_sample(self.x, self.y, make_periodic=make_periodic)
        self.reference_x, self.reference_y = append_one_sample(self.reference_x, self.reference_y,
                                                               make_periodic=make_periodic)
        return self

    def slice_by_index(self, start=0, stop=None, step=1):
        """Get view of function sliced by index.

        Parameters
        ----------
        start: int, default: 0
            Start index of the slice.
        stop: int, default: None
            Stop index of the slice, exclusive. If None, then it is equal to the length of the time series.
        step: int, default: 1
            Step of the slice.

        Returns
        -------
        ndarray, ndarray
            Sliced view of x, y variables.

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> x_res, y_res = wv.slice_by_index(1, 5)
        >>> x_res
        array([6., 7., 8., 9.])
        >>> y_res
        array([12., 14., 16., 18.])

        """
        if stop is None:
            stop = len(self.x)
        if start < 0:
            raise ValueError("Start index should be non-negative")
        if stop > len(self.x):
            raise ValueError("Stop index should be less than length of x")
        return self.x[start:stop:step], self.y[start:stop:step]

    def slice_by_value(self, start=None, stop=None, step=1):
        """Get view of function sliced by its value.

        Parameters
        ----------
        start: float, default: None
            Start value of the slice. If None, then it is equal to the first element of the time series.
        stop: float, default: None
            Stop value of the slice, inclusive. If None, then it is equal to the last element of the time series.
        step: int, default: 1
            Step of the slice.

        Returns
        -------
        ndarray, ndarray
            Sliced view of x, y variables.

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> x_res, y_res = wv.slice_by_value(7, 8)
        >>> x_res
        array([7., 8.])
        >>> y_res
        array([14., 16.])

        """
        if start is None:
            start_idx = 0
        else:
            start_idx = np.where(self.x == start)[0][0]
        if stop is None:
            stop_idx = len(self.x)
        else:
            stop_idx = np.where(self.x == stop)[0][0] + 1
        if not start_idx:
            raise ValueError("Start value not found in x")
        if not stop_idx:
            raise ValueError("Stop value not found in x")
        return self.slice_by_index(start_idx, stop_idx, step)

    def interpolate(self, n: int = None, new_x=None, method='linear', **kwargs):
        """ Interpolate function.

        For original time varying function sampled at different points use one of the
        'linear', 'cubic' or 'spline' interpolation methods.

        For time varying function that is an averaged function over periods of time,
        use 'constant' interpolation method.

        Parameters
        ----------
        n: int
            Number of fixed space samples in new function.
            Ignored if `new_x` specified.
        new_x: array-like
            Points to where to evaluate interpolated function.
            It overrides 'n' parameter. Range should be the same as original x.
        method: str, default='linear'
            Interpolation strategy. Supported strategies are 'linear',
            'constant', 'cubic' and 'spline'.
        kwargs:
            Additional parameters passed to interpolation function.
            For more details see

        Returns
        -------
        self

        See Also
        --------
        :func:`~traffic_weaver.process.interpolate`

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.interpolate(new_x=np.linspace(5, 15, 26), method='linear').get()
        >>> res_x
        array([ 5. ,  5.4,  5.8,  6.2,  6.6,  7. ,  7.4,  7.8,  8.2,  8.6,  9. ,
                9.4,  9.8, 10.2, 10.6, 11. , 11.4, 11.8, 12.2, 12.6, 13. , 13.4,
               13.8, 14.2, 14.6, 15. ])
        >>> res_y
        array([10. , 10.8, 11.6, 12.4, 13.2, 14. , 14.8, 15.6, 16.4, 17.2, 18. ,
               18.8, 19.6, 20.4, 21.2, 22. , 22.8, 23.6, 24.4, 25.2, 26. , 26.8,
               27.6, 28.4, 29.2, 30. ])


        """
        if new_x is None and n is None:
            raise ValueError("Either n or new_x should be provided")
        if new_x is None:
            new_x = np.linspace(self.x[0], self.x[-1], n)
        else:
            if new_x[0] != self.x[0] or new_x[-1] != self.x[-1]:
                raise ValueError("new_x should have the same range as x")
        self.y = interpolate(self.x, self.y, new_x, method=method, **kwargs)
        self.x = new_x
        return self

    def recreate_from_average(self, n: int, rfa_class: type[AbstractRFA] = ExpAdaptiveRFA, **kwargs, ):
        r"""Recreate function from average function using provided strategy.

        Parameters
        ----------
        n: int
            Number of samples between each point.
        rfa_class: subclass of AbstractRFA
            Recreate from average strategy.
        **kwargs
            Additional parameters passed to `rfa_class`.

        Returns
        -------
        self

        See Also
        --------
        :func:`~traffic_weaver.rfa.AbstractRFA`

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.rfa import LinearFixedRFA
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.recreate_from_average(5, rfa_class=LinearFixedRFA, alpha=0.8).get()
        >>> res_x
        array([ 5. ,  5.2,  5.4,  5.6,  5.8,  6. ,  6.2,  6.4,  6.6,  6.8,  7. ,
                7.2,  7.4,  7.6,  7.8,  8. ,  8.2,  8.4,  8.6,  8.8,  9. ,  9.2,
                9.4,  9.6,  9.8, 10. , 10.2, 10.4, 10.6, 10.8, 11. , 11.2, 11.4,
               11.6, 11.8, 12. , 12.2, 12.4, 12.6, 12.8, 13. , 13.2, 13.4, 13.6,
               13.8, 14. , 14.2, 14.4, 14.6, 14.8, 15. ])
        >>> res_y
        array([10. , 10. , 10. , 10. , 10.5, 11. , 11.5, 12. , 12. , 12.5, 13. ,
               13.5, 14. , 14. , 14.5, 15. , 15.5, 16. , 16. , 16.5, 17. , 17.5,
               18. , 18. , 18.5, 19. , 19.5, 20. , 20. , 20.5, 21. , 21.5, 22. ,
               22. , 22.5, 23. , 23.5, 24. , 24. , 24.5, 25. , 25.5, 26. , 26. ,
               26.5, 27. , 27.5, 28. , 28. , 28.5, 29. ])

        """
        self.x, self.y = rfa_class(self.x, self.y, n, **kwargs).rfa()
        return self

    def integral_match(self, target_function_integral_method='trapezoid',
                       reference_function_integral_method='rectangle', **kwargs):
        r"""Match function integral to approximated integral of the original function.

        For original time varying function sampled at different points use
        `reference_function_integral_method='trapezoid'`.


        For original time varying function that is an averaged function over periods of time
        use `reference_function_integral_method='rectangular'`.

        Parameters
        ----------
        target_function_integral_method: str, default: 'trapezoid'
            Method to calculate integral of recreated function.
            Available options: 'trapezoid', 'rectangle'
        reference_function_integral_method: str, default: 'rectangle'
            Method to calculate integral of origianl function.
            Available options: 'trapezoid', 'rectangle'
        **kwargs
            Additional parameters passed to integral matching function.

        Returns
        -------
        self

        See Also
        --------
        :func:`~traffic_weaver.match.integral_matching_reference_stretch`

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.recreate_from_average(10).integral_match().get()

        """
        self.y = integral_matching_reference_stretch(self.x, self.y, self.reference_x, self.reference_y,
                                                     target_function_integral_method=target_function_integral_method,
                                                     reference_function_integral_method=reference_function_integral_method,  # noqa: E501
                                                     **kwargs)
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

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.noise(10).get()

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

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.repeat(2).get()
        >>> res_x
        array([ 5.,  6.,  7.,  8.,  9., 10., 11., 12., 13., 14., 15., 16., 17.,
               18., 19., 20., 21., 22., 23., 24., 25., 26.])
        >>> res_y
        array([10., 12., 14., 16., 18., 20., 22., 24., 26., 28., 30., 10., 12.,
               14., 16., 18., 20., 22., 24., 26., 28., 30.])

        """
        self.x, self.y = repeat(self.x, self.y, repeats=n)
        self.reference_x, self.reference_y = repeat(self.reference_x, self.reference_y, repeats=n)
        return self

    def trend(self, trend_func: lambda x: x, normalized=False):
        r"""Apply trend to function.

        Parameters
        ----------
        trend_func: Callable
            Long term trend applied to the data in form of a function.
            Callable signature is `(x) -> y_shift` where
            `x` independent variable axis and
            `y_shift` is independent variable shift for that `x`.
        normalized: bool, default: False
                If true, `x` variable in `fun` is normalized to the range of [0, 1].

        Returns
        -------
        self

        See Also
        --------
        :func:`~traffic_weaver.process.trend`

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> # apply trend f(y) = 1/5 x
        >>> res_x, res_y = wv.trend(lambda x: 1 / 5 * x).get()
        >>> res_y
        array([11. , 13.2, 15.4, 17.6, 19.8, 22. , 24.2, 26.4, 28.6, 30.8, 33. ])
        >>> # apply same trend with normalization to [0, 1] range
        >>> _ = wv.restore_original()
        >>> res_x, res_y = wv.trend(lambda x: 2 * x, normalized=True).get()
        >>> res_y
        array([11. , 13.2, 15.4, 17.6, 19.8, 22. , 24.2, 26.4, 28.6, 30.8, 33. ])

        """
        self.x, self.y = trend(self.x, self.y, fun=trend_func, normalized=normalized)
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

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = np.concatenate([np.linspace(5, 10, 6), np.linspace(9, 5, 5)])
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.smooth(1.0).get()
        >>> res_y
        array([4.80997905, 6.07830526, 7.27209891, 8.27226261, 8.95969893,
               9.21531047, 8.95969893, 8.27226261, 7.27209891, 6.07830526,
               4.80997905])
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

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> f = wv.to_function(1.0)
        >>> f([6.12, 7.44])
        array([12.24, 14.88])

        >>> y = np.concatenate([np.linspace(5, 10, 6), np.linspace(9, 5, 5)])
        >>> wv = Weaver(x, y)
        >>> f = wv.to_function(1.0)
        >>> f(7.0)
        array(7.27209891)

        """
        return spline_smooth(self.x, self.y, s=s)

    def to_2d_array(self):
        """Return time series as 2D array.

        Returns
        -------
        xy: np.ndarray of shape (nr_of_samples, 2)
            2D array with each row representing one point in time series.
            The first column is the x-variable and the second column is the y-variable.

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> wv.to_2d_array()
        array([[ 5., 10.],
               [ 6., 12.],
               [ 7., 14.],
               [ 8., 16.],
               [ 9., 18.],
               [10., 20.],
               [11., 22.],
               [12., 24.],
               [13., 26.],
               [14., 28.],
               [15., 30.]])

        """
        return np.column_stack((self.x, self.y))

    def scale_x(self, scale):
        """Scale x-axis.

        Parameters
        ----------
        scale: float
            Value by which scale x-axis.

        Returns
        -------
        self

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.scale_x(2).get()
        >>> res_x
        array([10., 12., 14., 16., 18., 20., 22., 24., 26., 28., 30.])

        """
        self.x_scale = self.x_scale * scale
        self.x = self.x * scale
        self.reference_x = self.reference_x * scale
        return self

    def scale_y(self, scale):
        """Scale y-axis.

        Parameters
        ----------
        scale: float
            Value by which scale y-axis.

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.scale_y(2).get()
        >>> res_y
        array([20., 24., 28., 32., 36., 40., 44., 48., 52., 56., 60.])

        """
        self.y_scale = self.y_scale * scale
        self.y = self.y * scale
        self.reference_y = self.reference_y * scale
        return self

    def shift_x(self, shift):
        """Shift x-axis

        Parameters
        ----------
        shift: float
            Value by which shift x-axis.

        Returns
        -------
        self

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.shift_x(1).get()
        >>> res_x
        array([ 6.,  7.,  8.,  9., 10., 11., 12., 13., 14., 15., 16.])

        """
        self.x = self.x + shift
        self.reference_x = self.reference_x + shift
        return self

    def shift_y(self, shift):
        """Shift y-axis.

        Parameters
        ----------
        shift: float
            Value by which shift y-axis.

        Returns
        -------
        self

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.shift_y(1).get()
        >>> res_y
        array([11., 13., 15., 17., 19., 21., 23., 25., 27., 29., 31.])

        """
        self.y = self.y + shift
        self.reference_y = self.reference_y + shift
        return self

    def normalize_x(self, min_val, max_val):
        """Normalize x values.

        Parameters
        ----------
        min_val: float
            Minimum value for normalization.

        max_val: float
            Minimum value for normalization.

        Returns
        -------
        self

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.normalize_x(0, 10).get()
        >>> res_x
        array([ 0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10.])

        """
        self.x = normalize(self.x, min_val, max_val)
        self.original_x = normalize(self.original_x, min_val, max_val)
        self.reference_x = normalize(self.reference_x, min_val, max_val)
        return self

    def normalize_y(self, min_val, max_val):
        """Normalize y values.

        Parameters
        ----------
        min_val: float
            Minimum value for normalization.

        max_val: float
            Minimum value for normalization.

        Returns
        -------
        self

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.normalize_y(0, 10).get()
        >>> res_y
        array([ 0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10.])

        """
        self.y = normalize(self.y, min_val, max_val)
        self.original_y = normalize(self.original_y, min_val, max_val)
        self.reference_y = normalize(self.reference_y, min_val, max_val)
        return self

    def __len__(self):
        """Length of the time series"""
        return len(self.x)

    def truncate_by_value(self, x_left, x_right, x_left_as_ratio=False, x_right_as_ratio=False):
        """Truncate to specific value range or ratio of the range.

        Parameters
        ----------
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
            If true, `x_right` is treated as ratio of the x array to truncate from the right,
            where 0.0 is the start and 1.0 is the end of the array.

        Returns
        -------
        self

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.truncate_by_value(6.5, 11.5).get()
        >>> res_x
        array([ 6.,  7.,  8.,  9., 10., 11., 12.])
        >>> res_y
        array([12., 14., 16., 18., 20., 22., 24.])

        """
        self.x, self.y = truncate(self.x, self.y, x_left=x_left, x_right=x_right, x_left_as_ratio=x_left_as_ratio,
                                  x_right_as_ratio=x_right_as_ratio)
        self.reference_x, self.reference_y = truncate(self.reference_x, self.reference_y, x_left=x_left,
                                                      x_right=x_right, x_left_as_ratio=x_left_as_ratio,
                                                      x_right_as_ratio=x_right_as_ratio)
        return self

    def truncate_by_index(self, start=0, stop=None):
        """Truncate to specific index of the range.

        Parameters
        ----------
        start: int, default: 0
            Start index of the array to truncate.
        stop: int, default: None
            Stop index of the array to truncate. If None, then it is equal to the length of the time series.

        Returns
        -------
        self

        Examples
        --------
        >>> import numpy as np
        >>> from traffic_weaver.weaver import Weaver
        >>> x = np.linspace(5, 15, 11)
        >>> y = 2 * x
        >>> wv = Weaver(x, y)
        >>> res_x, res_y = wv.truncate_by_index(2, 6).get()
        >>> res_x
        array([ 7.,  8.,  9., 10.])
        >>> res_y
        array([14., 16., 18., 20.])

        """
        if stop is None:
            stop = len(self.x)
        if start < 0:
            raise ValueError("Start index should be non-negative")
        if stop > len(self.x):
            raise ValueError("Stop index should be less than length of x")
        self.x = self.x[start:stop]
        self.y = self.y[start:stop]
        self.reference_x = self.reference_x[start:stop]
        self.reference_y = self.reference_y[start:stop]
        return self
