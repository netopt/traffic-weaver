# Traffic Weaver

Semi-synthetic time series generator based on averaged data.

[![PyPI version](https://badge.fury.io/py/traffic-weaver.svg)](https://badge.fury.io/py/traffic-weaver)
[![test](https://github.com/netopt/traffic-weaver/actions/workflows/test.yml/badge.svg)](https://github.com/netopt/traffic-weaver/actions/workflows/test.yml)
[![coverage badge](https://github.com/netopt/traffic-weaver/raw/main/badges/coverage.svg)](https://github.com/netopt/traffic-weaver/raw/main/badges/coverage.svg)
[![Deploy Sphinx documentation to Pages](https://github.com/netopt/traffic-weaver/actions/workflows/documentation.yml/badge.svg)](https://github.com/netopt/traffic-weaver/actions/workflows/documentation.yml)
[![pages-build-deployment](https://github.com/netopt/traffic_weaver/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/netopt/traffic_weaver/actions/workflows/pages/pages-build-deployment)

## Acknowledgments and citation

TBD

## Table of content
- [Documentation](https://netopt.github.io/traffic-weaver/)
    - [Introduction](https://netopt.github.io/traffic-weaver/introduction.html)
    - [Quick start](https://netopt.github.io/traffic-weaver/quick_start.html)
    - [API reference](https://netopt.github.io/traffic-weaver/apidocs/traffic_weaver.html)


## Introduction

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

Below figure shows general usage example.
Based on provided original averaged time series (a), signal is *n*-times oversampled
with predefined strategy (b). Next, it is stretched to match integral of the input
time series function (c). Further, it is smoothed with spline function (d).
In order to create weekly semi-synthetic data, signal is repeated 7 times
(e) applying long-term trend consisting of sinusoidal and linear function (f).
Finally, the noise is introduced to the signal. starting from small values and
increasing over time (g). To validate correctness of applied processing,
(h) presents averaged two periods of created signal, showing that they closely
match the original signal (except the applied trend).

<img alt="Signal processing" width="800px" src="https://github.com/netopt/traffic-weaver/raw/main/docs/source/_static/gfx/signal_processing_overview.png"/>

.. _fig-signal-processing:

.. figure::
   :width: 800
   :alt: Signal processing

   Signal processing.
