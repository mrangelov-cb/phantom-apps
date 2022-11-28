"""Tests for unban hash"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_unban_hash import UnbanHashAction

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


def test_unban_hash_success(cbcsdk_mock, get_reputation_override_sha256_search_single_response):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = UnbanHashAction(
        obj,
        {"process_hash": "af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a"},
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/reputations/overrides/_search",
        get_reputation_override_sha256_search_single_response,
    )
    cbcsdk_mock.mock_request(
        "DELETE",
        "/appservices/v6/orgs/test/reputations/overrides/e9410b754ea011ebbfd0db2585a41b07",
        None,
    )
    action_result = action.call()
    assert (
        obj.progress_message
        == "Hash af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a was unbanned."
    )
    assert action_result == phantom.APP_SUCCESS


def test_unban_hash_multiple_records(
    cbcsdk_mock, get_reputation_override_sha256_search_multiple_response
):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = UnbanHashAction(
        obj,
        {"process_hash": "af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a"},
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/reputations/overrides/_search",
        get_reputation_override_sha256_search_multiple_response,
    )
    cbcsdk_mock.mock_request(
        "DELETE",
        "/appservices/v6/orgs/test/reputations/overrides/e9410b754ea011ebbfd0db2585a41b07",
        None,
    )
    action_result = action.call()
    assert (
        obj.progress_message
        == "There are multiple records for af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a."
    )
    assert action_result == phantom.APP_ERROR


def test_unban_hash_missing_process_hash(cbcsdk_mock):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = UnbanHashAction(obj, {})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "Missing process hash."
    assert action_result == phantom.APP_ERROR


def test_unban_hash_exception(cbcsdk_mock):
    """Test action - exception"""
    obj = CBCSplunk()
    action = UnbanHashAction(
        obj,
        {"process_hash": "1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794"},
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/reputations/overrides/_search",
        lambda *_: MockException(Exception),
    )
    action_result = action.call()
    assert (
        "Could not unban 1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794"
        in obj.progress_message
    )
    assert action_result == phantom.APP_ERROR


def test_unban_hash_success_no_override(
    cbcsdk_mock, get_reputation_override_sha256_search_no_response
):
    """Test action - no override available"""
    obj = CBCSplunk()
    action = UnbanHashAction(
        obj,
        {"process_hash": "af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a"},
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/reputations/overrides/_search",
        get_reputation_override_sha256_search_no_response,
    )
    action_result = action.call()
    assert (
        obj.progress_message
        == "The process af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a was not banned."
    )
    assert action_result == phantom.APP_SUCCESS


def test_unban_hash_no_cbc(monkeypatch, cbcsdk_mock):
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = UnbanHashAction(
        obj,
        {"process_hash": "1436cdbddc9aa21a3ef2a17994493dac4cb9fb92739401c55ee1091be625b794"},
    )
    action.cbc = None
    monkeypatch.setattr(CBCSplunk, "get_action_identifier", lambda arg: "unban hash")

    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."
