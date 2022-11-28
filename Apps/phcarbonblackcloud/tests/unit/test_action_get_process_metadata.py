"""Tests for get process metadata by guid"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_get_process_metadata import GetProcessMetadataAction

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


def test_get_process_metadata_success(cbcsdk_mock,
                                      get_process_validation_resp,
                                      post_process_details_resp,
                                      get_process_details_status_resp,
                                      get_process_details_resp):
    """Test action with correct parameters"""
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/processes/search_validation",
                             get_process_validation_resp)
    cbcsdk_mock.mock_request("POST",
                             "/api/investigate/v2/orgs/test/processes/search_jobs",
                             post_process_details_resp)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/processes/search_jobs/ccc47a52-9a61-4c77-8652-8a03dc187b98",
                             get_process_details_status_resp)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/search_jobs/"
                             "ccc47a52-9a61-4c77-8652-8a03dc187b98/results?start=0&rows=500",
                             get_process_details_resp)
    cbcsdk_mock.mock_request("POST",
                             "/api/investigate/v2/orgs/test/processes/detail_job",
                             post_process_details_resp)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/detail_jobs/ccc47a52-9a61-4c77-8652-8a03dc187b98",
                             get_process_details_status_resp)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/detail_jobs/"
                             "ccc47a52-9a61-4c77-8652-8a03dc187b98/results",
                             get_process_details_resp)
    obj = CBCSplunk()

    action = GetProcessMetadataAction(obj, {"process_guid": "27a278d2150911eb86f1011a55e73b72"})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "Successfully retrieved metadata for 27a278d2150911eb86f1011a55e73b72."
    assert action_result == phantom.APP_SUCCESS


def test_get_process_metadata_no_such_guid(cbcsdk_mock,
                                           get_process_validation_resp,
                                           post_process_details_resp,
                                           get_process_details_status_resp,
                                           get_process_details_0_found_resp):
    """Test action with correct parameters"""
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/processes/search_validation",
                             get_process_validation_resp)
    cbcsdk_mock.mock_request("POST",
                             "/api/investigate/v2/orgs/test/processes/search_jobs",
                             post_process_details_resp)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/processes/search_jobs/ccc47a52-9a61-4c77-8652-8a03dc187b98",
                             get_process_details_status_resp)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/detail_jobs/ccc47a52-9a61-4c77-8652-8a03dc187b98",
                             get_process_details_status_resp)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v2/orgs/test/processes/search_jobs/ccc47a52-9a61-4c77-8652-8a03dc187b98"
                             "/results?start=0&rows=500",
                             get_process_details_0_found_resp)
    obj = CBCSplunk()

    action = GetProcessMetadataAction(obj, {"process_guid": "27a278d2150911eb86f1011a55e73b72"})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "Could not find 27a278d2150911eb86f1011a55e73b72."
    assert action_result == phantom.APP_ERROR


def test_get_process_metadata_no_cbc():
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = GetProcessMetadataAction(obj, {"process_guid": "27a278d2150911eb86f1011a55e73b72"})
    action.cbc = None
    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."


def test_get_process_metadata_missing_process_guid(cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = GetProcessMetadataAction(obj, {})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "Missing process guid."
    assert action_result == phantom.APP_ERROR


def test_get_process_metadata_exception(cbcsdk_mock):
    """Test action with correct parameters - exception"""
    def get_resp():
        raise MockException(Exception)
    cbcsdk_mock.mock_request("GET",
                             "/api/investigate/v1/orgs/test/processes/search_validation",
                             get_resp)
    obj = CBCSplunk()

    action = GetProcessMetadataAction(obj, {"process_guid": "27a278d2150911eb86f1011a55e73b72"})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert "Could not get process metadata for 27a278d2150911eb86f1011a55e73b72" in obj.progress_message
    assert action_result == phantom.APP_ERROR
