import yaml
from pathlib import Path
import logging
from typing import Dict, List, Any
from google.cloud import storage

logger = logging.getLogger(__name__)


class JobStep:
    def __init__(self, step_config: Dict[str, Any]):
        self.name: str = step_config.get("step_name", "Unnamed Step")
        # "read", "write", "transform"
        self.type: str = step_config.get("type")
        self.connector: str = step_config.get("connector")  # For read/write
        self.connection_ref: str = step_config.get(
            "connection_ref")  # For read/write
        self.options: Dict[str, Any] = step_config.get("options", {})
        self.engine_specific: Dict[str, Any] = step_config.get(
            "engine_specific", {})
        self.input_aliases: List[str] = step_config.get(
            "input_aliases", [])  # for transfrom config
        self.input_alias: str = step_config.get(
            "input_alias")  # for write config
        self.output_alias: str = step_config.get("output_alias")

        if not self.type:
            raise ValueError(f"Step '{self.name}' is missing a 'type'.")
        logger.debug(f"Initialized JobStep: {self.name} (Type: {self.type})")


class Job:
    def __init__(self, job_name: str, description: str, version: str, engine_config: Dict[str, Any], steps: List[JobStep]):
        self.job_name = job_name
        self.description = description
        self.version = version
        self.engine_config = engine_config
        self.steps = steps
        logger.info(
            f"Job '{self.job_name}' (v{self.version}) loaded with {len(self.steps)} steps.")

    @classmethod
    def from_yaml(cls, file_path: str) -> 'Job':
        """Loads a job definition from a YAML file."""
        if file_path.startswith("gs://"):
            # Read from Google Cloud Storage
            try:
                client = storage.Client()
                bucket_name, blob_name = file_path[5:].split("/", 1)
                bucket = client.bucket(bucket_name)
                blob = bucket.blob(blob_name)
                yaml_content = blob.download_as_text()
                config = yaml.safe_load(yaml_content)
            except Exception as e:
                logger.error(f"Error reading YAML from GCS: {e}")
                raise
        else:
            # Read from local file
            path = Path(file_path)
            if not path.exists():
                logger.error(f"Job YAML file not found: {file_path}")
                raise FileNotFoundError(f"Job YAML file not found: {file_path}")

            with open(path, 'r') as f:
                try:
                    config = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    logger.error(f"Error parsing YAML file {file_path}: {e}")
                    raise

        job_name = config.get("job_name", "Untitled Job")
        description = config.get("description", "")
        version = config.get("version", "1.0")
        engine_config = config.get("engine", {})
        step_configs = config.get("steps", [])

        if not engine_config or not engine_config.get("type"):
            raise ValueError(
                f"Job '{job_name}' is missing engine type configuration.")

        steps = [JobStep(step_conf) for step_conf in step_configs]

        return cls(job_name, description, version, engine_config, steps)

    def get_engine_type(self) -> str:
        return self.engine_config.get("type").lower()
