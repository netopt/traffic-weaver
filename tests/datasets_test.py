from unittest import mock

import pytest
from traffic_weaver.datasets import load_mobile_video
from numpy.testing import assert_array_equal


@pytest.fixture
def mocked_dataset_file():
    data = """
        {
            "mobile_video": "[1, 2, 3, 4]"
        }
    """
    return mock.mock_open(read_data=data)


@pytest.fixture
def expected_content():
    return [1, 2, 3, 4]


def test_open_dataset_file_by_method(mocked_dataset_file, expected_content):
    with mock.patch('builtins.open', mocked_dataset_file):
        x, y = load_mobile_video()
        assert_array_equal(y, expected_content)
