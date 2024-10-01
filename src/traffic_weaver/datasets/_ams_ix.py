from traffic_weaver.datasets._base import RemoteFileMetadata, load_csv_dataset_from_remote, load_dataset_description

DATASET_FOLDER = 'ams-ix'


def ams_ix_dataset_description():
    """Get description of this dataset."""
    return load_dataset_description("ams_ix.md")


def fetch_ams_ix_yearly_by_day(**kwargs):
    """Load and return AMS-IX yearly by day dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-yearly-by-day_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549962",
                                checksum="56d31d4f0469599a80b5e952d484fe7b6fde8aec0a88ae6fc35e8b450e078447")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-yearly-by-day",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_daily(**kwargs):
    """Load and return AMS-IX daily dataset."""
    remote = RemoteFileMetadata(filename="ams-ix_daily_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549860",
                                checksum="2f606b0adecbbae50727539cebd2d107c6d5a962298d34cbeb1bf4b7cab0d3a9")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix_daily", dataset_folder=DATASET_FOLDER,
                                        validate_checksum=True, **kwargs)


def fetch_ams_ix_weekly(**kwargs):
    """Load and return AMS-IX weekly dataset."""
    remote = RemoteFileMetadata(filename="ams-ix_weekly_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549866",
                                checksum="2273530aeca328721764491d770a8259b255df5c028c899aa5c6c3b2001e33f4")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix_weekly", dataset_folder=DATASET_FOLDER,
                                        validate_checksum=True, **kwargs)


def fetch_ams_ix_monthly(**kwargs):
    """Load and return AMS-IX monthly dataset."""
    remote = RemoteFileMetadata(filename="ams-ix_monthly_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549863",
                                checksum="a8aeaabbd9089bf25455ab8d164f69a868032f7f0ba2c1a771bf5d04a2e16581")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix_monthly", dataset_folder=DATASET_FOLDER,
                                        validate_checksum=True, **kwargs)


def fetch_ams_ix_yearly_input(**kwargs):
    """Load and return AMS-IX yearly input dataset."""
    remote = RemoteFileMetadata(filename="ams-ix_yearly-input_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549869",
                                checksum="19fe5560606477ccacead54a993e856be45d59b5beb1dab819b612a437a301d3")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix_yearly_input",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_yearly_output(**kwargs):
    """Load and return AMS-IX yearly output dataset."""
    remote = RemoteFileMetadata(filename="ams-ix_yearly-output_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549872",
                                checksum="9f67208e8b6155634bb517d78c796e5344c1400d174e8ab62a65580a24b553f5")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix_yearly_output",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_isp_yearly_by_day(**kwargs):
    """Load and return AMS-IX ISP yearly by day dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-isp-yearly-by-day_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549941",
                                checksum="d9efb4dd7158c223c45ea2c66f2455ed2f15c5a94d8db437ad0cc6e29c8b0e03")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-isp-yearly-by-day",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_isp_daily(**kwargs):
    """Load and return AMS-IX ISP daily dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-isp_daily_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549926",
                                checksum="b839bef4522fdfd19eee291f713834caf812a1da20d871adb429b03c10c3b692")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-isp_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_isp_weekly(**kwargs):
    """Load and return AMS-IX ISP weekly dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-isp_weekly_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549929",
                                checksum="02ec0fbe6fdd0429ef79427a9b3c1210a0e912cb8b2d146305fdab35c9c22928")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-isp_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_isp_monthly(**kwargs):
    """Load and return AMS-IX ISP monthly dataset."""
    remote = RemoteFileMetadata(filename="aams-ix-isp_monthly_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549932",
                                checksum="11cb8057c1984072285c841553e478cacb0672e9153e4d72930c5af40c899875")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-isp_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_isp_yearly_input(**kwargs):
    """Load and return AMS-IX ISP yearly input dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-isp_yearly-input_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549935",
                                checksum="d6cac12520f3ebcb33b04e2a096106b42fa082510187f83d36e53dd4a81d96a0")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-isp_yearly_input",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_isp_yearly_output(**kwargs):
    """Load and return AMS-IX ISP yearly output dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-isp_yearly-output_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549938",
                                checksum="b7ec0614c03704388528005be5899948a84a70c418c3fd7de8bddc1d0d4db0c1")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-isp_yearly_output",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_grx_yearly_by_day(**kwargs):
    """Load and return AMS-IX GRX yearly by day dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-grx-yearly-by-day_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549890",
                                checksum="aff17528c4b3855cfb52bc42d1d67c1cb8d24fc44153f6def0febe30ce7c5892")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-grx-yearly-by-day",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_grx_daily(**kwargs):
    """Load and return AMS-IX GRX daily dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-grx_daily_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549875",
                                checksum="cc69b78859fcf8a328bde5cf407decf01493930efa1d31397af56b8060895c15")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-grx_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_grx_weekly(**kwargs):
    """Load and return AMS-IX GRX weekly dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-grx_weekly_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549881",
                                checksum="e7b2afd06e4e5302ad9745cf6887ee73f76d09cce8ba10167b2152630e544058")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-grx_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_grx_monthly(**kwargs):
    """Load and return AMS-IX GRX monthly dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-grx_monthly_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549878",
                                checksum="4a9e45d2bf647c6eba6b2550c2d7b06da363e736a8d801763dba5244ed8f491d")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-grx_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_grx_yearly_input(**kwargs):
    """Load and return AMS-IX GRX yearly input dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-grx_yearly-input_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549884",
                                checksum="e06a0ab9073057e618e7d41cf3cb4171650ee22bd5411a9bc95cd25104c44bc4")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-grx_yearly_input",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_grx_yearly_output(**kwargs):
    """Load and return AMS-IX GRX yearly output dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-grx_yearly-output_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549887",
                                checksum="e2d2b1dda84328effca9b461f07a99afd598a6a13011a2c41338bf5a347c5d70")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-grx_yearly_output",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_i_ipx_yearly_by_day(**kwargs):
    """Load and return AMS-IX I-IPX yearly by day dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-i-ipx-yearly-by-day_2024-09-21.csv",
                                url="https://figshare.com/ndownloader/files/49549917",
                                checksum="eee61d792e8427e5d4ea55b7e881acd646c676a8681270b63485102ca4062ebf")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-i-ipx-yearly-by-day",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_i_ipx_daily(**kwargs):
    """Load and return AMS-IX I-IPX daily dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-i-ipx_daily_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549893",
                                checksum="d9752817c7b635dab6cddd329e0d4238d7e94199de242d9d3327208c77cd3aa2")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-i-ipx_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_i_ipx_weekly(**kwargs):
    """Load and return AMS-IX I-IPX weekly dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-i-ipx_weekly_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549896",
                                checksum="13e4cc3bb2124e03c58066e25d4beac8a323c7cfde6ad2ec6219d8798b81f69c")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-i-ipx_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_i_ipx_monthly(**kwargs):
    """Load and return AMS-IX I-IPX monthly dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-i-ipx_monthly_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549899",
                                checksum="665b8841c0858e86db9aa8144d9404c175754055da5d1d23047f77f850c5a7ff")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-i-ipx_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_i_ipx_yearly_input(**kwargs):
    """Load and return AMS-IX I-IPX yearly input dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-i-ipx_yearly-input_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549902",
                                checksum="8549d3cd62a3b8074aac82450676fe359bcc679c897c487a8519322123f4bd93")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-i-ipx_yearly_input",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_i_ipx_yearly_output(**kwargs):
    """Load and return AMS-IX I-IPX yearly output dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-i-ipx_yearly-output_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549905",
                                checksum="450f50f262543c266503de7f89c9c5c5b07fdb5e40c0c39e82600e47e5d41ff8")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-i-ipx_yearly_output",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_i_ipx_diameter_daily(**kwargs):
    """Load and return AMS-IX I-IPX diameter daily dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-i-ipx-diameter_daily_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549908",
                                checksum="abbe54c558d3cc954f361d7f5eab66c194ec6f0866332410386ab39678ee15c2")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-i-ipx-diameter_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_i_ipx_diameter_weekly(**kwargs):
    """Load and return AMS-IX I-IPX diameter weekly dataset."""
    remote = RemoteFileMetadata(filename="./ams-ix-i-ipx-diameter_weekly_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549914",
                                checksum="2b5b622d041c4ad1f0e282420620b96da9ddee01c14eaf4457319515bbb1d286")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="./ams-ix-i-ipx-diameter_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_i_ipx_diameter_monthly(**kwargs):
    """Load and return AMS-IX I-IPX diameter monthly dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-i-ipx-diameter_monthly_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549911",
                                checksum="cebf44d0c585a0685e3446af44d001bddf36e975f8963f60fb36d0c0583eb82b")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-i-ipx-diameter_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_i_ipx_diameter_yearly_input(**kwargs):
    """Load and return AMS-IX I-IPX diameter yearly input dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-i-ipx-diameter_yearly-input_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549920",
                                checksum="eba37cdf6131d6d9ddd668e919ab5ef5f222171cf3f33170b9aa9af158e9025e")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-i-ipx-diameter_yearly_input.csv",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_i_ipx_diameter_yearly_output(**kwargs):
    """Load and return AMS-IX I-IPX diameter yearly output dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-i-ipx-diameter_yearly-output_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549923",
                                checksum="1a098f35c6b541569f0a5e3cbec5cafc020b98b038e0a3f2276de1b30231aed1")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-i-ipx-diameter_yearly_output.csv",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_nawas_anti_ddos_daily(**kwargs):
    """Load and return AMS-IX NAWAS anti-DDoS daily dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-nawas-anti-ddos_daily_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549944",
                                checksum="89682274e43228392120f1c28aaad1e2daa8c3781d1667944d7156e73c4363e2")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-nawas-anti-ddos_daily",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_nawas_anti_ddos_weekly(**kwargs):
    """Load and return AMS-IX NAWAS anti-DDoS weekly dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-nawas-anti-ddos_weekly_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549950",
                                checksum="1b70c8e7701d2fe6a5d737c3b46cfeeff1db1d577fe06ff67cefba788bdb807b")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-nawas-anti-ddos_weekly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_nawas_anti_ddos_monthly(**kwargs):
    """Load and return AMS-IX NAWAS anti-DDoS monthly dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-nawas-anti-ddos_monthly_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549947",
                                checksum="3d8332ac9761751604ce9f21ff03152a6051d8e2e7a3de512fb1cb3869746f36")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-nawas-anti-ddos_monthly",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_nawas_anti_ddos_yearly_input(**kwargs):
    """Load and return AMS-IX NAWAS anti-DDoS yearly input dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-nawas-anti-ddos_yearly-input_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549953",
                                checksum="3cc39c26e667b09c1eae6e31665867e1aa89dbb9e614660a7705a385222734d1")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-nawas-anti-ddos_yearly_input",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)


def fetch_ams_ix_nawas_anti_ddos_yearly_output(**kwargs):
    """Load and return AMS-IX NAWAS anti-DDoS yearly output dataset."""
    remote = RemoteFileMetadata(filename="ams-ix-nawas-anti-ddos_yearly-output_2024-09-22.csv",
                                url="https://figshare.com/ndownloader/files/49549956",
                                checksum="fa4f9c6e887aa9ecf1e98df856a894b125e892e773129a6e632549248f338776")
    return load_csv_dataset_from_remote(remote=remote, dataset_filename="ams-ix-nawas-anti-ddos_yearly_output",
                                        dataset_folder=DATASET_FOLDER, validate_checksum=True, **kwargs)
