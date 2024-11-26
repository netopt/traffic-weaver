# Traffic Weaver

Semi-synthetic time-varrying traffic generator based on averaged time series.

[![PyPI version](https://badge.fury.io/py/traffic-weaver.svg)](https://badge.fury.io/py/traffic-weaver)
[![test](https://github.com/w4k2/traffic-weaver/actions/workflows/test.yml/badge.svg)](https://github.com/w4k2/traffic-weaver/actions/workflows/test.yml)
[![coverage badge](https://github.com/w4k2/traffic-weaver/raw/main/badges/coverage.svg)](https://github.com/w4k2/traffic-weaver/raw/main/badges/coverage.svg)
[![Deploy Sphinx documentation to Pages](https://github.com/w4k2/traffic-weaver/actions/workflows/documentation.yml/badge.svg)](https://github.com/w4k2/traffic-weaver/actions/workflows/documentation.yml)
[![pages-build-deployment](https://github.com/w4k2/traffic-weaver/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/w4k2/traffic-weaver/actions/workflows/pages/pages-build-deployment)

## Acknowledgments and citation

Please cite this paper when you use this simulator in your publications/lectures/presentations:

> Piotr Lechowicz, Aleksandra Knapińska, Adam Włodarczyk, Krzysztof Walkowiak,
"Traffic Weaver: semi-synthetic time-varying traffic generator based on averaged time series,"
SoftwareX, Volume 28, 101946, 2024.


## Table of content

- [Documentation](https://w4k2.github.io/traffic-weaver/)
    - [Introduction](https://w4k2.github.io/traffic-weaver/introduction.html)
    - [Quick start](https://w4k2.github.io/traffic-weaver/quick_start.html)
    - [Datasets](https://w4k2.github.io/traffic-weaver/datasets.html)
    - [Using the API](https://w4k2.github.io/traffic-weaver/using_the_api.html)
    - [API reference](https://w4k2.github.io/traffic-weaver/apidocs/traffic_weaver.html)
    - [Development](https://w4k2.github.io/traffic-weaver/development.html)

## Introduction

Traffic Weaver is a Python package developed to generate a semi-synthetic signal (time series) with finer granularity,
based on averaged time series, in a manner that, upon averaging, closely matches the original signal provided.
The key components utilized to recreate the signal encompass:

* oversampling
* recreating from average with a given strategy,
* stretching to match the integral of the original time series,
* interpolating,
* smoothing,
* repeating,
* applying trend,
* adding noise.

The primary motivation behind Traffic Weaver is to furnish semi-synthetic time-varying traffic in telecommunication
networks, facilitating the development and validation of traffic prediction models, as well as aiding in the deployment
of network optimization algorithms tailored for time-varying traffic.

The purpose of Traffic Weaver is to generate new time-varying data based on an already available sample of data, i.e.,
to create semi-synthetic data when the size of real data is either insufficient or the time points at which the data
were measured are too rare.

In consequence, it can generate larger and diverse datasets with similar traffic patterns based on the original traffic.

Below figure shows a general usage example. shows a general usage example. Based on the provided original averaged time series (a),
the signal is *n*-times oversampled and recreated from average values with a predefined strategy (b).
Next, it is stretched to match the integral of the input time series function (c).
Further, it is smoothed with a spline function (d). In order to create weekly
semi-synthetic data, the signal is repeated seven times (e), applying a long-term trend consisting of sinusoidal and
linear functions (f). Finally, the noise is introduced to the signal, starting from small values and increasing over
time (g). To validate the correctness of the applied processing, (h) presents the averaged two periods of the created
signal, showing that they closely match the original signal (except the applied trend).

<img alt="Signal processing" width="800px" src="https://github.com/w4k2/traffic-weaver/raw/main/docs/source/_static/gfx/introduction/signal_processing_overview.png"/>
