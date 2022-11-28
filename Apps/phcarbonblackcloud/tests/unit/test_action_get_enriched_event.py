"""Tests for get enriched events by alert"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_get_enriched_event import GetEnrichedEventAction
from cbc_sdk.errors import ObjectNotFoundError

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


def test_get_enriched_event_success(cbcsdk_mock,
                                    get_cb_analytics_alert,
                                    get_enriched_events_search_job_response,
                                    get_enriched_events_search_job_results_response,
                                    get_enriched_events_search_job_events_response):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = GetEnrichedEventAction(obj, {"alert_id": "27a278d2150911eb86f1011a55e73b72"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET",
                             "/appservices/v6/orgs/test/alerts/27a278d2150911eb86f1011a55e73b72",
                             get_cb_analytics_alert)
    cbcsdk_mock.mock_request("POST",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs",
                             get_enriched_events_search_job_response)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56"
                             "-8741e929e48b",
                             get_enriched_events_search_job_results_response)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/enriched_events/detail_jobs/08ffa932-b633-4107-ba56"
                             "-8741e929e48b/results",
                             get_enriched_events_search_job_events_response)
    action_result = action.call()
    assert obj.progress_message == "Successfully retrieved 2 enriched events for 27a278d2150911eb86f1011a55e73b72."
    assert action_result == phantom.APP_SUCCESS


def test_get_enriched_event_missing_alert_id(cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = GetEnrichedEventAction(obj, {})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "Missing alert id."
    assert action_result == phantom.APP_ERROR


def test_get_enriched_event_no_such_alert(cbcsdk_mock):
    """Test action - ObjectNotFound"""

    def post_resp(*args, **kwargs):
        return MockException(ObjectNotFoundError)

    obj = CBCSplunk()
    action = GetEnrichedEventAction(obj, {"alert_id": "27a278d2150911eb86f1011a55e73b72"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET",
                             "/appservices/v6/orgs/test/alerts/27a278d2150911eb86f1011a55e73b72",
                             post_resp)
    action_result = action.call()
    assert "No such alert 27a278d2150911eb86f1011a55e73b72." in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_get_enriched_event_exception(cbcsdk_mock):
    """Test action - other Exception"""

    def post_resp(*args, **kwargs):
        return MockException(Exception)

    obj = CBCSplunk()
    action = GetEnrichedEventAction(obj, {"alert_id": "27a278d2150911eb86f1011a55e73b72"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request("GET",
                             "/appservices/v6/orgs/test/alerts/27a278d2150911eb86f1011a55e73b72",
                             post_resp)
    action_result = action.call()
    assert "Could not get enriched events by alert 27a278d2150911eb86f1011a55e73b72" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_get_enriched_event_no_cbc():
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = GetEnrichedEventAction(obj, {"alert_id": "27a278d2150911eb86f1011a55e73b72"})
    action.cbc = None
    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."
