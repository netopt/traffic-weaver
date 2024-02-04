r"""Wrapping array into intervals.

Contains IntervalArray structure wrapping array and allowing to access it by providing
interval value.
"""
from typing import Callable, Union, List

import numpy as np

from .array_utils import (
    oversample_linspace,
    oversample_piecewise_constant,
    extend_linspace,
    extend_constant,
)


class IntervalArray:
    def __init__(self, a: Union[np.ndarray, List], n: int = 1):
        r"""Wrap 1-D array into 2-D interval structure of length n.

        Reshapes array `a` of size `n` into 2-D array of shape `(len(a)/n, n)`.
        Elements are accessed using __getitem__ and __setitem__ providing interval
        and element number `a[i, j]` where it denotes `j`-th element of `i`-th interval,
        i.e., `i * n + j` element

        Skipping `j-th` value is equivalent to selecting element in flat array
        (without intervals):
        `a[i] == a[i // n, i % n]`.

        Parameters
        ----------
        a: 1D-array
            Input array.
        n: int, default: 1
            Interval size. f interval size is `1`, it behaves like a normal array.

        Examples
        ----------
        >>> from traffic_weaver.interval import IntervalArray
        >>> import numpy as np
        >>> x = np.arange(9)
        >>> a = IntervalArray(x, 5)
        >>> print(a[1, 2])
        7
        >>> print(a[1])
        1
        >>> a[1, 2] = 15
        >>> a[1, 2]
        15

        """
        self.a = np.asarray(a)
        self.n = n

    def __getitem__(self, item):
        r"""Access the element in interval array by index `item`.

        Parameters
        ----------
        item: int | tuple of two ints
            If item is a tuple `(k, i)`, it accesses element in `a[n * k + i]`.
            If item is an int `i`, it accesses element `a[i]`.

        Returns
        -------
        object
            Accessed element.
        """
        if isinstance(item, int):
            return self.a[item]
        elif len(item) == 2:
            interval = item[0]
            element = item[1]
            return self.a[interval * self.n + element]
        else:
            raise IndexError("too many indices for IntervalArray")

    def __setitem__(self, key, value):
        r"""Sets the element value in interval array to `value` accessed by index `key`.

        Parameters
        ----------
        key: int | tuple of two ints
            If item is a tuple (k, i), it accesses element in `a[n * k + i]`.
            If item is an int `i`, it accesses element `a[i]`.
        value: float
            Value to set for item.
        """
        if isinstance(key, int):
            self.a[key] = value
        elif len(key) == 2:
            interval = key[0]
            element = key[1]
            self.a[interval * self.n + element] = value
        else:
            raise IndexError("too many indices for IntervalArray")

    def __iter__(self):
        return iter(self.a)

    def extend_linspace(self, direction="both"):
        r"""Extend one interval in given direction with linearly spaced values.

        Parameters
        ----------
        direction: str, default='both'
            Possible values are 'both', 'left', 'right'.
        """
        self.a = extend_linspace(self.a, self.n, direction=direction)

    def extend_constant(self, direction="both"):
        r"""Extend one interval in given direction with constant value.

        Parameters
        ----------
        direction: str, default='both'
            Possible values are 'both', 'left', 'right'.
        """
        self.a = extend_constant(self.a, self.n, direction=direction)

    def nr_of_full_intervals(self):
        r"""Number of intervals that contain all n items."""
        return len(self.a) // self.n

    def __len__(self):
        r"""Total number of elements in all intervals."""
        return len(self.a)

    @property
    def array(self):
        r"""Array storing values of intervals."""
        return self.a

    def to_2d_array(self):
        r"""Convert intervals to 2D array.

        Examples
        --------
        Let assume that the IntervalArray has the following representation:

        .. code::

            IntervalArray([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], n=4)

        Converting it to 2D array results in creating the following ndarray:

        .. code::

            array([[ 0.,  1.,  2.,  3.],
            [ 4.,  5.,  6.,  7.],
            [ 8.,  9., nan, nan]])

        """
        m, n = self.a.size // self.n, self.n
        if self.a.size % self.n != 0:
            m = m + 1
        return np.pad(
            self.a.astype(float),
            (0, m * n - self.a.size),
            mode="constant",
            constant_values=np.nan,
        ).reshape(m, n)

    def to_2d_array_closed_intervals(self, drop_last=True):
        r"""Convert to 2D array, each row ends with the first value from the next one.

        Parameters
        ----------
        drop_last: bool, default: True
            Whether to drop the last row.
            Usually last row contains the last value of an array and
            is filled up with NaNs.

        Examples
        --------
        Let assume that the IntervalArray has the following representation:

        .. code::

            IntervalArray([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], n=4)

        Converting it to 2D array results in creating the following ndarray:

        .. code::

            array([[ 0.,  1.,  2.,  3., 4.],
            [ 4.,  5.,  6.,  7., 8..]])

        """
        interv = self.to_2d_array()
        res = np.concatenate(
            [interv, np.concatenate([interv[1:, :1], [[np.nan]]])], axis=1
        )
        return res if not drop_last else res[:-1]

    def oversample(
        self,
        num: int,
        method: Callable[[Union[list[float], np.ndarray], int], np.ndarray],
    ):
        r"""Oversample array n times using provided method.

        Parameters
        ----------
        num: int
            Number of additional samples.
        method: Callable
            Method used to oversample the array.

        Returns
        -------
        IntervalArray
            Oversampled IntervalArray.
        """
        prev_n = self.n
        a = method(self.a, num)
        return IntervalArray(a, prev_n * num)

    def oversample_linspace(self, num: int):
        r"""Concrete implementation of oversample using linspace.

        Parameters
        ----------
        num: int
            Number of additional samples.

        Returns
        -------
        IntervalArray
            Oversampled IntervalArray.
        """
        return self.oversample(num, method=oversample_linspace)

    def oversample_piecewise(self, num: int):
        r"""Concrete implementation of oversample using piecewise constants.

        Parameters
        ----------
        num: int
            Number of additional samples.

        Returns
        -------
        IntervalArray
            Oversampled IntervalArray.
        """
        return self.oversample(num, method=oversample_piecewise_constant)

    def __repr__(self):
        return f"IntervalArray({self.array.tolist()}, n={self.n})"
