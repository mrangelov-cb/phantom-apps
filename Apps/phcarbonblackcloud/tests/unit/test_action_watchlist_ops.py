"""Tests for Feed Ops"""
import pytest
from cbc_sdk import CBCloudAPI
from cbc_sdk.errors import ObjectNotFoundError

from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom

from actions.action_create_watchlist import CreateWatchlistAction
from actions.action_delete_watchlist import DeleteWatchlistAction
from actions.action_update_watchlist import UpdateWatchlistAction
from actions.action_retrieve_watchlist import RetrieveWatchlistAction


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


def test_create_watchlist_successful(cbcsdk_mock, get_watchlist_build_response):
    """Test to create a Watchlist"""
    obj = CBCSplunk()
    watchlist_dict = {"watchlist_name": "test_watchlist", "watchlist_report_ids": "123,456,789"}
    action = CreateWatchlistAction(obj, watchlist_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/threathunter/watchlistmgr/v3/orgs/test/watchlists", get_watchlist_build_response
    )
    action_result = action.call()
    assert "Created Watchlist" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_create_watchlist_error(cbcsdk_mock):
    """Test error on creating Watchlist"""
    obj = CBCSplunk()
    watchlist_dict = {"watchlist_report_ids": "123,456,789"}
    action = CreateWatchlistAction(obj, watchlist_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists",
        lambda *_: MockException(Exception),
    )
    action_result = action.call()
    assert "Watchlist was not created" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_retrieve_watchlist_action_successful(cbcsdk_mock, get_watchlist_object):
    """Test to retrieve a Watchlist"""
    obj = CBCSplunk()
    action = RetrieveWatchlistAction(obj, {"watchlist_id": "TC09QSSTRHqRF2qAAli3TA"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/TC09QSSTRHqRF2qAAli3TA",
        get_watchlist_object,
    )
    action_result = action.call()
    assert "Retrieved" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_retrieve_watchlist_action_not_found(cbcsdk_mock):
    """Test to retrieve a Watchlist - Not Found Error"""
    obj = CBCSplunk()
    action = RetrieveWatchlistAction(obj, {"watchlist_id": "1"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/1",
        lambda *_: MockException(ObjectNotFoundError),
    )
    action_result = action.call()
    assert "Watchlist not found" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_retrieve_watchlist_action_error(cbcsdk_mock):
    """Test to retrieve a Watchlist - general exception"""
    obj = CBCSplunk()
    action = RetrieveWatchlistAction(obj, {"watchlist_id": "1"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/threathunter/watchlistmgr/v3/orgs/test/watchlists/1", lambda *_: MockException(Exception)
    )
    action_result = action.call()
    assert "Watchlist couldn't be retrieved" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_delete_watchlist_successful(cbcsdk_mock, get_watchlist_object):
    """Test to delete a Watchlist"""
    obj = CBCSplunk()
    action = DeleteWatchlistAction(obj, {"watchlist_id": "TC09QSSTRHqRF2qAAli3TA"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/TC09QSSTRHqRF2qAAli3TA",
        get_watchlist_object,
    )
    cbcsdk_mock.mock_request(
        "DELETE",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/TC09QSSTRHqRF2qAAli3TA",
        CBCSDKMock.StubResponse(None, 204),
    )
    action_result = action.call()
    assert "Successfully deleted" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_delete_watchlist_not_found(cbcsdk_mock, get_watchlist_object):
    """Test to delete a Watchlist - not found"""
    obj = CBCSplunk()
    action = DeleteWatchlistAction(obj, {"watchlist_id": "TC09QSSTRHqRF2qAAli3TA"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/TC09QSSTRHqRF2qAAli3TA",
        get_watchlist_object,
    )
    cbcsdk_mock.mock_request(
        "DELETE",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/TC09QSSTRHqRF2qAAli3TA",
        lambda *_: MockException(ObjectNotFoundError),
    )
    action_result = action.call()
    assert "Watchlist not found" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_delete_watchlist_error(cbcsdk_mock, get_watchlist_object):
    """Test to delete a Watchlist - general exception"""
    obj = CBCSplunk()
    action = DeleteWatchlistAction(obj, {})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert "Watchlist couldn't be deleted" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_update_watchlist_successful(cbcsdk_mock, get_watchlist_object, get_report_object):
    """Test to update a Watchlist"""
    obj = CBCSplunk()
    watchlist_dict = {
        "watchlist_id": "TC09QSSTRHqRF2qAAli3TA",
        "watchlist_name": "TestNew",
        "add_report_ids": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        "remove_report_ids": "323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51"
    }
    action = UpdateWatchlistAction(obj, watchlist_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/TC09QSSTRHqRF2qAAli3TA",
        get_watchlist_object,
    )
    cbcsdk_mock.mock_request(
        "PUT",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/TC09QSSTRHqRF2qAAli3TA",
        get_watchlist_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/reports/323d1b5d-3ad3-4e2e-9ba0-9aacb2657f51",
        get_report_object,
    )
    action_result = action.call()
    assert "Successfully updated" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_update_watchlist_not_found(cbcsdk_mock):
    """Test to update a Watchlist - not found"""
    obj = CBCSplunk()
    watchlist_dict = {"watchlist_id": "1", "watchlist_name": "TestNew"}
    action = UpdateWatchlistAction(obj, watchlist_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/watchlists/1",
        lambda *_: MockException(ObjectNotFoundError),
    )
    action_result = action.call()
    assert "Watchlist not found" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_update_watchlist_error(cbcsdk_mock):
    """Test to update a Watchlist - general exception"""
    obj = CBCSplunk()
    watchlist_dict = {}
    action = UpdateWatchlistAction(obj, watchlist_dict)
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert "Watchlist couldn't be updated" in obj.progress_message
    assert action_result == phantom.APP_ERROR
