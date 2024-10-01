from traffic_weaver.datasets._base import RemoteFileMetadata, load_csv_dataset_from_remote, load_dataset_description

DATASET_FOLDER = 'ix-br'


def ix_br_dataset_description():
    """Get ix_br_dataset_description of this dataset"""
    return load_dataset_description("ix_br.md")


def fetch_ix_br_aggregated_daily(**kwargs):
    """Load and return IX-BR aggregated daily dataset."""
    remote = RemoteFileMetadata(filename="ix-br-aggregated_daily-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49549854",
                                checksum="23ab0b2acca20587a4946b748e0013125f7a5ab575a6974437019a1916b565ed")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-aggregated_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_aggregated_weekly(**kwargs):
    """Load and return IX-BR aggregated weekly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-aggregated_weekly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49549977",
                                checksum="47ce1cfd63642a280eaa0710b3c9709fb80379eee28025925db45044f8e08afd")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-aggregated_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_aggregated_monthly(**kwargs):
    """Load and return IX-BR aggregated monthly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-aggregated_monthly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49549974",
                                checksum="24075687089ff5160abca7641aa9cef33098083e8a1e54171f542757ee9cab66")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-aggregated_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_aggregated_yearly(**kwargs):
    """Load and return IX-BR aggregated yearly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-aggregated_yearly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49549980",
                                checksum="13125805a7861db559fb193360f9d674abb5012cfac9868abf79effb583776d9")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-aggregated_yearly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_aggregated_decadely(**kwargs):
    """Load and return IX-BR aggregated decadely dataset."""
    remote = RemoteFileMetadata(filename="ix-br-aggregated_decadely-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49549971",
                                checksum="30f574bf5f4da536b391e076c7cd68a7d39e198731ec95d82d85100152dfc2de")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-aggregated_decadely",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_aracaju_daily(**kwargs):
    """Load and return IX-BR Aracaju daily dataset."""
    remote = RemoteFileMetadata(filename="ix-br-aracaju_daily-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49549983",
                                checksum="6c022b25d8010d04dac176cce5e5f07e76e3269bd93b8fd27ef1ed87d0c0cde1")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-aracaju_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_aracaju_weekly(**kwargs):
    """Load and return IX-BR Aracaju weekly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-aracaju_weekly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49549992",
                                checksum="149726b299f6338cb0f39265bc05e6ae71139901d5550baa167a6ab32fc12b89")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-aracaju_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_aracaju_monthly(**kwargs):
    """Load and return IX-BR Aracaju monthly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-aracaju_monthly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49549989",
                                checksum="cc02eec0b2bde6134ad1ff0415826afc4d5ef55cad0844708d08e622b7ad3722")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-aracaju_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_aracaju_yearly(**kwargs):
    """Load and return IX-BR Aracaju yearly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-aracaju_yearly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49549995",
                                checksum="608c51e6a21cca05836147785a57b21c462d42578dbbb43eb79178c347567002")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-aracaju_yearly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_aracaju_decadely(**kwargs):
    """Load and return IX-BR Aracaju decadely dataset."""
    remote = RemoteFileMetadata(filename="ix-br-aracaju_decadely-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49549986",
                                checksum="cec057400047245346128b8e2e55baf2be2d3ffb2e1d549c4e0467617f415f18")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-aracaju_decadely",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_belem_daily(**kwargs):
    """Load and return IX-BR Belem daily dataset."""
    remote = RemoteFileMetadata(filename="ix-br-belem_daily-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49549998",
                                checksum="ccf95b1cd4d3a4b16f848d90804702273a7f040cfc88fc6908d6caa1949fa6d5")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-belem_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_belem_weekly(**kwargs):
    """Load and return IX-BR Belem weekly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-belem_weekly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550007",
                                checksum="37f0e66e05faf35801d1a32cfe0145ac90ba482aa6ddf77e75e8d1323f3651a3")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-belem_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_belem_monthly(**kwargs):
    """Load and return IX-BR Belem monthly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-belem_monthly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550004",
                                checksum="1561895e780328580366e93ad07483878604752881f34e04c9a65534471ef383")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-belem_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_belem_yearly(**kwargs):
    """Load and return IX-BR Belem yearly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-belem_yearly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550013",
                                checksum="c511fcbe8e7b29c5ab6e147848f8c81641095eacd8072fc955df83475cf6f281")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-belem_yearly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_belem_decadely(**kwargs):
    """Load and return IX-BR Belem decadely dataset."""
    remote = RemoteFileMetadata(filename="ix-br-belem_decadely-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550001",
                                checksum="d503b3c04a887cfeaa532fe972f69d31c1749aa709d1d5df0cabcd82a50ce994")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-belem_decadely",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_brasilia_daily(**kwargs):
    """Load and return IX-BR Brasilia daily dataset."""
    remote = RemoteFileMetadata(filename="ix-br-brasilia_daily-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550010",
                                checksum="4c4a508ca7260e0503f3315bdf986e0ea9b3571656a15e9d9236b50e538fb028")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-brasilia_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_brasilia_weekly(**kwargs):
    """Load and return IX-BR Brasilia weekly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-brasilia_weekly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550019",
                                checksum="fb335060052e889e485cd5468dd02ad371f8fbecdcce2023a460640ddb2ca46f")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-brasilia_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_brasilia_monthly(**kwargs):
    """Load and return IX-BR Brasilia monthly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-brasilia_monthly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550022",
                                checksum="929406c9b8642ab9ed98974a5242400a70fb1cdf96823de567b9e7d908d41b0b")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-brasilia_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_brasilia_yearly(**kwargs):
    """Load and return IX-BR Brasilia yearly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-brasilia_yearly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550025",
                                checksum="bc80492a41164a8f8c0213e460e6dca40476e4ee798cff2d8ea2fad605cf8d2f")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-brasilia_yearly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_brasilia_decadely(**kwargs):
    """Load and return IX-BR Brasilia decadely dataset."""
    remote = RemoteFileMetadata(filename="ix-br-brasilia_decadely-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550016",
                                checksum="161acfe24a14634375024e430586bb53ad4069bf08fadcea1c048f063b15b1bd")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-brasilia_decadely",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_curitiba_daily(**kwargs):
    """Load and return IX-BR Curitiba daily dataset."""
    remote = RemoteFileMetadata(filename="ix-br-curitiba_daily-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550028",
                                checksum="fa8d19c7aef870259922cd0dc44a51056ee58503d4f52892483bd6acd0dad405")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-curitiba_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_curitiba_weekly(**kwargs):
    """Load and return IX-BR Curitiba weekly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-curitiba_weekly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550037",
                                checksum="8811ea7780a2987d4f46270674f1b24a36b888c1ec827985a0e41f3aaa85b57f")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-curitiba_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_curitiba_monthly(**kwargs):
    """Load and return IX-BR Curitiba monthly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-curitiba_monthly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550034",
                                checksum="7f30955046e7faed1b3eaa081ed8a25fcfab2b17050574c08b5548297b459d61")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-curitiba_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_curitiba_yearly(**kwargs):
    """Load and return IX-BR Curitiba yearly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-curitiba_yearly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550040",
                                checksum="ce58090551837acc96a268a51c858932cbed3fa048162d98649791861b46f4d5")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-curitiba_yearly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_curitiba_decadely(**kwargs):
    """Load and return IX-BR Curitiba decadely dataset."""
    remote = RemoteFileMetadata(filename="ix-br-curitiba_decadely-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550031",
                                checksum="157103122da83f3b98f407d47fc550ea29fde7f5656879724b45762ec017b80a")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-curitiba_decadely",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_rio_de_janeiro_daily(**kwargs):
    """Load and return IX-BR Rio de Janeiro daily dataset."""
    remote = RemoteFileMetadata(filename="ix-br-rio-de-janeiro_daily-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550043",
                                checksum="b8afdc89de49cacb0d067c0f01d2a963f3459c9774ea5f40e8aed5821f272904")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-rio-de-janeiro_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_rio_de_janeiro_weekly(**kwargs):
    """Load and return IX-BR Rio de Janeiro weekly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-rio-de-janeiro_weekly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550055",
                                checksum="1b189a5ee6b81782ca41a5e602fe7178c6588fca3129639738e920a037884688")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-rio-de-janeiro_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_rio_de_janeiro_monthly(**kwargs):
    """Load and return IX-BR Rio de Janeiro monthly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-rio-de-janeiro_monthly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550049",
                                checksum="a9efe70a794e226e4cbe3844ea707277c47d1bdbee078ebbd62881ee8eef3154")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-rio-de-janeiro_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_rio_de_janeiro_yearly(**kwargs):
    """Load and return IX-BR Rio de Janeiro yearly dataset."""
    remote = RemoteFileMetadata(filename="ix-br-rio-de-janeiro_yearly-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550052",
                                checksum="052a944f403b579c4613f6a27353898f9f201eea3802b5a21f634f7883cfde00")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-rio-de-janeiro_yearly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ix_br_rio_de_janeiro_decadely(**kwargs):
    """Load and return IX-BR Rio de Janeiro decadely dataset."""
    remote = RemoteFileMetadata(filename="ix-br-rio-de-janeiro_decadely-2024-09-30.csv",
                                url="https://figshare.com/ndownloader/files/49550046",
                                checksum="f683308bc8ac7907668c0a6dc3f09fc6ebb4b12cba5cc726424cd5c68ec2455d")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ix-br-rio-de-janeiro_decadely",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)
