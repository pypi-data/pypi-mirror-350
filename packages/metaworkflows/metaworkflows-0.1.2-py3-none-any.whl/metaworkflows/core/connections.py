import os
import yaml
from abc import ABC, abstractmethod
from google.cloud import storage
import logging
import subprocess

logger = logging.getLogger(__name__)

def load_connections(file_path):
    """Loads connection configurations from a local file or GCS."""
    content = None
    if str(file_path).startswith("gs://"):
        # Read from Google Cloud Storage
        try:
            client = storage.Client()
            bucket_name, blob_name = str(file_path)[5:].split("/", 1)
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            content = blob.download_as_text()
            logger.info(f"Loaded connections from GCS: {file_path}")
        except Exception as e:
            logger.error(f"Error reading connections from GCS: {e}")
            return {}
    else:
        # Read from local file
        if not file_path.exists():
            logger.error(f"Connections configuration file not found: {file_path}")
            return {}
        with open(file_path, 'r') as f:
            content = f.read()
        logger.info(f"Loaded connections from local file: {file_path}")

    if content is None:
        return {}

    # Simple environment variable substitution
    import re
    for match in re.finditer(r"\$\{(.*?)\}", content):
        env_var = match.group(1)
        value = os.getenv(env_var, "")
        content = content.replace(f"${{{env_var}}}", value)

    try:
        connections = yaml.safe_load(content)
        return connections.get('connections', {}) if connections else {}
    except yaml.YAMLError as e:
        logger.error(f"Error parsing connections YAML: {e}")
        return {}

class BaseConnectionManager(ABC):
    """Abstract base class for connection managers."""

    @abstractmethod
    def get_connection(self, connection_name):
        """Retrieve a specific connection by name."""
        pass


# setup_logging()
class ConnectionManager(BaseConnectionManager):
    """Manages connections with lazy loading."""
    def __init__(self, file_path):
        self.file_path = file_path
        self._connections = None

    def _load_connections(self):
        """Loads connection configurations."""
        return load_connections(self.file_path)

    def get_connection(self, connection_name):
        """Retrieve a specific connection by name."""
        if self._connections is None:
            self._connections = self._load_connections()
        return self._connections.get(connection_name)


# class ConnectionSecretManager(BaseConnectionManager):
#     def __init__(self, project_id):
#         self.project_id = project_id
#         self.client = secretmanager.SecretManagerServiceClient()

#     def _get_secret(self, secret_name, version="latest"):
#         try:
#             secret_path = f"projects/{self.project_id}/secrets/{secret_name}/versions/{version}"
#             response = self.client.access_secret_version(name=secret_path)
#             return response.payload.data.decode("UTF-8")
#         except Exception as e:
#             logging.error(f"Failed to retrieve secret '{secret_name}': {e}")
#             return None

#     def get_connection(self, secret_name):
#         """Retrieve connection configurations from a secret."""
#         secret_data = self._get_secret(secret_name)
#         if not secret_data:
#             return {}

#         # Parse the secret data as YAML
#         try:
#             connection = yaml.safe_load(secret_data)
#             return connection if connection else {}
#         except yaml.YAMLError as e:
#             logging.error(f"Failed to parse secret data as YAML: {e}")
#             return {}

class GCloudConnectionSecretManager(BaseConnectionManager):
    def __init__(self):
        # self.project_id = project_id
        pass

    def _get_secret(self, secret_name, version="latest"):
        try:
            # Construct the gcloud command
            # secret_path = f"projects/{self.project_id}/secrets/{secret_name}/versions/{version}"
            command = [
                "gcloud", "secrets", "versions", "access", version,
                f"--secret={secret_name}"
            ]
            # Execute the gcloud command
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to retrieve secret '{secret_name}': {e.stderr}")
            return None

    def get_connection(self, secret_name):
        """Retrieve connection configurations from a secret."""
        secret_data = self._get_secret(secret_name)
        if not secret_data:
            return {}

        # Parse the secret data as YAML
        try:
            connection = yaml.safe_load(secret_data)
            return connection if connection else {}
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse secret data as YAML: {e}")
            return {}
        
def get_connection_manager(source_type: str, **kwargs):
    """
    Factory function to create a connection manager instance.

    Args:
        source_type (str): The type of connection manager to use. 
                           Options: 'file', 'secret'.
        kwargs: Additional arguments required for the specific connection manager.

    Returns:
        ConnectionManager or ConnectionSecretManager instance.

    Raises:
        ValueError: If an invalid source_type is provided.
    """
    if source_type == "file":
        file_path = kwargs.get("file_path")
        if not file_path:
            raise ValueError("file_path is required for ConnectionManager.")
        return ConnectionManager(file_path=file_path)

    elif source_type == "secret":
        # project_id = kwargs.get("project_id")
        # if not project_id:
            # raise ValueError("project_id is required for ConnectionSecretManager.")
        return GCloudConnectionSecretManager()

    else:
        raise ValueError(f"Invalid source_type '{source_type}'. Must be 'file' or 'secret'.")