Using the API
=============

Presented below examples assume the following imports.

.. code-block:: python

    from traffic_weaver.datasets import load_dataset
    from traffic_weaver import Weaver
    import numpy as np
    np.random(0)
    import matplotlib.pyplot as plt

Reading data
------------

Traffic Weaver can be initialized with user specified data or populated with exemplary dataset.

Reading data as a list of independent and dependent variables.

.. code-block:: python

    x = np.linspace(0, 10, 100)
    y = np.sin(2 * x)
    wv = Weaver(x, y)

Reading data from dataset.

.. code-block:: python

    wv = Weaver.from_2d_array(load_dataset('sandvine_audio'))

Reading data from csv file.

.. code-block:: python

    wv = Weaver.from_csv("./data.csv")

Reading data from pandas.

.. code-block:: python

    import pandas as pd
    df = pd.DataFrame(...)
    wv = Weaver.from_pandas(df)

Preprocessing data
------------------

AMS-IX weekly dataset contains 8 days of traffic,
In case 7 days or traffic are needed, it can be achieved by truncating the data.

.. code-block:: python

    wv = Weaver.from_2d_array(load_dataset('ams-ix-weekly'))
    wv.truncate(x_left=0, x_right_ratio=7/8).normalize_x(0, 7)

Getting processed signal
------------------------

In the `Weaver` class, `x` and `y` fields corresponds to processed time series.
`original_x` and `original_y` fields corresponds to originally passed values.
`reference_x` and `reference_y` fields corresponds to processed fields used as a reference
for integral matching. Reference function is transformed with the processed function
when applying scaling, truncating, shifting and repeating.
For other function it remains unchanged.
:func:`~traffic_weaver.weaver.Weaver.get` function returns processed data from `Weaver`,
:func:`~traffic_weaver.weaver.Weaver.get_original` returns original function and
:func:`~traffic_weaver.weaver.Weaver.get_reference` returns reference function for integral matching.

.. code-block:: python

    x = np.linspace(0, 10, 11)
    y = np.sin(2 * x)
    wv = Weaver(x, y)
    wv.scale_x(2).repeat(2)
    wv.noise(30).recreate_from_average(10).integral_match().smooth(1.0)

    fig, axes = plt.subplots(3)
    # plot processed signal
    axes[0].plot(*wv.get())
    # plot original signal
    axes[1].plot(*wv.get_original())
    # plot reference signal for integral matching
    axes[2].plot(*wv.get_reference_function())
    plt.show()


Interpolation
-------------

Interpolation can be used to create new points between existing ones according to the user needs.

.. code-block:: python

    # MIX-IT Milan yearly dataset contains 365 days of traffic,
    # however the dataset is samples with 9977 points.
    # In case 365 points are needed (one for each day), interpolation can be used.

    wv = Weaver.from_2d_array(load_dataset('mix-it-milan-yearly'))
    wv.normalize_x(0, 365)
    wv.interpolate(365)
    fig, axes = plt.subplots(2)
    axes[0].plot(*wv.get(), '.-')

    # exactly same result can be achieved specifying exact points location for interpolation
    wv.restore_original()
    wv.interpolate(new_x=np.linspace(0, 365, 365))
    axes[1].plot(*wv.get(), '.-')

    plt.show()

Repeating
---------

.. code-block:: python

    wv = Weaver.from_2d_array(load_dataset('sandvine_tiktok'))
    wv.append_one_sample(make_periodic=True)
    fig, axes = plt.subplots(2)
    axes[0].step(*wv.get(), '.-', where='post')
    wv.repeat(4)
    axes[1].step(*wv.get(), '.-', where='post')
    fig.show()

Trending
--------------
Long term trend is applied to the data in a form of a function.
Callable signature is `(x) -> y_shift`. The trend function can be either specified
in the domain of independent variable, or normalized to the range of [0, 1].

.. code-block:: python

    x = np.linspace(0, 10, 100)
    y = np.sin(2 * x)
    wv = Weaver(x, y)

    # apply trend f(y) = 1/5 x
    wv.trend(lambda x: 1 / 5 * x).get()

    fig, axes = plt.subplots(2)
    axes[0].plot(*wv.get())

    # apply same trend with normalization to [0, 1] range
    wv.restore_original()
    wv.trend(lambda x: 2 * x, normalized=True).get()

    axes[1].plot(*wv.get())
    plt.show()

Recreate from average
---------------------

Recreating from average can be achieved by using one of the strategies specified in
:doc:`rfa <apidocs/traffic_weaver.rfa>` module. Typically recreation should be followed
by integral matching to ensure that the integral of the original and recreated signal is similar.

.. code-block:: python

    from traffic_weaver.rfa import LinearFixedRFA, ExpAdaptiveRFA
    wv = Weaver.from_2d_array(load_dataset('sandvine_tiktok'))

    fig, axes = plt.subplots(3)
    axes[0].step(*wv.get(), '.-', where='post')
    wv.recreate_from_average(10, rfa_class=LinearFixedRFA).integral_match()
    axes[1].plot(*wv.get(), '.-')
    wv.restore_original()
    wv.recreate_from_average(10, rfa_class=ExpAdaptiveRFA, alpha=0.5).integral_match()
    axes[2].plot(*wv.get(), '.-')
    fig.show()

Integral match
--------------

Integral matching allows to adjust the signal to have the same integral as the reference signal.
Function :func:`~traffic_weaver.weaver.Weaver.integral_match` takes arguments `target_function_integral_method`
and `reference_function_integral_method` defining how integral
should be calculated for the target and the reference, respectively.
For original time varying function sampled at different points use
`reference_function_integral_method='trapezoid'`.
For original time varying function that is an averaged function over periods of time use
`reference_function_integral_method='rectangular'`.

.. code-block:: python

    wv = Weaver.from_2d_array(load_dataset('sandvine_tiktok'))
    wv.append_one_sample(make_periodic=True)
    fig, axes = plt.subplots(4)
    axes[0].step(*wv.get(), '.-', where='post')
    wv.recreate_from_average(10).integral_match()
    axes[1].plot(*wv.get(), '.-')
    wv.restore_original()
    axes[2].plot(*wv.get(), '.-')
    wv.recreate_from_average(10).integral_match(reference_function_integral_method='trapezoid')
    axes[3].plot(*wv.get(), '.-')
    fig.show()


Noising
-------

Noise can be added as a fixed signal-to-noise ratio value, or as a changing parameter over time.

.. code-block:: python

    wv = Weaver.from_2d_array(load_dataset('sandvine_tiktok'))
    wv.append_one_sample(make_periodic=True)
    fig, axes = plt.subplots(3)
    axes[0].step(*wv.get(), '.-', where='post')
    wv.repeat(5).recreate_from_average(20).integral_match()
    wv.noise(20)
    axes[1].plot(*wv.get())

    wv.restore_original()
    wv.repeat(5).recreate_from_average(20).integral_match()
    wv.noise([40 - 30 * i / len(wv) for i in range(len(wv))])
    axes[2].plot(*wv.get())
    plt.show()


Smoothing
---------

Function can be smoothened using spline.

.. code-block:: python

    wv = Weaver.from_2d_array(load_dataset('sandvine_tiktok'))
    wv.append_one_sample(make_periodic=True)
    fig, axes = plt.subplots(3)
    axes[0].step(*wv.get(), '.-', where='post')
    wv.recreate_from_average(20).integral_match()
    axes[1].plot(*wv.get())
    wv.smooth(1.0)
    axes[2].plot(*wv.get())
    plt.show()