"""Tests for add an IOC action"""
import pytest
from cbc_sdk import CBCloudAPI
from cbc_sdk.errors import ObjectNotFoundError
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_retrieve_report_iocs import RetrieveIOCAction

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


def test_retrieve_ioc_success_with_feed_id(cbcsdk_mock, get_report_with_one_ioc_response):
    """Test to retriee an IOC from report in feed"""
    obj = CBCSplunk()
    ioc_dict = {
        "feed_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51"
    }
    action = RetrieveIOCAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports",
        get_report_with_one_ioc_response,
    )
    action_result = action.call()
    assert "Successfully retrieved iocs for report" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_retrieve_ioc_success_with_watchlist_id(
    cbcsdk_mock, get_report_with_one_ioc_response, get_watchlist_object
):
    """Test to retrieve IOCs with `watchlist_id`"""
    obj = CBCSplunk()
    ioc_dict = {
        "watchlist_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51"
    }
    action = RetrieveIOCAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/TC09QSSTRHqRF2qAAli3TA",
        get_watchlist_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/reports/323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        get_report_with_one_ioc_response["results"][0],
    )
    action_result = action.call()
    assert "Successfully retrieved iocs for report" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_retrieve_iocs_no_required_ids(cbcsdk_mock):
    """Test to retrieve IOCs where the required fields are empty"""
    obj = CBCSplunk()
    ioc_dict = {
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
    }
    action = RetrieveIOCAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert (
        "Could not retrieve iocs for report - You should provide either feed_id or watchlist_id."
        in obj.progress_message
    )
    assert action_result == phantom.APP_ERROR


def test_retrieve_iocs_both_feed_and_report_provided(cbcsdk_mock):
    """Test to retrieve IOCs where the required fields are empty"""
    obj = CBCSplunk()
    ioc_dict = {
        "feed_id": "TC09QSSTRHqRF2qAAli3TA",
        "watchlist_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
    }
    action = RetrieveIOCAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert (
        "Could not retrieve iocs for report - You should provide either feed_id or watchlist_id."
        in obj.progress_message
    )
    assert action_result == phantom.APP_ERROR


def test_retrieve_iocs_report_cannot_be_found(
    cbcsdk_mock, get_report_with_one_ioc_response, get_watchlist_object
):
    """Test to retrieve IOCs whenever a Report cannot be found"""
    obj = CBCSplunk()
    ioc_dict = {
        "feed_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51"
    }
    action = RetrieveIOCAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports",
        {},
    )

    action_result = action.call()
    assert "Could not retrieve iocs for report - Report cannot be found." in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_retrieve_ioc_with_watchlist_id_no_report_found(
    cbcsdk_mock, get_report_with_one_ioc_response, get_watchlist_object
):
    """Test to retrieve IOCs with `watchlist_id` - no report found"""
    def get_resp(*args, **kwargs):
        return MockException(ObjectNotFoundError)

    obj = CBCSplunk()
    ioc_dict = {
        "watchlist_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51"
    }
    action = RetrieveIOCAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/TC09QSSTRHqRF2qAAli3TA",
        get_watchlist_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/reports/323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        get_resp
    )
    action_result = action.call()
    assert "Report cannot be found" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_retrieved_iocs_no_cbc(cbcsdk_mock, get_report_with_one_ioc_response):
    """Test to retrieve IOCs without CBC"""
    obj = CBCSplunk()
    ioc_dict = {
        "feed_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51"
    }
    action = RetrieveIOCAction(obj, ioc_dict)
    action.cbc = None
    action_result = action.call()
    assert "Please configure all connection parameters." in obj.progress_message
    assert action_result == phantom.APP_ERROR
