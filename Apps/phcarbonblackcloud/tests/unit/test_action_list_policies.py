"""Tests for list device policies"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_list_policies import ListPoliciesAction

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


def test_list_policies_success(cbcsdk_mock, get_policies_object):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = ListPoliciesAction(obj, {})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/policyservice/v1/orgs/test/policies/summary",
        get_policies_object,
    )
    action_result = action.call()
    assert obj.progress_message == "Successfully fetched policies list"
    assert action_result == phantom.APP_SUCCESS


def test_list_policies_exception(cbcsdk_mock):
    """Test action - exception"""

    def post_resp(*args, **kwargs):
        return MockException(Exception)

    obj = CBCSplunk()
    action = ListPoliciesAction(obj, {})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET",
        "/policyservice/v1/orgs/test/policies/summary",
        post_resp,
    )
    action_result = action.call()
    assert "Could not list policies" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_list_policies_no_cbc():
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = ListPoliciesAction(obj, {})
    action.cbc = None
    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."
