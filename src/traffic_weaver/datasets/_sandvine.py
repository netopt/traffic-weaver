from os import path

from ._base import load_csv_dataset_from_resources, load_dataset_description


def sandvine_dataset_description():
    """Get description of this dataset.
    """
    return load_dataset_description("sandvine.md")


def load_sandvine_audio():
    """Load and return sandvine audio dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "audio.csv"))


def load_sandvine_cloud():
    """Load and return sandvine cloud dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "cloud.csv"))


def load_sandvine_file_sharing():
    """Load and return sandvine file sharing dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "file_sharing.csv"))


def load_sandvine_fixed_social_media():
    """Load and return sandvine fixed social media dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "fixed_social_media.csv"))


def load_sandvine_gaming():
    """Load and return sandvine gaming dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "gaming.csv"))


def load_sandvine_marketplace():
    """Load and return sandvine marketplace dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "marketplace.csv"))


def load_sandvine_measurements():
    """Load and return sandvine measurements dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "measurements.csv"))


def load_sandvine_messaging():
    """Load and return sandvine messaging dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "messaging.csv"))


def load_sandvine_mobile_messaging():
    """Load and return sandvine mobile messaging dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "mobile_messaging.csv"))


def load_sandvine_mobile_social_media():
    """Load and return sandvine mobile social media dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "mobile_social_media.csv"))


def load_sandvine_mobile_video():
    """Load and return sandvine mobile video dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "mobile_video.csv"))


def load_sandvine_mobile_youtube():
    """Load and return sandvine mobile youtube dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "mobile_youtube.csv"))


def load_sandvine_mobile_zoom():
    """Load and return sandvine mobile zoom dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "mobile_zoom.csv"))


def load_sandvine_snapchat():
    """Load and return sandvine snapchat dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "snapchat.csv"))


def load_sandvine_social_networking():
    """Load and return sandvine social networking dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "social_networking.csv"))


def load_sandvine_tiktok():
    """Load and return sandvine tiktok dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "tiktok.csv"))


def load_sandvine_video_streaming():
    """Load and return sandvine video streaming dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "video_streaming.csv"))


def load_sandvine_vpn_and_security():
    """Load and return sandvine vpn and security dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "vpn_and_security.csv"))


def load_sandvine_web():
    """Load and return sandvine web dataset."""
    return load_csv_dataset_from_resources(path.join("sandvine", "web.csv"))
