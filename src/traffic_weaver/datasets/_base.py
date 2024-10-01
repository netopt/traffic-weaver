import hashlib
import logging
import os
import pickle
import shutil
import time
import warnings
from collections import namedtuple
from gzip import GzipFile
from importlib import resources
from os import environ, path, makedirs
from tempfile import TemporaryDirectory
from urllib.error import URLError
from urllib.request import urlretrieve

import numpy as np

RESOURCES_DATASETS = 'traffic_weaver.datasets.data'
RESOURCES_DATASETS_DESCRIPTION = 'traffic_weaver.datasets.data_description'

RemoteFileMetadata = namedtuple("RemoteFileMetadata", ["filename", "url", "checksum"])

logger = logging.getLogger(__name__)


def load_dataset(dataset, unpack_dataset_columns=False, **kwargs):
    """Load dataset as np.ndarray of shape (nr_of_samples, 2).

    It is 2D array with each row representing one point in time series.
    The first column is the x-variable and the second column is the y-variable.

    If `unpack_dataset_columns=True` is specified as kwargs, the dataset is unpacked to two separate arrays x and y.

    The list of available datasets is in the `traffic_weaver.datasets.data_description` module.


    Parameters
    ----------
    dataset: str
        Name of the dataset to load.
    unpack_dataset_columns: bool, default=False
        If True, the dataset is unpacked to two separate arrays x and y.

    Returns
    -------
    dataset: np.ndarray of shape (nr_of_samples, 2)
        2D array with each row representing one point in time series.
        The first column is the x-variable and the second column is the y-variable.

    Examples
    --------
    >>> data = load_dataset('sandvine_audio')

    """
    import traffic_weaver.datasets._datasets
    if dataset.startswith("sandvine"):
        fun_name = f"load_{dataset.replace('-', '_')}"
    else:
        fun_name = f"fetch_{dataset.replace('-', '_')}"

    try:
        getattr(traffic_weaver.datasets._datasets, fun_name)
    except AttributeError:
        raise ValueError(f"No such dataset: {dataset}")
    return getattr(traffic_weaver.datasets._datasets, fun_name)(unpack_dataset_columns=unpack_dataset_columns)


def get_data_home(data_home: str = None) -> str:
    """Return the path of the data directory.

    Datasets are stored in '.traffic-weaver-data' directory in the user directory.

    This directory can be changed by setting `TRAFFIC_WEAVER_DATA` environment variable.

    Parameters
    ----------
    data_home: str, default=None
        The path to the data directory. If `None`, the default directory is `.traffic-weaver-data`.

    Returns
    -------
    data_home: str
        The path to the data directory.

    Examples
    --------
    >>> import os
    >>> from traffic_weaver.datasets import get_data_home
    >>> data_home = get_data_home()
    >>> os.path.exists(data_home)
    True
    """
    if data_home is None:
        data_home = environ.get("TRAFFIC_WEAVER_DATA", path.join("~", ".traffic-weaver-data"))
    data_home = path.expanduser(data_home)
    makedirs(data_home, exist_ok=True)
    return data_home


def clear_data_home(data_home: str = None):
    """Remove all files in the data directory.

    Parameters
    ----------
    data_home: str, default=None
        The path to the data directory. If `None`, the default directory is `.traffic-weaver-data`.
    """
    data_home = get_data_home(data_home)
    shutil.rmtree(data_home)


def load_csv_dataset_from_resources(file_name, resources_module=RESOURCES_DATASETS, unpack_dataset_columns=False):
    """Load dataset from resources.

    Parameters
    ----------
    file_name: str
        name of the file to load.
    resources_module: str, default='traffic_weaver.datasets.data'
        The package name where the resources are located.
    unpack_dataset_columns: bool, default=False
        If True, the dataset is unpacked to two separate arrays x and y.

    Returns
    -------
    dataset: np.ndarray of shape (nr_of_samples, 2)
        2D array with each row representing one point in time series.
        The first column is the x-variable and the second column is the y-variable.

    """
    data_path = resources.files(resources_module) / file_name
    data_file = np.loadtxt(data_path, delimiter=',', dtype=np.float64)
    if unpack_dataset_columns:
        return data_file[:, 0], data_file[:, 1]
    else:
        return data_file


def _sha256(path):
    """Calculate the sha256 hash of the file at path."""
    sha256hash = hashlib.sha256()
    chunk_size = 8192
    with open(path, "rb") as f:
        while True:
            buffer = f.read(chunk_size)
            if not buffer:
                break
            sha256hash.update(buffer)
    return sha256hash.hexdigest()


