from traffic_weaver.datasets import (load_dataset, sandvine_dataset_description, mix_it_dataset_description,
                                     ams_ix_dataset_description, ix_br_dataset_description)


def test_descriptions():
    sandvine_dataset_description()
    mix_it_dataset_description()
    ams_ix_dataset_description()
    ix_br_dataset_description()


def test_sandvine():
    datasets = """
        sandvine_audio
        sandvine_cloud
        sandvine_file_sharing
        sandvine_fixed_social_media
        sandvine_gaming
        sandvine_marketplace
        sandvine_measurements
        sandvine_messaging
        sandvine_mobile_messaging
        sandvine_mobile_social_media
        sandvine_mobile_video
        sandvine_mobile_youtube
        sandvine_mobile_zoom
        sandvine_snapchat
        sandvine_social_networking
        sandvine_tiktok
        sandvine_video_streaming
        sandvine_vpn_and_security
        sandvine_web
    """
    for dataset in datasets.splitlines():
        dataset = dataset.strip()
        if dataset:
            load_dataset(dataset)


def test_mix_it():
    datasets = """
        mix-it-bologna_daily
        mix-it-bologna_weekly
        mix-it-bologna_monthly
        mix-it-bologna_yearly
        mix-it-milan_daily
        mix-it-milan_weekly
        mix-it-milan_monthly
        mix-it-milan_yearly
        mix-it-palermo_daily
        mix-it-palermo_weekly
        mix-it-palermo_monthly
        mix-it-palermo_yearly
    """
    for dataset in datasets.splitlines():
        dataset = dataset.strip()
        if dataset:
            load_dataset(dataset)


def test_ams_ix():
    datasets = """
        ams-ix-yearly-by-day
        ams-ix_daily
        ams-ix_weekly
        ams-ix_monthly
        ams-ix_yearly-input
        ams-ix_yearly-output
        ams-ix-isp-yearly-by-day
        ams-ix-isp_daily
        ams-ix-isp_weekly
        ams-ix-isp_monthly
        ams-ix-isp_yearly-input
        ams-ix-isp_yearly-output
        ams-ix-grx-yearly-by-day
        ams-ix-grx_daily
        ams-ix-grx_weekly
        ams-ix-grx_monthly
        ams-ix-grx_yearly-input
        ams-ix-grx_yearly-output
        ams-ix-i-ipx-yearly-by-day
        ams-ix-i-ipx_daily
        ams-ix-i-ipx_weekly
        ams-ix-i-ipx_monthly
        ams-ix-i-ipx_yearly-input
        ams-ix-i-ipx_yearly-output
        ams-ix-i-ipx-diameter_daily
        ams-ix-i-ipx-diameter_weekly
        ams-ix-i-ipx-diameter_monthly
        ams-ix-i-ipx-diameter_yearly-input
        ams-ix-i-ipx-diameter_yearly-output
        ams-ix-nawas-anti-ddos_daily
        ams-ix-nawas-anti-ddos_monthly
        ams-ix-nawas-anti-ddos_weekly
        ams-ix-nawas-anti-ddos_yearly-input
        ams-ix-nawas-anti-ddos_yearly-output
    """
    for dataset in datasets.splitlines():
        dataset = dataset.strip()
        if dataset:
            load_dataset(dataset)


def text_ix_br():
    datasets = """
        ix-br-aggregated_daily
        ix-br-aggregated_weekly
        ix-br-aggregated_monthly
        ix-br-aggregated_yearly
        ix-br-aggregated_decadely
        ix-br-aracaju_daily
        ix-br-aracaju_weekly
        ix-br-aracaju_monthly
        ix-br-aracaju_yearly
        ix-br-aracaju_decadely
        ix-br-belem_daily
        ix-br-belem_weekly
        ix-br-belem_monthly
        ix-br-belem_yearly
        ix-br-belem_decadely
        ix-br-brasilia_daily
        ix-br-brasilia_weekly
        ix-br-brasilia_monthly
        ix-br-brasilia_yearly
        ix-br-brasilia_decadely
        ix-br-curitiba_daily
        ix-br-curitiba_weekly
        ix-br-curitiba_monthly
        ix-br-curitiba_yearly
        ix-br-curitiba_decadely
        ix-br-rio-de-janeiro_daily
        ix-br-rio-de-janeiro_weekly
        ix-br-rio-de-janeiro_monthly
        ix-br-rio-de-janeiro_yearly
        ix-br-rio-de-janeiro_decadely
        """
    for dataset in datasets.splitlines():
        dataset = dataset.strip()
        if dataset:
            load_dataset(dataset)
