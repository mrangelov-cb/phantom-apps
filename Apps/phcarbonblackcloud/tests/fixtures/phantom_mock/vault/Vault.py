"""Mock Vault class for unit tests"""
import hashlib
import uuid


class Vault():
    """The Vault class"""
    TEMP_PATH = None
    VAULT_PATHS = {}
    vaults = []

    def __init__(self):
        """Constructor"""
        return

    @classmethod
    def add_attachment(clas, file_location, container_id, file_name=None, metadata=None):
        """Add attachment stub (this API method is deprecated)"""
        sha1_hash = None
        with open(file_location, 'r') as vault_file:
            vault_data = vault_file.read()
            sha1_data = hashlib.sha1(vault_data)
            sha1_hash = sha1_data.hexdigest()

        return {
            'container': container_id,
            'message': 'success',
            'file_name': (file_name or str(uuid.uuid4())),
            'succeeded': True,
            'hash': sha1_hash
        }

    @classmethod
    def create_attachment(cls, file_contents, container_id, file_name=None, metadata=None):
        """Create attachment stub"""
        vault_data = file_contents.encode('utf-8')
        sha1_data = hashlib.sha1(vault_data)
        sha1_hash = sha1_data.hexdigest()

        vault = {
            'container': container_id,
            'message': 'success',
            'file_name': (file_name or str(uuid.uuid4())),
            'succeeded': True,
            'hash': sha1_hash
        }
        cls.vaults.append(vault)
        return vault

    @classmethod
    def get_vault_tmp_dir(cls):
        """Should not be used, deprecated"""
        return '/tmp'

    @classmethod
    def get_file_path(cls, vault_id):
        """Should not be used, deprecated"""
        return Vault.VAULT_PATHS.get(vault_id)

    # TODO: Implement this
    @classmethod
    def get_file_info(cls, vault_id=None, file_name=None, container_id=None):
        """Dummy method"""
        return {}
