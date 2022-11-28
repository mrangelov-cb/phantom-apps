"""Tests for add an IOC action"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
from cbc_sdk.errors import ObjectNotFoundError
import phantom.app as phantom
from actions.action_add_ioc import AddIOCAction

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


def test_add_ioc_to_feed_success(
    cbcsdk_mock, get_report_no_iocs_response, get_report_with_one_ioc_response
):
    """Test to add an IOC to Feed"""
    obj = CBCSplunk()
    ioc_dict = {
        "feed_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        "cbc_field": "process_hash",
        "ioc_id": "test",
        "ioc_value": "b2e5665591b2118ca13709f61b60d700",
    }
    action = AddIOCAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api

    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports",
        get_report_no_iocs_response,
    )
    cbcsdk_mock.mock_request(
        "PUT",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports/323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        get_report_with_one_ioc_response["results"][0],
    )
    action_result = action.call()
    assert "Added IOC" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_add_ioc_to_watchlist_success(cbcsdk_mock, get_report_object, get_watchlist_object):
    """Test to add an IOC to Watchlist"""
    obj = CBCSplunk()
    ioc_dict = {
        "watchlist_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        "cbc_field": "md5",
        "ioc_value": "b2e5665591b2118ca13709f61b60d700",
    }
    action = AddIOCAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api

    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/TC09QSSTRHqRF2qAAli3TA",
        get_watchlist_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/reports/323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        get_report_object,
    )
    cbcsdk_mock.mock_request(
        "PUT",
        "/threathunter/watchlistmgr/v3/orgs/test/reports/323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        lambda *_: {},
    )
    action_result = action.call()
    assert "Added IOC" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_add_ioc_to_feed_no_report_found(
    cbcsdk_mock, get_report_no_iocs_response, get_report_with_one_ioc_response
):
    """Test to add an IOC to Feed - no report found"""
    obj = CBCSplunk()
    ioc_dict = {
        "feed_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        "cbc_field": "process_hash",
        "ioc_id": "test",
        "ioc_value": "b2e5665591b2118ca13709f61b60d700",
    }
    action = AddIOCAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api

    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports",
        {},
    )
    action_result = action.call()
    assert "Report cannot be found" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_add_ioc_to_watchlist_no_report(cbcsdk_mock, get_report_object, get_watchlist_object):
    """Test to add an IOC to Watchlist"""
    def get_resp(*args, **kwargs):
        return MockException(ObjectNotFoundError)

    obj = CBCSplunk()
    ioc_dict = {
        "watchlist_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f5",
        "cbc_field": "md5",
        "ioc_value": "b2e5665591b2118ca13709f61b60d700",
    }
    action = AddIOCAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api

    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/TC09QSSTRHqRF2qAAli3TA",
        get_watchlist_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/reports/323d1b5d-3ad3-4e2e-9ba0-9aacb2657f5",
        get_resp
    )

    action_result = action.call()
    assert "Report cannot be found" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_add_ioc_full_report_error(cbcsdk_mock, get_full_report_response):
    """Test to add an IOC whenever a Report is full"""
    obj = CBCSplunk()
    ioc_dict = {
        "feed_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        "cbc_field": "md5",
        "ioc_value": "b2e5665591b2118ca13709f61b60d700",
    }
    action = AddIOCAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api

    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports",
        get_full_report_response,
    )
    cbcsdk_mock.mock_request(
        "PUT",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports/323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        lambda: MockException(Exception),
    )
    action_result = action.call()
    assert "The report is full, create a new report!" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_add_ioc_failure(cbcsdk_mock, get_report_no_iocs_response):
    """Test to add an IOC on failure"""
    obj = CBCSplunk()
    ioc_dict = {
        "feed_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        "cbc_field": "md5",
        "ioc_value": "123",
    }
    action = AddIOCAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api

    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports",
        get_report_no_iocs_response,
    )
    cbcsdk_mock.mock_request(
        "PUT",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports/323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        lambda: MockException(Exception),
    )
    action_result = action.call()
    assert "IOC was not added" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_add_ioc_no_cbc_connection():
    """Test to add an IOC on no CBC"""
    obj = CBCSplunk()
    ioc_dict = {}
    action = AddIOCAction(obj, ioc_dict)
    action.cbc = None
    action_result = action.call()
    assert "IOC was not added" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_add_ioc_wrong_params():
    """Test to add an IOC on both watchlist_id and feed_id"""
    obj = CBCSplunk()
    ioc_dict = {"watchlist_id": "xxx", "feed_id": "xxx"}
    action = AddIOCAction(obj, ioc_dict)
    action.cbc = None
    action_result = action.call()
    assert "You should provide either watchlist_id or feed_id" in obj.progress_message
    assert action_result == phantom.APP_ERROR
