"""Tests for Feed Ops"""
import pytest
from cbc_sdk import CBCloudAPI
from cbc_sdk.errors import ObjectNotFoundError

from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom

from actions.action_update_feed import UpdateFeedAction
from actions.action_create_feed import CreateFeedAction
from actions.action_retrieve_feed import RetrieveFeedAction
from actions.action_delete_feed import DeleteFeedAction

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


def test_create_feed_successful(cbcsdk_mock, get_feed_build_response):
    """Test to add a Feed"""
    obj = CBCSplunk()
    feed_dict = {
        "feed_name": "test_feed",
        "feed_provider_url": "https://localhost/",
        "feed_summary": "test_feed_sum",
        "feed_category": "test_feed_cat",
    }
    action = CreateFeedAction(obj, feed_dict)
    action.cbc = cbcsdk_mock.api

    cbcsdk_mock.mock_request(
        "POST", "/threathunter/feedmgr/v2/orgs/test/feeds", get_feed_build_response
    )
    action_result = action.call()
    assert "Created Feed" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_create_feed_error(cbcsdk_mock, get_feed_build_response):
    """Test error on creating Feed"""
    obj = CBCSplunk()
    feed_dict = {}
    action = CreateFeedAction(obj, feed_dict)
    action.cbc = cbcsdk_mock.api

    cbcsdk_mock.mock_request(
        "POST", "/threathunter/feedmgr/v2/orgs/test/feeds", get_feed_build_response
    )
    action_result = action.call()
    assert "Feed was not created" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_retrieve_feed_action_successful(cbcsdk_mock, get_feed_build_response):
    """Test to retrieve a Feed"""
    obj = CBCSplunk()
    action = RetrieveFeedAction(obj, {"feed_id": "123"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/threathunter/feedmgr/v2/orgs/test/feeds/123", get_feed_build_response
    )
    action_result = action.call()
    assert "Retrieved" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_retrieve_feed_action_not_found(cbcsdk_mock):
    """Test to retrieve a Feed - Not Found Error"""
    obj = CBCSplunk()
    action = RetrieveFeedAction(obj, {"feed_id": "1"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/feedmgr/v2/orgs/test/feeds/1",
        lambda *_: MockException(ObjectNotFoundError),
    )
    action_result = action.call()
    assert "Feed not found" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_retrieve_feed_action_error(cbcsdk_mock):
    """Test to retrieve a Feed - general exception"""
    obj = CBCSplunk()
    action = RetrieveFeedAction(obj, {"feed_id": "1"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/threathunter/feedmgr/v2/orgs/test/feeds/1", lambda *_: MockException(Exception)
    )
    action_result = action.call()
    assert "Feed couldn't be retrieved" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_delete_feed_successful(cbcsdk_mock, get_feed_retrieve_object):
    """Test to delete a Feed"""
    obj = CBCSplunk()
    action = DeleteFeedAction(obj, {"feed_id": "123"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/threathunter/feedmgr/v2/orgs/test/feeds/123", get_feed_retrieve_object
    )
    cbcsdk_mock.mock_request(
        "DELETE", "/threathunter/feedmgr/v2/orgs/test/feeds/1", CBCSDKMock.StubResponse(None, 204)
    )
    action_result = action.call()
    assert "Successfully deleted" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_delete_feed_not_found(cbcsdk_mock, get_feed_retrieve_object):
    """Test to delete a Feed - not found"""
    obj = CBCSplunk()
    action = DeleteFeedAction(obj, {"feed_id": "1"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/threathunter/feedmgr/v2/orgs/test/feeds/1", get_feed_retrieve_object
    )
    cbcsdk_mock.mock_request(
        "DELETE",
        "/threathunter/feedmgr/v2/orgs/test/feeds/1",
        lambda *_: MockException(ObjectNotFoundError),
    )
    action_result = action.call()
    assert "Feed not found" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_delete_feed_error(cbcsdk_mock, get_feed_retrieve_object):
    """Test to delete a Feed - general exception"""
    obj = CBCSplunk()
    action = DeleteFeedAction(obj, {"feed_id": "1"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/threathunter/feedmgr/v2/orgs/test/feeds/1", get_feed_retrieve_object
    )
    cbcsdk_mock.mock_request(
        "DELETE", "/threathunter/feedmgr/v2/orgs/test/feeds/1", lambda *_: MockException(Exception)
    )
    action_result = action.call()
    assert "Feed couldn't be deleted" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_update_feed_successful(cbcsdk_mock, get_feed_retrieve_object):
    """Test to update a Feed"""
    obj = CBCSplunk()
    update_dict = {
        "feed_id": "1",
        "feed_name": "test_new",
        "feed_provider_url": "http://example.com",
        "feed_summary": "test",
        "feed_category": "test",
    }
    action = UpdateFeedAction(obj, update_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/threathunter/feedmgr/v2/orgs/test/feeds/1", get_feed_retrieve_object
    )
    cbcsdk_mock.mock_request(
        "PUT", "/threathunter/feedmgr/v2/orgs/test/feeds/123/feedinfo", get_feed_retrieve_object
    )
    action_result = action.call()
    assert "Successfully updated" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_update_feed_not_found(cbcsdk_mock):
    """Test to update a Feed - not found"""
    obj = CBCSplunk()
    update_dict = {
        "feed_id": "123",
        "feed_name": "test_new",
        "feed_provider_url": "http://example.com",
        "feed_summary": "test",
        "feed_category": "test",
    }
    action = UpdateFeedAction(obj, update_dict)
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/feedmgr/v2/orgs/test/feeds/1",
        lambda *_: MockException(ObjectNotFoundError),
    )
    action_result = action.call()
    assert "Feed not found" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_update_feed_error(cbcsdk_mock):
    """Test to update a Feed - general exception"""
    obj = CBCSplunk()
    update_dict = {}
    action = UpdateFeedAction(obj, update_dict)
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert "Feed couldn't be updated" in obj.progress_message
    assert action_result == phantom.APP_ERROR
