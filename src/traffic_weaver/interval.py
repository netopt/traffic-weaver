r"""Wrapping array into intervals.

Contains IntervalArray structure wrapping array and allowing to access it by providing
interval value.
"""
from typing import Callable, Union

import numpy as np

from .oversample_fun import (oversample_linspace, oversample_piecewise_constant,
                             extend_linspace, extend_constant, )


class IntervalArray:
    def __init__(self, a: np.ndarray, n: int = 1):
        r"""Wrap 1-D array into 2-D interval structure of length n

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
        r"""Extend one period in given direction with linearly spaced values.

        Parameters
        ----------
        direction: str, default='both'
            Possible values are 'both', 'left', 'right'.
        """
        self.a = extend_linspace(self.a, self.n, direction=direction)

    def extend_constant(self, direction="both"):
        r"""Extend one period in given direction with constant value.

        Parameters
        ----------
        direction: str, default='both'
            Possible values are 'both', 'left', 'right'.
        """
        self.a = extend_constant(self.a, self.n, direction=direction)

    def nr_of_intervals(self):
        return len(self.a) // self.n

    def __len__(self):
        return len(self.a)

    @property
    def array(self):
        return self.a

    def as_intervals(self):
        m, n = self.a.size // self.n, self.n
        if self.a.size % self.n != 0:
            m = m + 1
        return np.pad(self.a.astype(float), (0, m * n - self.a.size), mode="constant",
                      constant_values=np.nan, ).reshape(m, n)

    def as_closed_intervals(self, drop_last=True):
        interv = self.as_intervals()
        res = np.concatenate([interv, np.concatenate([interv[1:, :1], [[np.nan]]])],
                             axis=1)
        return res if not drop_last else res[:-1]

    def oversample(self, num: int,
                   method: Callable[[Union[list[float], np.ndarray], int], np.ndarray], ):
        prev_n = self.n
        a = method(self.a, num)
        return IntervalArray(a, prev_n * num)
    def oversample_linspace(self, num: int):
        return self.oversample(num, method=oversample_linspace)

    def oversample_piecewise(self, num: int):
        return self.oversample(num, method=oversample_piecewise_constant)

    def __repr__(self):
        return f"IntervalArray({self.array.tolist()}, n={self.n})"