def _fetch_remote(remote: RemoteFileMetadata, dirname=None, n_retries=3, delay=1.0, validate_checksum=True):
    """Download remote dataset into path.

    Fetch a dataset pointed by remote's url, save into path using remote's filename and
    ensure integrity based on the SHA256 Checksum of the downloaded file.

    Parameters
    ----------
    remote: RemoteFileMetadata
        Named tuple containing remote dataset meta information: url, filename, checksum.

    dirname: str
        Directory to save the file to.

    n_retries: int, default=3
        Number of retries when HTTP errors are encountered.

    delay: float, default=1.0
        Number of seconds between retries.

    validate_checksum: bool, default=True
        If True, check the SHA256 checksum of the downloaded file.

    Returns
    -------
    file_path: str
        Full path of the created file.
    """
    file_path = remote.filename if dirname is None else path.join(dirname, remote.filename)

    while True:
        try:
            urlretrieve(remote.url, file_path)
            break
        except (URLError, TimeoutError):
            if n_retries == 0:
                # If no more retries are left, re-raise the caught exception.
                raise
            warnings.warn(f"Retry downloading from url: {remote.url}")
            n_retries -= 1
            time.sleep(delay)

    if validate_checksum:
        checksum = _sha256(file_path)
        if remote.checksum != checksum:
            raise OSError("{} has an SHA256 checksum ({}) "
                          "differing from expected ({}), "
                          "file may be corrupted.".format(file_path, checksum, remote.checksum))
    return file_path


def load_csv_dataset_from_remote(remote: RemoteFileMetadata, dataset_filename, dataset_folder, data_home=None,
                                 download_if_missing: bool = True, download_even_if_available: bool = False,
                                 validate_checksum: bool = True, n_retries=3, delay=1.0, gzip=False,
                                 unpack_dataset_columns=False, ):
    """
    Load a dataset from a remote location in csv.gz format.
    After downloading the dataset it is stored in the cache folder for further use in pickle format.

    Parameters
    ----------
    remote: RemoteFileMetadata
        Named tuple containing remote dataset meta information: url, filename, checksum.
    dataset_filename: str
        Name for the dataset file.
    dataset_folder: str
        Folder in `data_home` where the dataset is stored.
    data_home: str, default=None
        Download cache folder fot the dataset. By default data is stored in `~/.traffic-weaver-data`.
    download_if_missing: bool, default=True
        If False, raise an OSError if the data is not locally available instead of
        trying to download the data from the source.
    download_even_if_available: bool, default=False
        If True, download the data even if it is already available locally.
    validate_checksum: bool, default=True
        If True, check the SHA256 checksum of the downloaded file.
    n_retries: int, default=3
        Number of retries in case of HTTPError or URLError when downloading the data.
    delay: float, default=1.0
        Number of seconds between retries.
    gzip: bool, default=False
        If True, the file is assumed to be compressed in gzip format in the remote.
    unpack_dataset_columns: bool, default=False
        If True, the dataset is unpacked to two separate arrays x and y.

    Returns
    -------
    dataset: np.ndarray of shape (nr_of_samples, 2)
        2D array with each row representing one point in time series.
        The first column is the x-variable and the second column is the y-variable.
    """
    data_home = get_data_home(data_home)

    dataset_dir = path.join(data_home, dataset_folder)
    dataset_file_path = path.join(dataset_dir, dataset_filename)

    available = path.exists(dataset_file_path)

    dataset = None
    if (download_if_missing and not available) or (download_if_missing and download_even_if_available and available):
        os.makedirs(dataset_dir, exist_ok=True)
        with TemporaryDirectory(dir=dataset_dir) as tmp_dir:
            logger.info(f"Downloading {remote.url}")
            archive_path = _fetch_remote(remote, dirname=tmp_dir, n_retries=n_retries, delay=delay,
                                         validate_checksum=validate_checksum)
            if gzip:
                dataset = np.loadtxt(GzipFile(filename=archive_path), delimiter=',', dtype=np.float64)
            else:
                dataset = np.loadtxt(archive_path, delimiter=',', dtype=np.float64)
            dataset_tmp_file_path = path.join(tmp_dir, dataset_filename)
            pickle.dump(dataset, open(dataset_tmp_file_path, "wb"))
            os.rename(dataset_tmp_file_path, dataset_file_path)
    elif not available and not download_if_missing:
        raise OSError("Data not found and `download_if_missing` is False")
    if dataset is None:
        dataset = pickle.load(open(dataset_file_path, "rb"))
    if unpack_dataset_columns:
        return dataset[:, 0], dataset[:, 1]
    else:
        return dataset


def load_dataset_description(datasetsource_filename, resources_module=RESOURCES_DATASETS_DESCRIPTION):
    """Load source of the dataset from filename from resources.

    Parameters
    ----------
    datasetsource_filename: str
        name of the file to load.
    resources_module: str, default='traffic_weaver.datasets.datadescription'
        The package name where the resources are located.

    Returns
    -------
    description: str
        Source of the dataset.

    """
    data_path = resources.files(resources_module) / datasetsource_filename
    return data_path.read_text(encoding='utf-8')
