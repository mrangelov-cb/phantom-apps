"""Mock BaseConnector class for unit tests"""
import phantom.app as phantom
import json


class BaseConnector:
    """The base connector class with stubs"""

    def __init__(self):
        """The constructor for the mock class"""
        self.config = {
            "server_url": "test",
            "custom_connector_id": "test",
            "custom_key": "test",
            "org_key": "test",
            "fetch_cb_analytics": True,
            "fetch_device_control": True,
            "fetch_watchlist": True,
            "fetch_container_runtime": False,
            "min_severity": 1,
            "ingest": {"container_label": "events"},
        }
        self.asset_id = "1abc234"
        self.app_id = "1abc1234"
        self.app_json_file_loc = None
        self.container_id = 0
        self.container_info = {
            "1": {"test123": True},
        }
        self.starting_container_id = 0
        self.starting_artifact_id = 0
        self.product_install_id = "1234"
        self.product_version = "1.0.0"
        self.state_file_location = "state_file"
        self.poll_now = False
        self.base_url = "https://127.0.0.1"
        self.message = ""
        self.progress_message = ""
        self.state = None
        self.status = None
        self.action_results = []
        self.action_identifier = ""
        self.logger = None
        self.containers = []
        self.artifacts = []
        return

    def get_config(self):
        """Get config stub"""
        return self.config

    def get_phantom_base_url(self):
        """Get base url stub"""
        return self.base_url

    def get_container_id(self):
        """Get container id stub"""
        return self.container_id

    def get_container_info(self, container_id=None):
        """Get container info stub"""
        if not container_id:
            container_id = self.container_id
        return True, self.containers[container_id], "200"

    def get_product_installation_id(self):
        """Get product install id stub"""
        return self.product_install_id

    def get_product_version(self):
        """Get version stub"""
        return self.product_version

    def load_state(self):
        """Connector state loader stub"""
        with open(self.state_file_location, "r+") as state_file:
            self.state = json.loads(state_file.read() or "{}")
        return self.state

    def get_state(self):
        """State getter stub"""
        return self.state

    def save_state(self, state=None):
        """State save stub"""
        self.state = state or self.state
        with open(self.state_file_location, "w+") as state_file:
            state_file.write(json.dumps(self.state))
        return

    def save_artifact(self, artifact):
        """Artifact creating method stub"""
        artifact_id = self.starting_artifact_id
        artifact["id"] = artifact_id
        self.starting_artifact_id += 1
        self.artifacts.append(artifact)
        return (phantom.APP_SUCCESS, "Artifact saved", artifact_id)

    def save_artifacts(self, artifacts):
        """Artifact save method stub"""
        return_val = []
        for artifact in artifacts:
            self.artifacts.append(artifact)
            return_val.append([phantom.APP_SUCCESS, "Artifact saved", self.starting_artifact_id])
            self.starting_artifact_id += 1

        return return_val

    def save_container(self, container):
        """Save container - stub method"""
        container_id = self.starting_artifact_id
        self.starting_container_id += 1
        self.containers.append(container)
        return (phantom.APP_SUCCESS, "Container saved", container_id)

    def save_containers(self, containers):
        """Save multiple containers - stub"""
        return_val = []
        for container in containers:
            self.containers.append(container)
            return_val.append([phantom.APP_SUCCESS, "Container saved", self.starting_container_id])
            self.starting_container_id += 1

        return return_val

    def debug_print(self, message, dump_obj=None):
        """Dummy debug print"""
        pass

    def error_print(self, message, dump_obj=None):
        """Dummy error print"""
        pass

    def set_status(self, status, message=None, error=None):
        """Action set status stub"""
        self.status = status
        self.message = message
        return status

    def append_to_message(self, message):
        """Append to message stub"""
        self.message += message
        return

    def set_status_save_progress(self, status, message):
        """Save progress stub"""
        self.status = status
        self.progress_message = message
        return self.status

    def send_progress(self, message):
        """Send progress stub"""
        self.progress_message = message
        return

    def save_progress(self, message, more=None):
        """Save progress stub"""
        self.progress_message = message
        return

    def add_action_result(self, action_result):
        """Action result add stub"""
        action_result.set_logger(self.logger)
        self.action_results.append(action_result)
        return action_result

    def get_status(self):
        """Status getter stub"""
        return self.status

    def get_status_message(self):
        """Status message getter stub"""
        return self.message

    def get_action_identifier(self):
        """Action identifier getter"""
        return self.action_identifier

    def is_poll_now(self):
        """Manual poll trigger getter"""
        return self.poll_now

    def get_app_id(self):
        """APP ID getter stub"""
        return self.app_id

    def get_asset_id(self):
        """Asset ID getter"""
        return self.asset_id

    def set_validator(self, type=None, validation_function=None):
        """Validator setter stub"""
        return None
