"""Tests for get binary file"""
import pytest
import io
import urllib
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_get_binary_file import GetBinaryFileAction

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


class MockRawFile:
    """Class to mock a raw file response"""
    @property
    def raw(self):
        """Raw property"""
        contents = "Test"
        return io.StringIO(contents)


def get_file_content(url, stream=True):
    """Replacement function for the Connection.get"""
    return MockRawFile()


def dummy_urlopen(url):
    """Mock urllib.request.urlopen"""
    class dummy_request():
        """Mock response object"""
        def read(self):
            """Mock response read method"""
            return "test"
    return dummy_request()


# ==================================== UNIT TESTS BELOW ====================================


def test_get_file_success(monkeypatch,
                          cbcsdk_mock,
                          get_binary_file_response,
                          get_binary_metadata_response):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = GetBinaryFileAction(obj, {"file_hash": "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776"})
    action.cbc = cbcsdk_mock.api
    meta_url = "/ubs/v1/orgs/test/sha256/87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776/metadata"

    cbcsdk_mock.mock_request("POST", "/ubs/v1/orgs/test/file/_download", get_binary_file_response)
    cbcsdk_mock.mock_request("GET",
                             meta_url,
                             get_binary_metadata_response)
    monkeypatch.setattr(urllib.request, "urlopen", dummy_urlopen)

    action_result = action.call()
    assert obj.progress_message == "File successfully retrieved"
    assert action_result == phantom.APP_SUCCESS


def test_get_file_missing_file_hash(monkeypatch, cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = GetBinaryFileAction(obj, {})
    action.cbc = cbcsdk_mock.api

    action_result = action.call()
    assert obj.progress_message == "No file_hash provided"
    assert action_result == phantom.APP_ERROR


def test_get_file_bad_file_hash_wrong_length(monkeypatch, cbcsdk_mock):
    """Test action with bad parameters"""
    obj = CBCSplunk()
    action = GetBinaryFileAction(obj, {"file_hash": "bad"})
    action.cbc = cbcsdk_mock.api

    action_result = action.call()
    assert obj.progress_message == "Malformed sha256 hash"
    assert action_result == phantom.APP_ERROR


def test_get_file_bad_file_hash(monkeypatch, cbcsdk_mock):
    """Test action with bad parameters"""
    obj = CBCSplunk()
    action = GetBinaryFileAction(obj, {"file_hash": "bad" * 21 + "#"})
    action.cbc = cbcsdk_mock.api

    action_result = action.call()
    assert obj.progress_message == "Malformed sha256 hash"
    assert action_result == phantom.APP_ERROR


def test_get_file_exception(monkeypatch, cbcsdk_mock, get_binary_metadata_response):
    """Test action - exception"""
    def post_resp(url, *args):
        return MockException(Exception)
    obj = CBCSplunk()
    action = GetBinaryFileAction(obj, {"file_hash": "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776"})
    action.cbc = cbcsdk_mock.api
    url = "/ubs/v1/orgs/test/sha256/87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776/metadata"
    cbcsdk_mock.mock_request("POST", "/ubs/v1/orgs/test/file/_download", post_resp)
    cbcsdk_mock.mock_request("GET",
                             url,
                             get_binary_metadata_response)
    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get binary file")

    action_result = action.call()
    assert "Could not find file" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_get_file_no_cbc(monkeypatch, cbcsdk_mock):
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = GetBinaryFileAction(obj, {"file_hash": "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776"})

    action.cbc = None
    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get binary file")

    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."


def test_get_file_fail_create_attachment(monkeypatch,
                                         cbcsdk_mock,
                                         get_binary_file_response,
                                         get_binary_metadata_response):
    """Test action with correct parameters - create attachment exception"""
    obj = CBCSplunk()
    action = GetBinaryFileAction(obj, {"file_hash": "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776"})
    action.cbc = cbcsdk_mock.api
    url = "/ubs/v1/orgs/test/sha256/87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776/metadata"
    cbcsdk_mock.mock_request("POST", "/ubs/v1/orgs/test/file/_download", get_binary_file_response)
    cbcsdk_mock.mock_request("GET",
                             url,
                             get_binary_metadata_response)
    monkeypatch.setattr(urllib.request, "urlopen", dummy_urlopen)

    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get binary file")
    monkeypatch.setattr('actions.action_get_file.Vault.create_attachment', lambda *args, **kwargs: {})
    action_result = action.call()
    assert obj.progress_message == "Could not create vault"
    assert action_result == phantom.APP_ERROR


def test_get_file_fail_get_file(monkeypatch,
                                cbcsdk_mock,
                                get_binary_file_response,
                                get_binary_metadata_response):
    """Test action with correct parameters - exception"""
    obj = CBCSplunk()
    action = GetBinaryFileAction(obj, {"file_hash": "87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776"})
    action.cbc = cbcsdk_mock.api
    url = "/ubs/v1/orgs/test/sha256/87976f3430cc99bc939e0694247c0759961a49832b87218f4313d6fc0bc3a776/metadata"
    cbcsdk_mock.mock_request("POST", "/ubs/v1/orgs/test/file/_download", get_binary_file_response)
    cbcsdk_mock.mock_request("GET",
                             url,
                             get_binary_metadata_response)

    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get binary file")
    monkeypatch.setattr('actions.action_get_file.Vault.create_attachment', lambda *args, **kwargs: "")
    action_result = action.call()
    assert "Could not fetch file" in obj.progress_message
    assert action_result == phantom.APP_ERROR
