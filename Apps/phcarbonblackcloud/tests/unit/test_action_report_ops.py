"""Tests for creating a Report"""
import uuid
import pytest
from cbc_sdk import CBCloudAPI
from cbc_sdk.errors import ObjectNotFoundError
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom

from actions.action_create_report import CreateReportAction
from actions.action_delete_report import DeleteReportAction

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


def test_create_report_succesfuly(cbcsdk_mock, monkeypatch):
    """Test the creating of a Report"""
    obj = CBCSplunk()
    create_report_dict = {
        "feed_id": "123",
        "report_name": "TestReport",
        "report_severity": "6",
        "report_summary": "TestSummary",
        "report_tags": "tag1,tag2",
    }
    monkeypatch.setattr(uuid, "uuid4", lambda: "123")
    cbcsdk_mock.mock_request(
        "PUT",
        "/threathunter/feedmgr/v2/orgs/test/feeds/123/reports/123",
        {},
    )
    action = CreateReportAction(obj, create_report_dict)
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert "Created Report" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_create_report_succesfuly_on_watchlist(cbcsdk_mock, monkeypatch):
    """Test the creating of a Report with `report_save_as_watchlist`"""
    obj = CBCSplunk()
    create_report_dict = {
        "report_save_as_watchlist": True,
        "report_name": "TestReport",
        "report_severity": "6",
        "report_summary": "TestSummary",
        "report_tags": "tag1,tag2",
    }
    monkeypatch.setattr(uuid, "uuid4", lambda: "123")
    cbcsdk_mock.mock_request(
        "POST",
        "/threathunter/watchlistmgr/v3/orgs/test/reports",
        {},
    )
    cbcsdk_mock.mock_request(
        "PUT",
        "/threathunter/watchlistmgr/v3/orgs/test/reports/123",
        {},
    )
    action = CreateReportAction(obj, create_report_dict)
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert "Created Report" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_create_report_error_params(cbcsdk_mock, monkeypatch):
    """Test the creating of a Report without required params"""
    obj = CBCSplunk()
    create_report_dict = {
        "report_name": "TestReport",
        "report_severity": "6",
        "report_summary": "TestSummary",
        "report_tags": "tag1,tag2",
    }
    monkeypatch.setattr(uuid, "uuid4", lambda: "123")
    action = CreateReportAction(obj, create_report_dict)
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert "You have to set `feed_id` or set `Save to Watchlist` to True." in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_create_report_error_params_report_severity(cbcsdk_mock, monkeypatch):
    """Test the creating of a Report with wrong severity."""
    obj = CBCSplunk()
    create_report_dict = {
        "feed_id": "123",
        "report_name": "TestReport",
        "report_severity": "11",
        "report_summary": "TestSummary",
        "report_tags": "tag1,tag2",
    }
    monkeypatch.setattr(uuid, "uuid4", lambda: "123")
    action = CreateReportAction(obj, create_report_dict)
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert "Report severity must be an integer and inbetween 1 and 10." in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_create_report_error_exception(cbcsdk_mock, monkeypatch):
    """Test the creating of a Report - general exception"""
    obj = CBCSplunk()
    create_report_dict = {
        "report_name": "TestReport",
        "report_severity": "6",
        "report_summary": "TestSummary",
        "report_tags": "tag1,tag2",
    }
    monkeypatch.setattr(uuid, "uuid4", lambda: MockException)
    action = CreateReportAction(obj, create_report_dict)
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert "Report was not created" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_delete_report_succesfuly(cbcsdk_mock, get_report_response):
    """Test the deleting of a Report success"""
    obj = CBCSplunk()
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/reports/report_id",
        get_report_response,
    )
    cbcsdk_mock.mock_request(
        "DELETE",
        "/threathunter/watchlistmgr/v3/orgs/test/reports/report_id",
        {},
    )
    action = DeleteReportAction(obj, {"report_id": "report_id"})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert "Deleted Report" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_delete_report_not_found(cbcsdk_mock):
    """Test the deleting of a Report not found"""
    obj = CBCSplunk()
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/reports/report_id",
        lambda *_: MockException(ObjectNotFoundError),
    )
    action = DeleteReportAction(obj, {"report_id": "report_id"})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert "Report not found" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_delete_report_general_exc(cbcsdk_mock):
    """Test the deleting of a Report - general exception"""
    obj = CBCSplunk()
    create_report_dict = {
        "feed_id": "feed_id",
        "report_id": "report_id",
    }
    cbcsdk_mock.mock_request(
        "GET",
        "/threathunter/watchlistmgr/v3/orgs/test/reports/report_id",
        lambda *_: MockException(),
    )
    action = DeleteReportAction(obj, create_report_dict)
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert "Report was not deleted" in obj.progress_message
    assert action_result == phantom.APP_ERROR
