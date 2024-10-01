from traffic_weaver.datasets._base import RemoteFileMetadata, load_csv_dataset_from_remote, load_dataset_description

DATASET_FOLDER = "mix-it"


def mix_it_dataset_description():
    """Get description of this dataset."""
    return load_dataset_description("mix_it.md")


def fetch_mix_it_bologna_daily(**kwargs):
    """Load and return MIX Bologna daily dataset."""
    remote = RemoteFileMetadata(filename="mix-it-bologna_daily_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49543767",
                                checksum="9f0970dfeca937818f40eab2fbc62c72a4270b6d93d4b2b9d91e3db0f6092c2a")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="mix-it-bologna_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_it_bologna_weekly(**kwargs):
    """Load and return MIX Bologna weekly dataset."""
    remote = RemoteFileMetadata(filename="mix-it-bologna_weekly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49543773",
                                checksum="b852c310c6f543659e7fa194d19c3a6cadd7de6b47f184843909acfee98cb781")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="mix-it-bologna_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_it_bologna_monthly(**kwargs):
    """Load and return MIX Bologna monthly dataset."""
    remote = RemoteFileMetadata(filename="mix-it-bologna_monthly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49543770",
                                checksum="e29881dc7c44782da783f70d9123548c4aeb75bdcd82f31e6d8622d51617db99")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="mix-it-bologna_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_it_bologna_yearly(**kwargs):
    """Load and return MIX Bologna yearly dataset."""
    remote = RemoteFileMetadata(filename="mix-it-bologna_yearly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49543776",
                                checksum="0cbd8c03d46f0ae76ab958fca384f3d5692fefcbbb4c99995d17d5a86e5bd401")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="mix-it-bologna_yearly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_it_milan_daily(**kwargs):
    """Load and return MIX Milan daily dataset."""
    remote = RemoteFileMetadata(filename="mix-it-milan_daily_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49543779",
                                checksum="fbd873d3f91896d992508b00f42c98ac44d1a03ad42551fb09903168831e42f1")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="mix-it-milan_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_it_milan_weekly(**kwargs):
    """Load and return MIX Milan weekly dataset."""
    remote = RemoteFileMetadata(filename="mix-it-milan_weekly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49543788",
                                checksum="a38147bb0a4d857ac80f6440f64d7c5983faf326bae6433cad7a4b05fa98afab")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="mix-it-milan_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_it_milan_monthly(**kwargs):
    """Load and return MIX Milan monthly dataset."""
    remote = RemoteFileMetadata(filename="mix-it-milan-monthly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49543782",
                                checksum="30d6b7c5b8bbfbff92992052cde3ac9ed3b31aa47103fd5fdc6ab34a6ca9ef59")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="mix-it-milan_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_it_milan_yearly(**kwargs):
    """Load and return MIX Milan yearly dataset."""
    remote = RemoteFileMetadata(filename="mix-it-milan_yearly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49543791",
                                checksum="d3d925d1ffae871a65a7ef4f158722953352cc5f2e0a4165880c69115c56f17c")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="mix-it-milan_yearly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_it_palermo_daily(**kwargs):
    """Load and return MIX Palermo daily dataset."""
    remote = RemoteFileMetadata(filename="mix-it-palermo_daily_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49543794",
                                checksum="3b1f43504f26c38e5c81247da20ce9194fc138ecb4e549f3c3af35d9bc60fb9e")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="mix-it-palermo_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_it_palermo_weekly(**kwargs):
    """Load and return MIX Palermo weekly dataset."""
    remote = RemoteFileMetadata(filename="mix-it-palermo_weekly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49543800",
                                checksum="a239292b440a6f9cf6f4ce1b5b8766164c6aafca9b12f5352fb56247bc9a28ce")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="mix-it-palermo_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_it_palermo_monthly(**kwargs):
    """Load and return MIX Palermo monthly dataset."""
    remote = RemoteFileMetadata(filename="mix-it-palermo-monthly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49543797",
                                checksum="8b94d22ef455ba61d16557b2c587db7aee030e052da7c8c3da9507a5f1074e6b")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="mix-it-palermo_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_mix_it_palermo_yearly(**kwargs):
    """Load and return MIX Palermo yearly dataset."""
    remote = RemoteFileMetadata(filename="mix-it-palermo_yearly_2024-09_04.csv",
                                url="https://figshare.com/ndownloader/files/49543803",
                                checksum="b3f0d9240803edfa6000086df38613b719b85eaa9c39d5f031fdfb3c9bee3e4f")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="mix-it-palermo_yearly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)
