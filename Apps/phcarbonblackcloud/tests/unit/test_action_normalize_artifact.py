"""Tests for normalize artifact action"""
import pytest
from cbc_sdk import CBCloudAPI
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.rules as rules
import phantom.app as phantom
from actions.action_on_poll import OnPollAction
from actions.action_normalize_artifact import NormalizeArtifactAction

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


def test_successful_normalize(cbcsdk_mock, get_one_alert_response):
    """Test action with correct parameters"""
    obj = CBCSplunk()
    action = OnPollAction(
        obj, {"start_time": 1, "end_time": 2, "artifact_count": 1, "container_count": 1}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/alerts/_search", get_one_alert_response
    )

    action_result = action.call()
    assert "Polling complete. Found 1" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS
    assert len(obj.artifacts) == 1
    assert obj.artifacts[0]["cef"]["alertId"] == "038894832709076d63111e99466f73575fcf3ca"
    obj.containers[0] = {
        "artifact_count": 1,
        "description": "Container added by Splunk",
        "name": "Splunk Log Entry",
        "status": "new",
        "severity": "high",
    }
    obj.artifacts[0]["cef"].pop("alertId")
    assert "alertId" not in obj.artifacts[0]

    action = NormalizeArtifactAction(
        obj, {"artifact_id": 0, "raw": obj.artifacts[0]["cef"]["_raw"]}
    )
    rules.set_connector(obj)
    action_result = action.call()

    assert action_result == phantom.APP_SUCCESS
    assert pytest.rules_connector == obj
    assert obj.artifacts[0]["cef"]["alertId"] == "038894832709076d63111e99466f73575fcf3ca"


def test_failure_normalize(monkeypatch, cbcsdk_mock, get_one_alert_response):
    """Test action with correct parameters, but failure to get container"""

    def prep_exc():
        return phantom.APP_ERROR, None, None

    obj = CBCSplunk()
    action = OnPollAction(
        obj, {"start_time": 1, "end_time": 2, "artifact_count": 1, "container_count": 1}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/alerts/_search", get_one_alert_response
    )

    action_result = action.call()
    assert "Polling complete. Found 1" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS
    assert len(obj.artifacts) == 1
    assert obj.artifacts[0]["cef"]["alertId"] == "038894832709076d63111e99466f73575fcf3ca"
    obj.containers[0] = {
        "artifact_count": 1,
        "description": "Container added by Splunk",
        "name": "Splunk Log Entry",
        "status": "new",
        "severity": "high",
    }
    obj.artifacts[0]["cef"].pop("alertId")
    assert "alertId" not in obj.artifacts[0]
    action = NormalizeArtifactAction(
        obj, {"artifact_id": 0, "raw": obj.artifacts[0]["cef"]["_raw"]}
    )
    monkeypatch.setattr(action.connector, "get_container_info", lambda *args, **kwargs: prep_exc())
    rules.set_connector(obj)
    action_result = action.call()

    assert action_result == phantom.APP_ERROR
    assert "Could not find container id" in obj.progress_message


def test_missing_params_normalize(cbcsdk_mock, get_one_alert_response):
    """Test action with missing parameters"""
    obj = CBCSplunk()
    action = OnPollAction(
        obj, {"start_time": 1, "end_time": 2, "artifact_count": 1, "container_count": 1}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/alerts/_search", get_one_alert_response
    )

    action_result = action.call()
    assert "Polling complete. Found 1" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS
    assert len(obj.artifacts) == 1
    assert obj.artifacts[0]["cef"]["alertId"] == "038894832709076d63111e99466f73575fcf3ca"
    obj.containers[0] = {
        "artifact_count": 1,
        "description": "Container added by Splunk",
        "name": "Splunk Log Entry",
        "status": "new",
        "severity": "high",
    }
    obj.artifacts[0]["cef"].pop("alertId")
    assert "alertId" not in obj.artifacts[0]

    action = NormalizeArtifactAction(obj, {"raw": obj.artifacts[0]["cef"]["_raw"]})
    rules.set_connector(obj)
    action_result = action.call()

    assert action_result == phantom.APP_ERROR
    assert "artifact_id or raw parameters not supplied" in obj.progress_message


