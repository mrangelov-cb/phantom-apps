"""Tests for add an IOC action"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_remove_ioc_feed import RemoveIOCFeedAction

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


def test_remove_ioc_success_with_feed_id(cbcsdk_mock, get_report_with_one_ioc_response):
    """Test to remove an IOC with `feed_id`"""
    obj = CBCSplunk()
    ioc_dict = {
        "feed_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        "ioc_id": "foo",
    }
    action = RemoveIOCFeedAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports",
        get_report_with_one_ioc_response,
    )
    cbcsdk_mock.mock_request(
        "PUT",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports/323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        lambda *_: {},
    )
    action_result = action.call()
    assert "Removed IOC" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_remove_ioc_success_with_feed_id_by_value(cbcsdk_mock, get_report_with_one_ioc_response):
    """Test to remove an IOC with `feed_id`"""
    obj = CBCSplunk()
    ioc_dict = {
        "feed_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        "ioc_value": "b2e5665591b2118ca13709f61b60d700",
    }
    action = RemoveIOCFeedAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports",
        get_report_with_one_ioc_response,
    )
    cbcsdk_mock.mock_request(
        "PUT",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports/323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        lambda *_: {},
    )
    action_result = action.call()
    assert "Removed IOC" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_remove_ioc_success_no_required_ids(cbcsdk_mock):
    """Test to remove an IOC where the required fields are empty"""
    obj = CBCSplunk()
    ioc_dict = {
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        "ioc_id": "foo",
    }
    action = RemoveIOCFeedAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert (
        "IOC was not Removed - You should provide feed_id."
        in obj.progress_message
    )
    assert action_result == phantom.APP_ERROR


def test_remove_ioc_report_cannot_be_found(
    cbcsdk_mock, get_report_with_one_ioc_response, get_watchlist_object
):
    """Test to remove an IOC whenever a Report cannot be found"""
    obj = CBCSplunk()
    ioc_dict = {
        "feed_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        "ioc_value": "b2e5665591b2118ca13709f61b60d700",
    }
    action = RemoveIOCFeedAction(obj, ioc_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports",
        {},
    )

    action_result = action.call()
    assert "IOC was not Removed - Report cannot be found" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_remove_ioc_no_cbc(cbcsdk_mock, get_report_with_one_ioc_response):
    """Test to remove an IOC without CBC"""
    obj = CBCSplunk()
    ioc_dict = {
        "feed_id": "TC09QSSTRHqRF2qAAli3TA",
        "report_id": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        "ioc_id": "foo",
    }
    action = RemoveIOCFeedAction(obj, ioc_dict)
    action.cbc = None
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports",
        get_report_with_one_ioc_response,
    )
    cbcsdk_mock.mock_request(
        "PUT",
        "/threathunter/feedmgr/v2/orgs/test/feeds/TC09QSSTRHqRF2qAAli3TA/reports/323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        lambda *_: {},
    )
    action_result = action.call()
    assert "IOC was not Removed" in obj.progress_message
    assert action_result == phantom.APP_ERROR
