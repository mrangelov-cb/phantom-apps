"""Tests for ban hash"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_ban_hash import BanHashAction

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


def test_ban_hash_success(cbcsdk_mock, get_binary_object, get_reputation_override_sha256_object):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = BanHashAction(
        obj,
        {"process_hash": "1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794"},
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/reputations/overrides",
        get_reputation_override_sha256_object,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/ubs/v1/orgs/test/sha256/1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794/metadata",
        get_binary_object,
    )

    action_result = action.call()
    assert (
        obj.progress_message
        == "Hash 1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794 was banned."
    )
    assert action_result == phantom.APP_SUCCESS


def test_ban_hash_missing_process_hash(cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = BanHashAction(obj, {})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "Missing process hash."
    assert action_result == phantom.APP_ERROR


def test_ban_hash_exception(cbcsdk_mock, get_binary_object):
    """Test action - exception"""

    def post_resp(*args, **kwargs):
        return MockException(Exception)

    obj = CBCSplunk()
    action = BanHashAction(
        obj,
        {"process_hash": "1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794"},
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/reputations/overrides",
        post_resp,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/ubs/v1/orgs/test/sha256/1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794/metadata",
        get_binary_object,
    )
    action_result = action.call()
    assert (
        "Could not ban 1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794"
        in obj.progress_message
    )
    assert action_result == phantom.APP_ERROR


def test_ban_hash_binary_exception(cbcsdk_mock, get_reputation_override_sha256_object):
    """Test action - exception"""

    def post_resp(*args, **kwargs):
        return MockException(Exception)

    def create_override(url, *args):
        data = {
            "sha256_hash": "1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794",
            "override_type": "SHA256",
            "override_list": "BLACK_LIST",
            "filename": "Actor name not defined",
            "description": "Banned via Splunk Soar Action",
        }
        assert args[0] == data
        return get_reputation_override_sha256_object

    obj = CBCSplunk()
    action = BanHashAction(
        obj,
        {"process_hash": "1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794"},
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/reputations/overrides",
        create_override,
    )
    cbcsdk_mock.mock_request(
        "GET",
        "/ubs/v1/orgs/test/sha256/1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794/metadata",
        post_resp,
    )
    action_result = action.call()
    assert (
        obj.progress_message
        == "Hash 1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794 was banned."
    )
    assert action_result == phantom.APP_SUCCESS


def test_ban_hash_no_cbc():
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = BanHashAction(
        obj,
        {"process_hash": "1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794"},
    )
    action.cbc = None

    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."
