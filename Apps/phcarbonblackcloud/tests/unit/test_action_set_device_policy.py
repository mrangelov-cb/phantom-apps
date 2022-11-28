"""Tests for set device policy"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.app as phantom
from actions.action_set_device_policy import SetDevicePolicyAction

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


def test_set_device_policy_id_success(
    cbcsdk_mock, get_dummy_policy_object, get_device_object
):
    """Test action with policy ID"""
    obj = CBCSplunk()
    action = SetDevicePolicyAction(obj, {"device_id": 6023, "policy_id": 8675309})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/policyservice/v1/orgs/test/policies/8675309", get_dummy_policy_object
    )
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/6023", get_device_object
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/device_actions",
        CBCSDKMock.StubResponse(None, scode=204),
    )
    action_result = action.call()
    assert obj.progress_message == "Successfully set device policy"
    assert action_result == phantom.APP_SUCCESS


def test_set_device_policy_name_success(
    cbcsdk_mock, get_policies_object, get_device_object
):
    """Test action with policy name"""
    obj = CBCSplunk()
    action = SetDevicePolicyAction(obj, {"device_id": 6023, "policy_name": "Standard"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/policyservice/v1/orgs/test/policies/summary", get_policies_object
    )
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/6023", get_device_object
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/device_actions",
        CBCSDKMock.StubResponse(None, scode=204),
    )
    action_result = action.call()
    assert obj.progress_message == "Successfully set device policy"
    assert action_result == phantom.APP_SUCCESS


def test_set_device_policy_id_name_success(
    cbcsdk_mock, get_dummy_policy_object, get_device_object
):
    """Test action with policy ID and policy name"""
    obj = CBCSplunk()
    action = SetDevicePolicyAction(
        obj, {"device_id": 6023, "policy_id": 65536, "policy_name": "A Dummy Policy"}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/policyservice/v1/orgs/test/policies/65536", get_dummy_policy_object
    )
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/6023", get_device_object
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/device_actions",
        CBCSDKMock.StubResponse(None, scode=204),
    )
    action_result = action.call()
    assert obj.progress_message == "Successfully set device policy"
    assert action_result == phantom.APP_SUCCESS


def test_set_device_policy_id_name_mismatch(
    cbcsdk_mock, get_dummy_policy_object, get_device_object
):
    """Test action with policy name and policy ID mismatch"""
    obj = CBCSplunk()
    action = SetDevicePolicyAction(
        obj, {"device_id": 6023, "policy_name": "St", "policy_id": 65536}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/policyservice/v1/orgs/test/policies/65536", get_dummy_policy_object
    )
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/6023", get_device_object
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/device_actions",
        CBCSDKMock.StubResponse(None, scode=204),
    )
    action_result = action.call()
    assert "Policy ID and policy name mismatch" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS


def test_set_device_policy_exception(
    cbcsdk_mock, get_dummy_policy_object, get_device_object
):
    """Test action - Exception due to update policy error"""

    def post_resp(*args, **kwargs):
        return MockException(Exception)

    obj = CBCSplunk()
    action = SetDevicePolicyAction(obj, {"device_id": 6023, "policy_id": 8675309})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/policyservice/v1/orgs/test/policies/8675309", get_dummy_policy_object
    )
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/6023", get_device_object
    )
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/device_actions", post_resp
    )
    action_result = action.call()
    assert "Could not set device policy" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_set_device_policy_no_cbc():
    """Test action with missing cbc connection"""
    obj = CBCSplunk()
    action = SetDevicePolicyAction(obj, {})
    action.cbc = None
    action_result = action.call()
    assert action_result == phantom.APP_ERROR
    assert obj.progress_message == "Please configure all connection parameters."


def test_set_device_policy_missing_policy(cbcsdk_mock):
    """Test action with missing parameters: policy_id and/or policy_name"""
    obj = CBCSplunk()
    action = SetDevicePolicyAction(obj, {"device_id": 6023})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "You must provide policy_id or policy_name"
    assert action_result == phantom.APP_ERROR


def test_set_device_policy_missing_device_id(cbcsdk_mock):
    """Test action with missing device id"""
    obj = CBCSplunk()
    action = SetDevicePolicyAction(obj, {})
    action.cbc = cbcsdk_mock.api
    action_result = action.call()
    assert obj.progress_message == "Missing device id."
    assert action_result == phantom.APP_ERROR


def test_set_device_policy_exception_id(cbcsdk_mock):
    """Test action - Exception due to Policy select error when policy ID is used"""

    def post_resp(url, *args):
        return MockException(Exception)

    obj = CBCSplunk()
    action = SetDevicePolicyAction(obj, {"device_id": 354648, "policy_id": 65536})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/policyservice/v1/orgs/test/policies/65536", post_resp
    )
    action_result = action.call()
    assert "Could not get device policy:" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_set_device_policy_exception_name(cbcsdk_mock):
    """Test action - Exception due to Policy select error when policy name is used"""

    def post_resp(url, *args):
        return MockException(Exception)

    obj = CBCSplunk()
    action = SetDevicePolicyAction(
        obj, {"device_id": 354648, "policy_name": "Standard"}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/policyservice/v1/orgs/test/policies/summary", post_resp
    )
    action_result = action.call()
    assert "Could not get device policy" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_set_device_policy_exception_device(cbcsdk_mock, get_dummy_policy_object):
    """Test action - Exception due to Device select error"""

    def post_resp(url, *args):
        return MockException(Exception)

    obj = CBCSplunk()
    action = SetDevicePolicyAction(obj, {"device_id": 6023, "policy_id": 8675309})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/policyservice/v1/orgs/test/policies/8675309", get_dummy_policy_object
    )
    cbcsdk_mock.mock_request("GET", "/appservices/v6/orgs/test/devices/6023", post_resp)
    action_result = action.call()
    assert "Could not select device" in obj.progress_message
    assert action_result == phantom.APP_ERROR


def test_set_device_policy_name_no_policy_found(
    cbcsdk_mock, get_policies_object, get_device_object
):
    """Test action with policy name - no policy found"""
    obj = CBCSplunk()
    action = SetDevicePolicyAction(obj, {"device_id": 6023, "policy_name": "Standard2"})
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "GET", "/policyservice/v1/orgs/test/policies/summary", get_policies_object
    )
    cbcsdk_mock.mock_request(
        "GET", "/appservices/v6/orgs/test/devices/6023", get_device_object
    )
    cbcsdk_mock.mock_request(
        "POST",
        "/appservices/v6/orgs/test/device_actions",
        CBCSDKMock.StubResponse(None, scode=204),
    )
    action_result = action.call()
    assert obj.progress_message == "Could not get device policy - no such policy Standard2"
    assert action_result == phantom.APP_ERROR
