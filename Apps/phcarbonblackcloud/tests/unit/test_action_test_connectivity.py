"""Tests for test connectivity"""
import pytest
import sys
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_test_connectivity import CheckConnectivityAction

from tests.fixtures.cbc_sdk_mock import CBCSDKMock
from cbc_sdk.errors import UnauthorizedError, ConnectionError, ObjectNotFoundError


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


def test_action_test_connectivity_exist():
    """Test if action called"""
    obj = CBCSplunk()
    obj.handle_action({})
    assert "actions.action_test_connectivity" in sys.modules.keys()
    assert "CheckConnectivityAction" in dir(sys.modules["actions.action_test_connectivity"])


def test_successful_connectivity(cbcsdk_mock, get_no_alert_response):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = CheckConnectivityAction(obj, {})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/alerts/_search", get_no_alert_response
    )

    action_result = action.call()
    assert obj.progress_message == "Connection successful."
    assert action_result == phantom.APP_SUCCESS


def test_unauthorized_error_connectivity(cbcsdk_mock):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = CheckConnectivityAction(obj, {})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/alerts/_search",
        lambda *_: MockException(UnauthorizedError),
    )
    action_result = action.call()
    assert obj.progress_message == "Bad Custom Connector ID or key."
    assert action_result == phantom.APP_ERROR


def test_connection_error_connectivity(cbcsdk_mock):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = CheckConnectivityAction(obj, {})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/alerts/_search",
        lambda *_: MockException(ConnectionError),
    )
    action_result = action.call()
    assert obj.progress_message == "Could not connect to CBC. Check the Server URL."
    assert action_result == phantom.APP_ERROR


def test_object_not_found_connectivity(cbcsdk_mock):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = CheckConnectivityAction(obj, {})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/alerts/_search",
        lambda *_: MockException(ObjectNotFoundError),
    )
    action_result = action.call()
    assert obj.progress_message == "Invalid ORG key."
    assert action_result == phantom.APP_ERROR


def test_other_error_connectivity(cbcsdk_mock):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = CheckConnectivityAction(obj, {})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/alerts/_search",
        lambda *_: MockException(Exception),
    )
    action_result = action.call()
    assert "Unknown error" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_no_cbc_connectivity(cbcsdk_mock):
    """Test action with no cbc"""
    obj = CBCSplunk()
    action = CheckConnectivityAction(obj, {})
    action.cbc = None
    action_result = action.call()
    assert obj.progress_message == "Please configure all connection parameters."
    assert action_result == phantom.APP_ERROR
