from traffic_weaver.datasets._base import RemoteFileMetadata, load_csv_dataset_from_remote, load_dataset_description

DATASET_FOLDER = 'mix'


def mix_dataset_description():
    """Get description of this dataset."""
    return load_dataset_description("mix.txt")


def fetch_mix_bologna_daily(**kwargs):
    """Load and return MIX Bologna daily dataset."""
    remote = RemoteFileMetadata(filename="MIX-bologna_daily_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49072606",
                                checksum="9f0970dfeca937818f40eab2fbc62c72a4270b6d93d4b2b9d91e3db0f6092c2a")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename='MIX-bologna_daily',
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_bologna_weekly(**kwargs):
    """Load and return MIX Bologna weekly dataset."""
    remote = RemoteFileMetadata(filename="MIX-bologna_weekly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49072609",
                                checksum="182622599376193d497afae984d5eaf6540cb65e851221631bed6481d038cecb")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename='MIX-bologna_weekly',
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_bologna_monthly(**kwargs):
    """Load and return MIX Bologna monthly dataset."""
    remote = RemoteFileMetadata(filename="MIX-bologna_monthly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49072972",
                                checksum="6bd221d5a70293f795c3e999614ff6658b3236de7e5830457654e4b56c22fc77")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename='MIX-bologna_monthly',
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_bologna_yearly(**kwargs):
    """Load and return MIX Bologna yearly dataset."""
    remote = RemoteFileMetadata(filename="MIX-bologna_yearly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49072612",
                                checksum="48d898e3ca246fe8f5f7a917bdcf3cd026ea371837936ed5acf1344bdf411d61")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename='MIX-bologna_yearly',
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_milan_daily(**kwargs):
    """Load and return MIX Milan daily dataset."""
    remote = RemoteFileMetadata(filename="MIXmilana_daily_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49072615",
                                checksum="fbd873d3f91896d992508b00f42c98ac44d1a03ad42551fb09903168831e42f1")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename='MIX-milan_daily',
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_milan_weekly(**kwargs):
    """Load and return MIX Milan weekly dataset."""
    remote = RemoteFileMetadata(filename="MIX-milan_weekly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49072621",
                                checksum="ffb4034f92db1a713999d97bede2556628c593ebd5d750308e495843129f8dd2")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename='MIX-milan_weekly',
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_milan_monthly(**kwargs):
    """Load and return MIX Milan monthly dataset."""
    remote = RemoteFileMetadata(filename="MIX-milan-monthly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49072618",
                                checksum="c97d78d681f758f4301c5d44882165607f573fe1d5459f52f79af00d8b996a65")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename='MIX-milan_monthly',
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_milan_yearly(**kwargs):
    """Load and return MIX Milan yearly dataset."""
    remote = RemoteFileMetadata(filename="MIX-milan_yearly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49072624",
                                checksum="1bd8dcb96b290f68aa71abe30f4e465138970dad6c8ab88d019e72a389722cc5")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename='MIX-milan_yearly',
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_palermo_daily(**kwargs):
    """Load and return MIX Palermo daily dataset."""
    remote = RemoteFileMetadata(filename="MIXmpalermo_daily_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49072633",
                                checksum="3b1f43504f26c38e5c81247da20ce9194fc138ecb4e549f3c3af35d9bc60fb9e")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename='MIX-palermo_daily',
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_palermo_weekly(**kwargs):
    """Load and return MIX Palermo weekly dataset."""
    remote = RemoteFileMetadata(filename="MIX-palermo_weekly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49072639",
                                checksum="51f20dbde61223214a2e77a0968870b578da225afa4978758fd1b6acd6fc6423")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename='MIX-palermo_weekly',
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_palermo_monthly(**kwargs):
    """Load and return MIX Palermo monthly dataset."""
    remote = RemoteFileMetadata(filename="MIX-palermo-monthly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49072636",
                                checksum="0f747e7e1fa73b1bdd54c3a2fc3d0b2cee87f43cbeca0f3f41c0248df8438a6d")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename='MIX-palermo_monthly',
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_palermo_yearly(**kwargs):
    """Load and return MIX Palermo yearly dataset."""
    remote = RemoteFileMetadata(filename="MIX-palermo_yearly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49072630",
                                checksum="182e965cb777a4c26cf31e7a270dabb894f6012fc422694ef2187a0f7c759f76")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename='MIX-palermo_yearly',
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)
