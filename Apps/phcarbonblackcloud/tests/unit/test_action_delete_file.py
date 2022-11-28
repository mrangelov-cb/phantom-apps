"""Tests for delete file"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_delete_file import DeleteFileAction
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


def test_delete_file_success(
    monkeypatch,
    cbcsdk_mock,
    get_device_object,
    get_session_init_object,
    get_session_poll_object,
    delete_file_start_resp_object,
    delete_file_end_resp_object,
):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = DeleteFileAction(obj, {"device_id": 354648, "file_name": "test.txt"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/354648", get_device_object
    )
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
        delete_file_start_resp_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/3",
        delete_file_end_resp_object,
    )
    cbcsdk_mock.mock_request(
        "DELETE", "/appservices/v6/orgs/test/liveresponse/sessions/1:2468", None
    )
    action_result = action.call()
    assert obj.progress_message == "File successfully deleted."
    assert action_result == phantom.APP_SUCCESS


def test_delete_file_missing_file_name(monkeypatch, cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = DeleteFileAction(obj, {"device_id": 354648})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "No file_name provided."
    assert action_result == phantom.APP_ERROR


def test_delete_file_missing_device_id(monkeypatch, cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = DeleteFileAction(obj, {"file_name": "test"})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "Missing device id."
    assert action_result == phantom.APP_ERROR


def test_delete_file_exception(monkeypatch, cbcsdk_mock):
    """Test action - exception"""

    def post_resp(url, *args):
        return MockException(Exception)

    obj = CBCSplunk()
    action = DeleteFileAction(obj, {"device_id": 354648, "file_name": "test"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/354648", post_resp
    )
    action_result = action.call()
    assert "Could not delete file" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_delete_file_no_cbc(monkeypatch, cbcsdk_mock):
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = DeleteFileAction(obj, {"device_id": 354648, "file_name": "test"})
    action.cbc = None
    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."


def test_delete_file_fail_to_start_lr(monkeypatch, cbcsdk_mock, get_device_object):
    """Test action with correct parameters - fail to start lr"""

    def post_resp(url, *args):
        return MockException(Exception)

    obj = CBCSplunk()
    action = DeleteFileAction(obj, {"device_id": 354648, "file_name": "test.txt"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/354648", get_device_object
    )
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/liveresponse/sessions", post_resp
    )
    action_result = action.call()
    assert "Could not establish LR session" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_delete_file_fail_to_delete_file_contents(
    monkeypatch,
    cbcsdk_mock,
    get_device_object,
    get_session_init_object,
    get_session_poll_object,
    delete_file_start_resp_object,
):
    """Test action with correct parameters - delete file contents exception"""

    def post_resp(url, *args):
        return MockException(Exception)

    obj = CBCSplunk()
    action = DeleteFileAction(obj, {"device_id": 354648, "file_name": "test.txt"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/354648", get_device_object
    )
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
        delete_file_start_resp_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/3",
        post_resp,
    )
    action_result = action.call()
    assert "Could not delete file contents" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_delete_file_fail_to_delete_missing_file_contents(
    monkeypatch,
    cbcsdk_mock,
    get_device_object,
    get_session_init_object,
    get_session_poll_object,
    delete_file_start_resp_object,
    delete_file_error_resp_object,
):
    """Test action with correct parameters - non-existent file"""
    obj = CBCSplunk()
    action = DeleteFileAction(obj, {"device_id": 354648, "file_name": "test.txt"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/354648", get_device_object
    )
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
        delete_file_start_resp_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/3",
        delete_file_error_resp_object,
    )
    cbcsdk_mock.mock_request(
        "DELETE", "/appservices/v6/orgs/test/liveresponse/sessions/1:2468", None
    )
    action_result = action.call()
    assert "No such file" in obj.progress_message
    assert action_result == phantom.APP_ERROR
