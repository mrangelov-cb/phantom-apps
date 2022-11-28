"""Tests for list processes"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_list_processes import ListProcessesAction

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


def test_list_processes_success(
    cbcsdk_mock,
    get_device_object,
    get_session_init_object,
    get_session_poll_object,
    get_list_proc_start_object,
    get_list_proc_end_object,
):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = ListProcessesAction(obj, {"device_id": 354648})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/354648", get_device_object)
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/liveresponse/sessions",
        get_session_init_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468",
        get_session_poll_object,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands",
        get_list_proc_start_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/10",
        get_list_proc_end_object,
    )
    cbcsdk_mock.mock_request(
        "DELETE", "/appservices/v6/orgs/test/liveresponse/sessions/1:2468", None
    )

    action_result = action.call()
    assert obj.progress_message == "List Processes successfully retrieved."
    assert action_result == phantom.APP_SUCCESS
    assert len(obj.action_results[0].get_data()) == 3


def test_list_processes_missing_device_id(cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = ListProcessesAction(obj, {})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "Missing device id."
    assert action_result == phantom.APP_ERROR


def test_list_processes_exception(cbcsdk_mock):
    """Test action - exception"""

    def post_resp(url, *args):
        return MockException(Exception)

    obj = CBCSplunk()
    action = ListProcessesAction(obj, {"device_id": 354648})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/354648", post_resp)
    action_result = action.call()
    assert "Could not get processes for 354648" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_list_processes_no_cbc():
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = ListProcessesAction(obj, {"device_id": 354648})
    action.cbc = None
    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."
