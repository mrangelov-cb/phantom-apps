"""Tests for cbcapp connector"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk

from tests.fixtures.cbc_sdk_mock import CBCSDKMock


class MockException:
    """MockException class for Exceptions"""

    def __init__(self, *args, **kwargs):
        """Raising exception"""
        raise Exception


@pytest.fixture(scope="function")
def cb():
    """Create CBCloudAPI singleton"""
    return CBCloudAPI(
        url="https://example.com", org_key="test", token="abcd/1234", ssl_verify=False
    )


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch, cb):
    """Mocks CBC SDK for unit tests"""
    return CBCSDKMock(monkeypatch, cb)


# ==================================== UNIT TESTS BELOW ====================================


def test_handle_no_action(monkeypatch):
    """Test no action"""
    obj = CBCSplunk()
    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "action does not exist")
    assert obj.handle_action(None) is False
