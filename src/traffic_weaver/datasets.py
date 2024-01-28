r"""Small datasets used in Weaver."""
import json
import os

import numpy as np


def __open_datasets_dict():
    filename = os.path.join(
        os.path.dirname(__file__), "./datasets/example_datasets.json"
    )
    with open(filename) as f:
        dataset_dict = json.load(f)
        return dataset_dict


def __example_dataset(fun):
    def wrapper():
        dataset_name = fun.__name__[fun.__name__.find("_") + 1 :]
        y = np.array(eval(__open_datasets_dict()[dataset_name]))
        x = np.arange(0, len(y))
        return x, y

    return wrapper


@__example_dataset
def load_mobile_video():
    pass


@__example_dataset
def load_mobile_youtube():
    pass


@__example_dataset
def load_mobile_social_media():
    pass


@__example_dataset
def load_fixed_social_media():
    pass


@__example_dataset
def load_tiktok():
    pass


@__example_dataset
def load_snapchat():
    pass


@__example_dataset
def load_mobile_messaging():
    pass


@__example_dataset
def load_mobile_zoom():
    pass


@__example_dataset
def load_measurements():
    pass


@__example_dataset
def load_social_networking():
    pass


@__example_dataset
def load_web():
    pass


@__example_dataset
def load_video_streaming():
    pass


@__example_dataset
def load_cloud():
    pass


@__example_dataset
def load_messaging():
    pass


@__example_dataset
def load_audio():
    pass


@__example_dataset
def load_vpn_and_security():
    pass


@__example_dataset
def load_marketplace():
    pass


@__example_dataset
def load_file_sharing():
    pass


@__example_dataset
def load_gaming():
    pass
