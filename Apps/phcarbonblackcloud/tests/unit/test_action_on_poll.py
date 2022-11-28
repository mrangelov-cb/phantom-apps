"""Tests for cbcapp connector"""
import pytest
import sys
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_on_poll import OnPollAction
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


def test_action_on_poll_exist():
    """Test if action called"""
    obj = CBCSplunk()
    obj.handle_action({"start_time": 1, "end_time": 2, "artifact_count": 1, "container_count": 1})
    assert "actions.action_on_poll" in sys.modules.keys()
    assert "OnPollAction" in dir(sys.modules["actions.action_on_poll"])


def test_successful_empty_poll(cbcsdk_mock, get_no_alert_response):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = OnPollAction(
        obj, {"start_time": 1, "end_time": 2, "artifact_count": 1, "container_count": 1}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/alerts/_search", get_no_alert_response
    )

    action_result = action.call()
    assert "Polling complete. Found 0" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_successful_single_poll(cbcsdk_mock, get_three_alerts_response):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = OnPollAction(
        obj, {"start_time": 1, "end_time": 2, "artifact_count": 4, "container_count": 4}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/alerts/_search", get_three_alerts_response
    )

    action_result = action.call()
    assert "Polling complete. Found 3" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS
    assert len(obj.artifacts) == 3
    assert obj.artifacts[0]["cef"]["alertId"] == "038894832709076d63111e99466f73575fcf3ca"


def test_successful_large_poll(cbcsdk_mock, get_one_alert_response, get_10k1_alert_response):
    """Test action with correct parameters"""
    _was_called = False
    _count = 0

    def post_method(*args, **kwargs):
        nonlocal _was_called
        nonlocal _count
        if not _was_called:
            _count += 1
            if _count == 2:
                _was_called = True
            return get_10k1_alert_response
        else:
            return get_one_alert_response

    obj = CBCSplunk()
    action = OnPollAction(
        obj,
        {"start_time": 1, "end_time": 2, "artifact_count": -1, "container_count": -1},
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/alerts/_search", post_method)

    action_result = action.call()
    assert "Polling complete. Found 10001" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS
    assert obj.artifacts[0]["cef"]["alertId"] == "038894832709076d63111e99466f73575fcf3ca"


def test_failure_missing_params():
    """Test action with incorrect parameters"""
    obj = CBCSplunk()
    action = OnPollAction(obj, {"artifact_count": 1, "container_count": 1})

    action_result = action.call()
    assert "start time or end time not specified" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_failure_edr_not_enabled(cbcsdk_mock):
    """Test action with correct parameters - cbc exception"""
    obj = CBCSplunk()
    action = OnPollAction(
        obj, {"start_time": 1, "end_time": 2, "artifact_count": 1, "container_count": 1}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/alerts/_search",
        lambda *_: MockException(Exception, "WATCHLIST alerts are not available"),
    )

    action_result = action.call()
    assert (
        "Failed: WATCHLIST alerts not available, please enable Enterprise EDR"
        in obj.progress_message
    )
    assert action_result == phantom.APP_ERROR


def test_failure_fetch_alerts(monkeypatch, cbcsdk_mock, get_one_alert_response):
    """Test action with correct parameters - get alerts exception"""
    obj = CBCSplunk()
    action = OnPollAction(
        obj, {"start_time": 1, "end_time": 2, "artifact_count": 1, "container_count": 1}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/alerts/_search", get_one_alert_response
    )
    monkeypatch.setattr("actions.action_on_poll.prepare_artifact", lambda *_: Exception())
    action_result = action.call()

    assert "Error fetching alerts from CBC:" in obj.progress_message
    assert action_result == phantom.APP_ERROR
