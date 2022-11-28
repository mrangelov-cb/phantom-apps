"""Tests for get file"""
import pytest
import io
from cbc_sdk import CBCloudAPI
from cbc_sdk.connection import Connection
from cbc_sdk.credentials import Credentials
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_get_file import GetFileAction

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


@pytest.fixture(scope="function")
def connection_mock(monkeypatch, cb):
    """Mocks Connection for unit tests"""
    creds = Credentials({'url': 'https://example.com', 'token': 'ABCDEFGH'})
    conn = Connection(creds)
    monkeypatch.setattr(conn, "get", get_file_content)
    cb.session = conn
    return conn

# ==================================== UNIT TESTS BELOW ====================================


def test_get_file_success(monkeypatch,
                          cbcsdk_mock,
                          connection_mock,
                          get_device_object,
                          get_session_init_object,
                          get_session_poll_object,
                          get_file_resp_object):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = GetFileAction(obj, {"device_id": 354648, "file_name": "test.txt"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/354648", get_device_object
    )
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/liveresponse/sessions", get_session_init_object)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', get_session_poll_object)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             get_file_resp_object)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/10',
                             get_file_resp_object)

    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get file")

    action_result = action.call()
    assert obj.progress_message == "File successfully retrieved"
    assert action_result == phantom.APP_SUCCESS


def test_get_file_missing_file_name(monkeypatch, cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = GetFileAction(obj, {"device_id": 354648})
    action.cbc = cbcsdk_mock.api
    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get file")

    action_result = action.call()
    assert obj.progress_message == "No file_name provided"
    assert action_result == phantom.APP_ERROR


def test_get_file_missing_device_id(monkeypatch, cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = GetFileAction(obj, {"file_name": "test"})
    action.cbc = cbcsdk_mock.api
    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get file")

    action_result = action.call()
    assert obj.progress_message == "Missing device id."
    assert action_result == phantom.APP_ERROR


def test_get_file_exception(monkeypatch, cbcsdk_mock):
    """Test action - exception"""
    def post_resp(url, *args):
        return MockException(Exception)
    obj = CBCSplunk()
    action = GetFileAction(obj, {"device_id": 354648, "file_name": "test"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/354648", post_resp
    )
    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get file")

    action_result = action.call()
    assert "Could not get file" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_get_file_no_cbc(monkeypatch, cbcsdk_mock):
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = GetFileAction(obj, {"device_id": 354648, "file_name": "test"})
    action.cbc = None
    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get file")

    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."


def test_get_file_fail_create_attachment(monkeypatch,
                                         cbcsdk_mock,
                                         connection_mock,
                                         get_device_object,
                                         get_session_init_object,
                                         get_session_poll_object,
                                         get_file_resp_object):
    """Test action with correct parameters - create attachment exception"""
    obj = CBCSplunk()
    action = GetFileAction(obj, {"device_id": 354648, "file_name": "test.txt"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/354648", get_device_object
    )
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/liveresponse/sessions", get_session_init_object)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', get_session_poll_object)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             get_file_resp_object)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/10',
                             get_file_resp_object)

    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get file")
    monkeypatch.setattr('actions.action_get_file.Vault.create_attachment', lambda *args, **kwargs: {})
    action_result = action.call()
    assert obj.progress_message == "Could not create vault"
    assert action_result == phantom.APP_ERROR


def test_get_file_fail_get_file(monkeypatch,
                                cbcsdk_mock,
                                connection_mock,
                                get_device_object,
                                get_session_init_object,
                                get_session_poll_object,
                                get_file_resp_object):
    """Test action with correct parameters - exception"""
    obj = CBCSplunk()
    action = GetFileAction(obj, {"device_id": 354648, "file_name": "test.txt"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/354648", get_device_object
    )
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/liveresponse/sessions", get_session_init_object)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', get_session_poll_object)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             get_file_resp_object)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/10',
                             get_file_resp_object)

    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get file")
    monkeypatch.setattr('actions.action_get_file.Vault.create_attachment', lambda *args, **kwargs: "")
    action_result = action.call()
    assert "Could not get file" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_get_file_fail_to_start_lr(monkeypatch,
                                   cbcsdk_mock,
                                   connection_mock,
                                   get_device_object):
    """Test action with correct parameters - fail to start lr"""
    def post_resp(url, *args):
        return MockException(Exception)
    obj = CBCSplunk()
    action = GetFileAction(obj, {"device_id": 354648, "file_name": "test.txt"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/354648", get_device_object
    )
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/liveresponse/sessions", post_resp)

    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get file")
    action_result = action.call()
    assert "Could not establish LR session" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_get_file_fail_to_get_file_contents(monkeypatch,
                                            cbcsdk_mock,
                                            connection_mock,
                                            get_device_object,
                                            get_session_init_object,
                                            get_session_poll_object,
                                            get_file_resp_object):
    """Test action with correct parameters - get file contents exception"""
    def post_resp(url, *args):
        return MockException(Exception)
    obj = CBCSplunk()
    action = GetFileAction(obj, {"device_id": 354648, "file_name": "test.txt"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/354648", get_device_object
    )
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/liveresponse/sessions", get_session_init_object)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', get_session_poll_object)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             get_file_resp_object)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/10',
                             post_resp)

    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "get file")
    monkeypatch.setattr('actions.action_get_file.Vault.create_attachment', lambda *args, **kwargs: {})
    action_result = action.call()
    assert "Could not get file contents" in obj.progress_message
    assert action_result == phantom.APP_ERROR
