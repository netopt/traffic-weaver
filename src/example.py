def small_example():
    from traffic_weaver import Weaver
    from traffic_weaver.datasets import load_mobile_video
    from traffic_weaver.array_utils import append_one_sample
    import matplotlib.pyplot as plt

    # load exemplary dataset
    x, y = load_mobile_video()

    # add one sample to the end as file contains averaged values for time intervals
    x, y = append_one_sample(x, y, make_periodic=True)

    wv = Weaver(x, y)

    # plot original time series
    fig, axes = plt.subplots()
    axes.plot(*wv.get(), drawstyle="steps-post")
    plt.show()

    # process time series
    wv.repeat(4).trend(lambda x: 0.5 * x).noise(snr=60)

    # plot modified time series
    fig, axes = plt.subplots()
    axes.plot(*wv.get())
    plt.show()

    # get time series processed data
    x, y = wv.get()

    # or get them as a spline function to sample any arbitrary point
    f = wv.to_function()
    # get value at 0.5
    f(0.5)


def larger_example():
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    from traffic_weaver import Weaver
    from traffic_weaver.datasets import load_mobile_video
    from traffic_weaver.array_utils import append_one_sample

    font = {"family": "serif", "serif": "Palatino", "size": 12}
    matplotlib.rc("font", **font)

    kwargs = {"marker": "o", "markersize": 4, "linewidth": 2, "linestyle": "dashed"}
    kwargs2 = {"linewidth": 2}

    n = 10

    x, y = load_mobile_video()
    # add one point to the end of data
    x, y = append_one_sample(x, y, make_periodic=True)

    wv = Weaver(x, y)

    # plot
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(12, 20))
    axes = axes.flatten()

    axes[0].plot(*wv.get(), drawstyle="steps-post", **kwargs)
    axes[1].plot(*(wv.oversample(n).get()), **kwargs)
    axes[2].plot(*(wv.integral_match().get()), **kwargs2)
    axes[3].plot(*(wv.smooth(s=0.2).get()), **kwargs2)
    axes[4].plot(*(wv.repeat(4).get()), **kwargs2)
    axes[5].plot(*wv.trend(lambda x: 0.5 * x).get(), **kwargs2)
    snr = np.linspace(50, 20, len(wv.get()[1]))
    axes[6].plot(*(wv.noise(snr).get()), **kwargs2)

    plt.tight_layout(pad=2.0)
    plt.show()


if __name__ == "__main__":
    small_example()