def test_wrong_artifact_count_normalize(cbcsdk_mock, get_one_alert_response):
    """Test action with wrong artifact_count"""
    obj = CBCSplunk()
    action = OnPollAction(
        obj, {"start_time": 1, "end_time": 2, "artifact_count": 1, "container_count": 1}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/alerts/_search", get_one_alert_response
    )

    action_result = action.call()
    assert "Polling complete. Found 1" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS
    assert len(obj.artifacts) == 1
    assert obj.artifacts[0]["cef"]["alertId"] == "038894832709076d63111e99466f73575fcf3ca"
    obj.containers[0] = {
        "artifact_count": 2,
        "description": "Container added by Splunk",
        "name": "Splunk Log Entry",
        "status": "new",
        "severity": "high",
    }
    obj.artifacts[0]["cef"].pop("alertId")
    assert "alertId" not in obj.artifacts[0]

    action = NormalizeArtifactAction(
        obj, {"artifact_id": 0, "raw": obj.artifacts[0]["cef"]["_raw"]}
    )
    rules.set_connector(obj)
    action_result = action.call()

    assert action_result == phantom.APP_SUCCESS
    assert "Container does not contain Splunk SIEM ingested data" in obj.progress_message


def test_wrong_raw_normalize(cbcsdk_mock, get_one_alert_response):
    """Test action with unparsable raw parameter"""
    obj = CBCSplunk()
    action = OnPollAction(
        obj, {"start_time": 1, "end_time": 2, "artifact_count": 1, "container_count": 1}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/alerts/_search", get_one_alert_response
    )

    action_result = action.call()
    assert "Polling complete. Found 1" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS
    assert len(obj.artifacts) == 1
    assert obj.artifacts[0]["cef"]["alertId"] == "038894832709076d63111e99466f73575fcf3ca"
    obj.containers[0] = {
        "artifact_count": 1,
        "description": "Container added by Splunk",
        "name": "Splunk Log Entry",
        "status": "new",
        "severity": "high",
    }
    obj.artifacts[0]["cef"].pop("alertId")
    assert "alertId" not in obj.artifacts[0]

    action = NormalizeArtifactAction(obj, {"artifact_id": 0, "raw": "test"})
    rules.set_connector(obj)
    action_result = action.call()

    assert action_result == phantom.APP_ERROR
    assert "Invalid JSON data in raw parameter" in obj.progress_message


def test_could_not_delete_normalize(monkeypatch, cbcsdk_mock, get_one_alert_response):
    """Test action with correct parameters, but could not delete"""
    obj = CBCSplunk()
    action = OnPollAction(
        obj, {"start_time": 1, "end_time": 2, "artifact_count": 1, "container_count": 1}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/alerts/_search", get_one_alert_response
    )

    action_result = action.call()
    assert "Polling complete. Found 1" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS
    assert len(obj.artifacts) == 1
    assert obj.artifacts[0]["cef"]["alertId"] == "038894832709076d63111e99466f73575fcf3ca"
    obj.containers[0] = {
        "artifact_count": 1,
        "description": "Container added by Splunk",
        "name": "Splunk Log Entry",
        "status": "new",
        "severity": "high",
    }
    obj.artifacts[0]["cef"].pop("alertId")
    assert "alertId" not in obj.artifacts[0]

    action = NormalizeArtifactAction(
        obj, {"artifact_id": 0, "raw": obj.artifacts[0]["cef"]["_raw"]}
    )
    rules.set_connector(obj)
    monkeypatch.setattr(
        "actions.action_normalize_artifact.delete_artifact",
        lambda *args, **kwargs: False,
    )
    action_result = action.call()

    assert action_result == phantom.APP_SUCCESS
    assert "Could not delete original artifact, data duplication poss" in obj.progress_message


def test_failure_to_save_normalize(monkeypatch, cbcsdk_mock, get_one_alert_response):
    """Test action with correct parameters - failure to save artefact"""
    obj = CBCSplunk()
    action = OnPollAction(
        obj, {"start_time": 1, "end_time": 2, "artifact_count": 1, "container_count": 1}
    )
    action.cbc = cbcsdk_mock.api
    cbcsdk_mock.mock_request(
        "POST", "/appservices/v6/orgs/test/alerts/_search", get_one_alert_response
    )

    action_result = action.call()
    assert "Polling complete. Found 1" in obj.progress_message
    assert action_result == phantom.APP_SUCCESS
    assert len(obj.artifacts) == 1
    assert obj.artifacts[0]["cef"]["alertId"] == "038894832709076d63111e99466f73575fcf3ca"
    obj.containers[0] = {
        "artifact_count": 1,
        "description": "Container added by Splunk",
        "name": "Splunk Log Entry",
        "status": "new",
        "severity": "high",
    }
    obj.artifacts[0]["cef"].pop("alertId")
    assert "alertId" not in obj.artifacts[0]

    action = NormalizeArtifactAction(
        obj, {"artifact_id": 0, "raw": obj.artifacts[0]["cef"]["_raw"]}
    )
    rules.set_connector(obj)
    monkeypatch.setattr(obj, "save_artifact", lambda *args: (phantom.APP_ERROR, None, None))
    action_result = action.call()

    assert action_result == phantom.APP_ERROR
    assert "Could not save new artifact" in obj.progress_message
