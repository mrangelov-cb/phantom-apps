"""Tests for dismiss alert"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_dismiss_alert import DismissAlertAction

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


def test_dismiss_alert_success(cbcsdk_mock, return_single_alert_object):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = DismissAlertAction(obj, {"alert_id": "27a278d2150911eb86f1011a55e73b72"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/alerts/27a278d2150911eb86f1011a55e73b72",
        return_single_alert_object,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/alerts/27a278d2150911eb86f1011a55e73b72/workflow",
        {"request_id": "497ABX"},
    )
    action_result = action.call()
    assert obj.progress_message == "Alert dismissed 27a278d2150911eb86f1011a55e73b72."
    assert action_result == phantom.APP_SUCCESS


def test_dismiss_alert_missing_alert_id(cbcsdk_mock, return_single_alert_object):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = DismissAlertAction(obj, {})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/alerts/27a278d2150911eb86f1011a55e73b72",
        return_single_alert_object,
    )
    action_result = action.call()
    assert obj.progress_message == "Missing alert id."
    assert action_result == phantom.APP_ERROR


def test_dismiss_alert_exception(cbcsdk_mock, return_single_alert_object):
    """Test action - exception"""

    def post_resp(*args, **kwargs):
        return MockException(Exception)

    obj = CBCSplunk()
    action = DismissAlertAction(obj, {"alert_id": "27a278d2150911eb86f1011a55e73b72"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/alerts/27a278d2150911eb86f1011a55e73b72",
        return_single_alert_object,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/alerts/27a278d2150911eb86f1011a55e73b72/workflow",
        post_resp,
    )
    action_result = action.call()
    assert "Could not dismiss alert 27a278d2150911eb86f1011a55e73b72" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_dismiss_alert_no_cbc():
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = DismissAlertAction(obj, {"alert_id": "27a278d2150911eb86f1011a55e73b72"})
    action.cbc = None
    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."
