from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, spark: Any, config: Dict[str, Any], dataframes: Dict[str, Any]) -> Any:
        """
        Apply transformation.
        :param spark: SparkSession or other engine context (can be None for Python native).
        :param config: Configuration for the transformation (e.g., SQL query, script path).
        :param dataframes: Dictionary of input dataframes/datasets.
        :return: Transformed dataframe/dataset.
        """
        pass