"""Config for tests"""


import pytest
import sys
from cbc_sdk import CBCloudAPI
from tests.fixtures.cbc_sdk_mock import CBCSDKMock
import tests.fixtures.phantom_mock as phantom_mock


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch):
    """Mocks CBC SDK for unit tests"""
    cbc_sdk = CBCloudAPI(url="https://example.com", org_key="test", token="abcd/1234", ssl_verify=False)
    return CBCSDKMock(monkeypatch, cbc_sdk)


pytest_plugins = [
   "tests.fixtures.cbc_sdk_mock_responses",
]


# This is done to allow importing Splunk SOAR's classes from the test harness
module = type(sys)('phantom')
module.__spec__ = phantom_mock.__spec__
module.__path__ = phantom_mock.__path__
module.__loader__ = phantom_mock.__loader__
sys.modules["phantom"] = module
