from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseReader(ABC):
    def __init__(self, connection_details: Optional[Dict[str, Any]] = None):
        """
        Initialize the reader.
        :param connection_details: Dictionary containing connection parameters.
        """
        self.connection_details = connection_details if connection_details else {}

    @abstractmethod
    def read(self, options: Dict[str, Any]) -> Any:
        """
        Read data based on the provided options.
        :param options: Dictionary of options specific to the reader and data source.
        :return: Data read from the source (e.g., pandas DataFrame, Spark DataFrame).
        """
        pass

class BaseWriter(ABC):
    def __init__(self, connection_details: Optional[Dict[str, Any]] = None):
        """
        Initialize the writer.
        :param connection_details: Dictionary containing connection parameters.
        """
        self.connection_details = connection_details if connection_details else {}

    @abstractmethod
    def write(self, data: Any, options: Dict[str, Any]):
        """
        Write data based on the provided options.
        :param data: Data to be written (e.g., pandas DataFrame, Spark DataFrame).
        :param options: Dictionary of options specific to the writer and data sink.
        """
        pass