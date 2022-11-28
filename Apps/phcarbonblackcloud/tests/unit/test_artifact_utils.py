"""Tests for cbcapp connector"""
from cbcapp_connector import CarbonBlackCloudSplunkSoarAppConnector as CBCSplunk
import phantom.rules as rules
from utils.artifact_utils import prepare_artifact, delete_artifact


class MockException:
    """MockException class for Exceptions"""

    def __init__(self, *args, **kwargs):
        """Raising exception"""
        raise Exception


# ==================================== UNIT TESTS BELOW ====================================


def test_prepare_artifact(get_one_alert_response):
    """Test prepare artifact helper function"""
    config = {"ingest": {}}
    config["ingest"]["container_label"] = "event"
    artifact = prepare_artifact(get_one_alert_response["results"][0], config)
    assert artifact["cef"]["alertId"] == "038894832709076d63111e99466f73575fcf3ca"
    assert artifact["severity"] == "low"
    assert artifact["name"] == "CBC CB_ANALYTICS - some-system"


def test_delete_artifact(get_one_alert_response):
    """Test delete artifact"""
    obj = CBCSplunk()
    rules.set_connector(obj)
    config = {"ingest": {}}
    config["ingest"]["container_label"] = "event"
    artifact = prepare_artifact(get_one_alert_response["results"][0], config)
    obj.save_artifact(artifact)
    assert len(obj.artifacts) == 1
    delete_artifact(0)
    assert len(obj.artifacts) == 0
