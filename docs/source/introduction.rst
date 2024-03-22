Introduction
============

Scope
-----

Traffic Weaver reads averaged time series and creates
semi-synthetic signal with finer granularity, that after averaging
matches the original provided signal.
Following tools are applied to create semi-synthetic signal.

* Oversampling with a given strategy
* Stretching to match the integral of the original time series
* Smoothing
* Repeating
* Trending
* Noising

:numref:`fig-signal-processing` shows general usage example.
Based on provided original averaged time series (a), signal is *n*-times oversampled
with predefined strategy (b). Next, it is stretched to match integral of the input
time series function (c). Further, it is smoothed with spline function (d).
In order to create weekly semi-synthetic data, signal is repeated 7 times
(e) applying long-term trend consisting of sinusoidal and linear function (f).
Finally, the noise is introduced to the signal. starting from small values and
increasing over time (g). To validate correctness of applied processing,
(h) presents averaged two periods of created signal, showing that they closely
match the original signal (except the applied trend).

.. _fig-signal-processing:

.. figure:: /_static/gfx/signal_processing_overview.pdf
   :width: 800
   :alt: Signal processing

   Signal processing.

Software architecture
---------------------

:numref:`fig-software-architecture` presents overview of software architecture.
`Weaver`, located in `weaver.py` module, wraps supplied time series data and provides
interface for processing functionalities. Time series can be either specified by the
user or obtained from embedded example datasets.
Individual functionalities provided by the `Weaver` are delegated to other modules,
e.g., oversampling functionality is located in `oversample.py` module. However,
it is possible to use individual functionalities from they corresponding modules
regardless of wrapping time series into `Weaver`. `Weaver` allows to retrieve processed
data either as sampled points or continues spline function.


.. _fig-software-architecture:

.. figure:: /_static/gfx/software_architecture.pdf
   :width: 500
   :alt: Software architecture

   Software architecture.

Functionalities description
---------------------------

This section describes main functionalities provided by the Traffic Weaver.
In the below description term `interval` refers to the distance between two sampled
points in input time series. The aim of the Weaver is to create output time series
with inserted multiple points in each interval.

- Class :func:`Weaver(x, y)<traffic_weaver.weaver.Weaver>`
	`Weaver` is an interface for recreating time series.
	It takes as an input time series provided as two lists containing values of
	independent and dependent variables. It delegates processing to other modules
	and allows to retrieve recreated time series either as lists of values of
	independent and dependent variables or as a spline, using,
	:func:`~traffic_weaver.weaver.Weaver.get` and
	:func:`~traffic_weaver.weaver.Weaver.to_function`
	methods, respectively.
- Oversampling
	Oversampling is recreation of time series with finer sampling granularity based on supplied strategy.
	Number of created points between each interval (pair of points in the original
	time series) is provided as a parameter. The strategy determines how created time
	series transit between points, i.e., how new points are located.
	Software provides several strategies, namely,
	:func:`~traffic_weaver.oversample.ExpAdaptiveOversample`,
	:func:`~traffic_weaver.oversample.ExpFixedOversample`,
	:func:`~traffic_weaver.oversample.LinearAdaptiveOversample`,
	:func:`~traffic_weaver.oversample.LinearFixedOversample`,
	:func:`~traffic_weaver.oversample.PiecewiseConstantOversample`,
	:func:`~traffic_weaver.oversample.CubicSplineOversample`.
	E.g., `ExpAdaptiveOversample` creates adaptive transition window for each
	interval by combining linear and exponential function. The size of the window
	is inversely proportionally to the change of function value on both edges of
	the interval, i.e., if function value has higher change on the right side of
	the interval, than on the left side, the right side transition window is smaller
	than the left one.

	`Weaver` class provides method
	:func:`oversample(n, oversample_class, **kwargs)<traffic_weaver.weaver.Weaver.oversample>`
	that delegates execution to oversample module and takes as an input number of samples
	`n` in each interval after oversampling, `oversample_class` defining
	oversample strategy class inheriting
	:func:`~traffic_weaver.oversample.AbstractOversample` class,
	and dictionary of parameters passed to selected strategy.
- Integral matching
	It aims to reshape time series to match its integral to the integral of the
	reference piece wise constant function over the same domain
	(the original time series). It does that by stretching time series in intervals
	such that the integral in interval of current time series is equal to the
	integral of the same interval in the reference function.
	Points in each interval are transformed inversely proportionally to the
	exponential value of distance from the interval center.

	`Weaver` class provides method :func:`integral_match(**kwargs)<traffic_weaver.weaver.Weaver.integral_match>`
	that delegates execution to match module and takes as an input a dictionary of
	parameters passed to matching function. Currently stored time series in `Weaver` is
	matched with reference to originally passed function to the class.
- Smoothing
	It smooths a function using smoothing splines.

	`Weaver` class provides method :func:`smooth(s)<traffic_weaver.weaver.Weaver.smooth>` to
	delegate the execution to smoothing function, and takes `s` as an argument.
	The argument `s` is a smoothing condition that controls the tradeoff
	between closeness and smoothness of fit. Larger `s` means more smoothing while
	smaller values of `s` indicate less smoothing. If `s` is None, it's 'good' value
	is calculated based on number of samples and standard deviation.
- Repeating
	It repeats time series a given number of times, resulting in long term time series
	containing periodic, e.g., daily or weakly, patterns.

	`Weaver` class provides method :func:`repeat(n)<traffic_weaver.weaver.Weaver.repeat>` to
	repeat time series. `n` is an argument passed to the function, defining how many
	time repeat the time series.
- Trending
	It applies trend to time series according to specified function. It allows to
	add long term trend to time series, e.g., constant dependent variable increase over
	time.

	`Weaver` class provides method
	:func:`trend(trend_func)<traffic_weaver.weaver.Weaver.trend>` to apply trend to
	processed time series. Argument `trend_function` is a callable that shifts value
	for dependent variable based on value of independent variable normalized to
	`(0, 1)` range. The callable takes one argument being the normalized value of
	independent variable, and has to return shift value for the dependent variable.
- Noising
	It applies constant or changing over time gaussian noise to time series
	expressed as signal to noise ratio.

	`Weaver` class provides method
	:func:`noise(snr, **kwargs)<traffic_weaver.weaver.Weaver.noise>` to apply noise to
	a time series. Argument `snr` defines signal-to-noise ratio of a function either as
	a scalar value, or as a list of changing values over time which size matches size
	of independent variable. `**kwargs` is a set of parameters passed to noising
	function, allowing, e.g., to express noise as normal distribution standard
	deviation instead of signal to noise ration.
