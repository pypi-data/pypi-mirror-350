from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from metaworkflows.core.connections import BaseConnectionManager

class BaseEngine(ABC):
    def __init__(self, engine_config: Dict[str, Any], connections: BaseConnectionManager):
        self.engine_config = engine_config
        self.connections = connections # Global connection map

    @abstractmethod
    def initialize(self):
        """Initialize the engine session (e.g., SparkSession)."""
        pass

    @abstractmethod
    def read(self, connector_type: str, connection_ref: Optional[str], options: Dict[str, Any]) -> Any:
        """Read data from a source."""
        pass

    @abstractmethod
    def transform(self, step_config: Any, dataframes: Dict[str, Any]) -> Any:
        """Apply transformations to the data."""
        pass

    @abstractmethod
    def write(self, dataframe: Any, connector_type: str, connection_ref: Optional[str], options: Dict[str, Any]):
        """Write data to a sink."""
        pass

    @abstractmethod
    def custom_script(self, step_config: Any):
        """Custom script execution."""
        pass

    @abstractmethod
    def cleanup(self):
        """Clean up engine resources (e.g., stop SparkSession)."""
        pass

    def get_connection_details(self, connection_ref: str) -> Dict[str, Any]:
        """Helper to get connection details from the global map."""
        if not connection_ref:
            raise ValueError("Connection reference cannot be empty for I/O operations that require it.")
        conn_details = self.connections.get_connection(connection_ref)
        if not conn_details:
            raise ValueError(f"Connection reference '{connection_ref}' not found in connections.yaml.")
        return conn_details