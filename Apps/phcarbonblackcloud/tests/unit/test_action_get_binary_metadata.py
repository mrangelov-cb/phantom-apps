"""Tests for get binary file metadata"""
import pytest
from cbc_sdk import CBCloudAPI
from cbc_sdk.errors import ObjectNotFoundError
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_get_binary_metadata import GetBinaryMetadataAction

from tests.fixtures.cbc_sdk_mock import CBCSDKMock


class MockException:
    """MockException class for Exceptions"""
    def __init__(self, exc_type, *args, **kwargs):
        """Raising exception"""
        raise exc_type(args, kwargs)


@pytest.fixture(scope="function")
def cb():
    """Create CBCloudAPI singleton"""
    return CBCloudAPI(url="https://example.com", org_key="test", token="abcd/1234", ssl_verify=False)


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch, cb):
    """Mocks CBC SDK for unit tests"""
    return CBCSDKMock(monkeypatch, cb)


# ==================================== UNIT TESTS BELOW ====================================


def test_get_metadata_success(monkeypatch,
                              cbcsdk_mock,
                              get_binary_metadata_response):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = GetBinaryMetadataAction(obj,
                                     {"file_hash": "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776"})
    action.cbc = cbcsdk_mock.api
    meta_url = "/ubs/v1/orgs/test/sha256/87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776/metadata"

    cbcsdk_mock.mock_request("GET", meta_url, get_binary_metadata_response)

    action_result = action.call()
    assert obj.progress_message == "Get UBS metadata successfully retrieved."
    assert action_result == phantom.APP_SUCCESS
    data = obj.action_results[0].get_data()
    assert data[0]["sha256"] == "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776"


def test_get_metadata_not_found(monkeypatch, cbcsdk_mock):
    """Test action with correct parameters - not such hash"""
    def get_resp(*args):
        raise MockException(ObjectNotFoundError)
    obj = CBCSplunk()
    action = GetBinaryMetadataAction(obj,
                                     {"file_hash": "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776"})
    action.cbc = cbcsdk_mock.api
    meta_url = "/ubs/v1/orgs/test/sha256/87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776/metadata"

    cbcsdk_mock.mock_request("GET", meta_url, get_resp)

    action_result = action.call()
    assert obj.progress_message == "Could not find hash in UBS: "\
                                   "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776."
    assert action_result == phantom.APP_ERROR


def test_get_metadata_exception(monkeypatch, cbcsdk_mock):
    """Test action with correct parameters - exception"""
    def get_resp(*args):
        raise MockException(Exception)
    obj = CBCSplunk()
    action = GetBinaryMetadataAction(obj,
                                     {"file_hash": "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776"})
    action.cbc = cbcsdk_mock.api
    meta_url = "/ubs/v1/orgs/test/sha256/87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776/metadata"

    cbcsdk_mock.mock_request("GET", meta_url, get_resp)

    action_result = action.call()
    assert "Could not retrieve binary metadata for " in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_get_metadata_missing_file_hash(monkeypatch, cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = GetBinaryMetadataAction(obj, {})
    action.cbc = cbcsdk_mock.api

    action_result = action.call()
    assert obj.progress_message == "No file_hash provided"
    assert action_result == phantom.APP_ERROR


def test_get_metadata_no_cbc(monkeypatch, cbcsdk_mock):
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = GetBinaryMetadataAction(obj,
                                     {"file_hash": "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776"})

    action.cbc = None
    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."
