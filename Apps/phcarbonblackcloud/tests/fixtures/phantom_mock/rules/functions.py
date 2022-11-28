"""Mock phantom.rules API functions for unit testing"""
import pytest


def delete_artifact(artifact_id=None):
    """This mocks the container automation API's delete artifact"""
    found = False
    if pytest.rules_connector is not None and artifact_id is not None:
        for artifact in list(pytest.rules_connector.artifacts):
            if artifact["id"] == artifact_id:
                pytest.rules_connector.artifacts.remove(artifact)
                found = True
                break
        return found
    else:
        return False


def set_connector(connector):
    """This is a helper function to set the connector to delete artifacts from"""
    pytest.rules_connector = connector
