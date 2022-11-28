"""Tests for quarantine a device"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_quarantine_device import QuarantineAction

from tests.fixtures.cbc_sdk_mock import CBCSDKMock


class MockException:
    """MockException class for Exceptions"""

    def __init__(self, exc_type, *args, **kwargs):
        """Raising exception"""
        raise exc_type(args, kwargs)


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


def test_quarantine_device_success(cbcsdk_mock, get_device_object):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = QuarantineAction(obj, {"device_id": 354648})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/354648", get_device_object)
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/device_actions", None)

    action_result = action.call()
    assert obj.progress_message == "Device quarantined successfully."
    assert action_result == phantom.APP_SUCCESS


def test_quarantine_device_already_quarantined(cbcsdk_mock, get_quarantined_device_object):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = QuarantineAction(obj, {"device_id": 354648})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/354648", get_quarantined_device_object
    )
    action_result = action.call()
    assert obj.progress_message == "The device is already quarantined."
    assert action_result == phantom.APP_SUCCESS


def test_quarantine_device_missing_alert_id(cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = QuarantineAction(obj, {})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "Missing device id."
    assert action_result == phantom.APP_ERROR


def test_quarantine_device_exception(cbcsdk_mock, get_device_object):
    """Test action - exception"""

    def post_resp(*args, **kwargs):
        return MockException(Exception)

    obj = CBCSplunk()
    action = QuarantineAction(obj, {"device_id": 354648})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/354648", get_device_object)
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/device_actions", post_resp)

    action_result = action.call()
    assert "Could not quarantine 354648" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_quarantine_device_no_cbc():
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = QuarantineAction(obj, {"device_id": 354648})
    action.cbc = None
    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."
