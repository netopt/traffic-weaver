"""Sandvine dataset.

Load methods return dataset as np.ndarray of shape (nr_of_samples, 2).
It is 2D array with each row representing one point in time series.
The first column is the x-variable and the second column is the y-variable.

If `unpack_dataset_columns=True` is specified as kwargs, the dataset is unpacked to two separate arrays x and y.

"""

from os import path

from ._base import load_csv_dataset_from_resources, load_dataset_description


def sandvine_dataset_description():
    """Get description of this dataset.
    """
    return load_dataset_description("sandvine.md")


def load_sandvine_audio(**kwargs):
    """Load and return sandvine audio dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "audio.csv"), **kwargs)


def load_sandvine_cloud(**kwargs):
    """Load and return sandvine cloud dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "cloud.csv"), **kwargs)


def load_sandvine_file_sharing(**kwargs):
    """Load and return sandvine file sharing dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "file_sharing.csv"), **kwargs)


def load_sandvine_fixed_social_media(**kwargs):
    """Load and return sandvine fixed social media dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "fixed_social_media.csv"), **kwargs)


def load_sandvine_gaming(**kwargs):
    """Load and return sandvine gaming dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "gaming.csv"), **kwargs)


def load_sandvine_marketplace(**kwargs):
    """Load and return sandvine marketplace dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "marketplace.csv"), **kwargs)


def load_sandvine_measurements(**kwargs):
    """Load and return sandvine measurements dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "measurements.csv"), **kwargs)


def load_sandvine_messaging(**kwargs):
    """Load and return sandvine messaging dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "messaging.csv"), **kwargs)


def load_sandvine_mobile_messaging(**kwargs):
    """Load and return sandvine mobile messaging dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "mobile_messaging.csv"), **kwargs)


def load_sandvine_mobile_social_media(**kwargs):
    """Load and return sandvine mobile social media dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "mobile_social_media.csv"), **kwargs)


def load_sandvine_mobile_video(**kwargs):
    """Load and return sandvine mobile video dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "mobile_video.csv"), **kwargs)


def load_sandvine_mobile_youtube(**kwargs):
    """Load and return sandvine mobile youtube dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "mobile_youtube.csv"), **kwargs)


def load_sandvine_mobile_zoom(**kwargs):
    """Load and return sandvine mobile zoom dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "mobile_zoom.csv"), **kwargs)


def load_sandvine_snapchat(**kwargs):
    """Load and return sandvine snapchat dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "snapchat.csv"), **kwargs)


def load_sandvine_social_networking(**kwargs):
    """Load and return sandvine social networking dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "social_networking.csv"), **kwargs)


def load_sandvine_tiktok(**kwargs):
    """Load and return sandvine tiktok dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "tiktok.csv"), **kwargs)


def load_sandvine_video_streaming(**kwargs):
    """Load and return sandvine video streaming dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "video_streaming.csv"), **kwargs)


def load_sandvine_vpn_and_security(**kwargs):
    """Load and return sandvine vpn and security dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "vpn_and_security.csv"), **kwargs)


def load_sandvine_web(**kwargs):
    """Load and return sandvine web dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "web.csv"), **kwargs)
