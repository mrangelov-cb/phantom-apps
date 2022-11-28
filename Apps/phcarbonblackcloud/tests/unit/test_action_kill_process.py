"""Tests for kill process"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_kill_process import KillProcessAction

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


def test_kill_process_pid_success(
    cbcsdk_mock,
    get_device_object,
    get_session_init_object,
    get_session_poll_object,
    get_list_proc_start_object,
    get_list_proc_end_object,
    get_kill_proc_object
):
    """Test action with correct parameters - pid"""
    called = False

    def post_commands_response(*args):
        nonlocal called
        if not called:
            called = True
            return get_list_proc_start_object
        else:
            return get_kill_proc_object

    obj = CBCSplunk()
    action = KillProcessAction(obj, {"device_id": 354648, "process_pid": 303})
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
        post_commands_response,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/10",
        get_list_proc_end_object,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands",
        post_commands_response,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/16",
        get_kill_proc_object,
    )
    cbcsdk_mock.mock_request(
        "DELETE", "/appservices/v6/orgs/test/liveresponse/sessions/1:2468", None
    )

    action_result = action.call()
    assert obj.progress_message == "Process(es) successfully killed"
    assert action_result == phantom.APP_SUCCESS
    data = obj.action_results[0].get_data()
    assert data[0]["process_pid"] == 303
    assert data[0]["process_killed"] is True


def test_kill_process_name_success(
    cbcsdk_mock,
    get_device_object,
    get_session_init_object,
    get_session_poll_object,
    get_list_proc_start_object,
    get_list_proc_end_object,
    get_kill_proc_object
):
    """Test action with correct parameters - process name"""
    called = False

    def post_commands_response(*args):
        nonlocal called
        if not called:
            called = True
            return get_list_proc_start_object
        else:
            return get_kill_proc_object

    obj = CBCSplunk()
    action = KillProcessAction(obj, {"device_id": 354648, "process_name": "proc1"})
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
        post_commands_response,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/10",
        get_list_proc_end_object,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands",
        post_commands_response,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/16",
        get_kill_proc_object,
    )
    cbcsdk_mock.mock_request(
        "DELETE", "/appservices/v6/orgs/test/liveresponse/sessions/1:2468", None
    )

    action_result = action.call()
    assert obj.progress_message == "Process(es) successfully killed"
    assert action_result == phantom.APP_SUCCESS
    data = obj.action_results[0].get_data()
    assert data[0]["process_pid"] == 303


def test_kill_process_hash_success(
    cbcsdk_mock,
    get_device_object,
    get_session_init_object,
    get_session_poll_object,
    get_list_proc_start_object,
    get_list_proc_end_object,
    get_kill_proc_object,
    get_proc_validation_object,
    get_proc_search_jobs_object,
    start_async_proc_search_object,
    get_proc_search_status_object
):
    """Test action with correct parameters - process name"""
    called = False

    def post_commands_response(*args):
        nonlocal called
        if not called:
            called = True
            return get_list_proc_start_object
        else:
            return get_kill_proc_object

    obj = CBCSplunk()
    action = KillProcessAction(obj, {"device_id": 354648, "process_hash": "proc1"})
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
        "GET",
        "/api/investigate/v1/orgs/test/processes/search_validation",
        get_proc_validation_object,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/processes/search_jobs",
        start_async_proc_search_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v1/orgs/test/processes/search_jobs/test",
        get_proc_search_status_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/processes/search_jobs/test/results",
        get_proc_search_jobs_object,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands",
        post_commands_response,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/10",
        get_list_proc_end_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/16",
        get_kill_proc_object,
    )
    cbcsdk_mock.mock_request(
        "DELETE", "/appservices/v6/orgs/test/liveresponse/sessions/1:2468", None
    )

    action_result = action.call()
    assert obj.progress_message == "Process(es) successfully killed"
    assert action_result == phantom.APP_SUCCESS
    data = obj.action_results[0].get_data()
    assert data[0]["process_pid"] == 303


def test_kill_process_guid_success(
    cbcsdk_mock,
    get_device_object,
    get_session_init_object,
    get_session_poll_object,
    get_list_proc_start_object,
    get_list_proc_end_object,
    get_kill_proc_object,
    get_proc_validation_object,
    get_proc_search_jobs_object,
    start_async_proc_search_object,
    get_proc_search_status_object
):
    """Test action with correct parameters - process name"""
    called = False

    def post_commands_response(*args):
        nonlocal called
        if not called:
            called = True
            return get_list_proc_start_object
        else:
            return get_kill_proc_object

    obj = CBCSplunk()
    action = KillProcessAction(obj, {"device_id": 354648, "process_guid": "proc1"})
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
        "GET",
        "/api/investigate/v1/orgs/test/processes/search_validation",
        get_proc_validation_object,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/api/investigate/v2/orgs/test/processes/search_jobs",
        start_async_proc_search_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v1/orgs/test/processes/search_jobs/test",
        get_proc_search_status_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/api/investigate/v2/orgs/test/processes/search_jobs/test/results",
        get_proc_search_jobs_object,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands",
        post_commands_response,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/10",
        get_list_proc_end_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/16",
        get_kill_proc_object,
    )
    cbcsdk_mock.mock_request(
        "DELETE", "/appservices/v6/orgs/test/liveresponse/sessions/1:2468", None
    )

    action_result = action.call()
    assert obj.progress_message == "Process(es) successfully killed"
    assert action_result == phantom.APP_SUCCESS
    data = obj.action_results[0].get_data()
    assert data[0]["process_pid"] == 303


def test_kill_process_missing_device_id(cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = KillProcessAction(obj, {})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "Missing device id."
    assert action_result == phantom.APP_ERROR


def test_kill_process_exception(cbcsdk_mock):
    """Test action - exception"""

    def post_resp(url, *args):
        return MockException(Exception)

    obj = CBCSplunk()
    action = KillProcessAction(obj, {"device_id": 354648, "process_pid": 1234})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/354648", post_resp)
    action_result = action.call()
    assert "Could not kill process" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_kill_process_no_cbc():
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = KillProcessAction(obj, {"device_id": 354648, "process_pid": 1234})
    action.cbc = None
    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."


def test_kill_process_no_pid(
    cbcsdk_mock,
    get_device_object,
    get_session_init_object,
    get_session_poll_object,
    get_list_proc_start_object,
    get_list_proc_end_object,
    get_kill_proc_wrong_pid_object
):
    """Test action with correct parameters - pid"""
    called = False

    def post_commands_response(*args):
        nonlocal called
        if not called:
            called = True
            return get_list_proc_start_object
        else:
            return get_kill_proc_wrong_pid_object

    obj = CBCSplunk()
    action = KillProcessAction(obj, {"device_id": 354648, "process_pid": 303})
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
        post_commands_response,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands",
        post_commands_response,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/16",
        get_kill_proc_wrong_pid_object,
    )
    cbcsdk_mock.mock_request(
        "DELETE", "/appservices/v6/orgs/test/liveresponse/sessions/1:2468", None
    )

    action_result = action.call()
    assert "Could not kill" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_kill_process_pid_missing_in_list(
    cbcsdk_mock,
    get_device_object,
    get_session_init_object,
    get_session_poll_object,
    get_list_proc_start_object,
    get_list_proc_end_object,
    get_kill_proc_object
):
    """Test action with correct parameters - pid not in process list"""
    obj = CBCSplunk()
    action = KillProcessAction(obj, {"device_id": 354648, "process_pid": 305})
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
    assert obj.progress_message == "Process(es) successfully killed"
    assert action_result == phantom.APP_SUCCESS
    data = obj.action_results[0].get_data()
    assert data[0]["process_pid"] == 305
    assert data[0]["process_killed"] is True


def test_kill_process_fail_lr_session(
    cbcsdk_mock,
    get_device_object,
    get_session_init_object,
    get_session_poll_object,
    get_list_proc_start_object,
    get_list_proc_end_object,
    get_kill_proc_object
):
    """Test action with correct parameters - exception"""
    def post_resp(*args):
        raise MockException(Exception)

    obj = CBCSplunk()
    action = KillProcessAction(obj, {"device_id": 354648, "process_pid": 303})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/354648", get_device_object)
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/liveresponse/sessions",
        post_resp
    )

    action_result = action.call()
    assert "Could not establish LR session" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_kill_process_missing_all_options(cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = KillProcessAction(obj, {"device_id": 123})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "You must provide process_pid or process_name or process_hash or process_guid"
    assert action_result == phantom.APP_ERROR


def test_kill_process_fail_to_kill(
    cbcsdk_mock,
    get_device_object,
    get_session_init_object,
    get_session_poll_object,
    get_list_proc_start_object,
    get_list_proc_end_object,
    get_kill_proc_object
):
    """Test action with correct parameters - exception upon kill"""
    called = False

    def post_commands_response(*args):
        nonlocal called
        if not called:
            called = True
            return get_list_proc_start_object
        else:
            return get_kill_proc_object

    def kill_resp(*args):
        raise MockException(Exception)

    obj = CBCSplunk()
    action = KillProcessAction(obj, {"device_id": 354648, "process_pid": 303})
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
        post_commands_response,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/10",
        get_list_proc_end_object,
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands",
        post_commands_response,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/16",
        kill_resp,
    )
    cbcsdk_mock.mock_request(
        "DELETE", "/appservices/v6/orgs/test/liveresponse/sessions/1:2468", None
    )

    action_result = action.call()
    assert obj.progress_message == "Process(es) successfully killed"
    assert action_result == phantom.APP_SUCCESS
    data = obj.action_results[0].get_data()
    assert data[0]["process_pid"] == 303
    assert data[0]["process_killed"] is False
