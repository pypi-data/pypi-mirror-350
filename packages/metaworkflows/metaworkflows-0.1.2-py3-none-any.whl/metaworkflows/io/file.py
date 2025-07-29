import logging
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
from metaworkflows.io.base import BaseReader, BaseWriter
from metaworkflows import PROJECT_ROOT # For resolving relative paths

logger = logging.getLogger(__name__)

# --- Python Engine File I/O ---
class FileReader(BaseReader):
    def read(self, options: Dict[str, Any]) -> pd.DataFrame:
        path_str = options.get("path")
        if not path_str:
            raise ValueError("File path ('path') option is required for FileReader.")
        
        # Resolve path: could be absolute or relative to project root or a base_path from connection
        file_path = Path(path_str)
        if not file_path.is_absolute():
            base_path = Path(self.connection_details.get("base_path", PROJECT_ROOT))
            file_path = base_path / path_str
            logger.debug(f"Resolved relative path to: {file_path}")


        file_format = options.get("format", file_path.suffix[1:]).lower() # Infer from extension if not given
        logger.info(f"Reading file: {file_path} with format: {file_format}")

        if file_format == "csv":
            return pd.read_csv(file_path, **options.get("read_options", {}))
        elif file_format == "json":
            return pd.read_json(file_path, **options.get("read_options", {}))
        elif file_format == "parquet":
            return pd.read_parquet(file_path, **options.get("read_options", {}))
        elif file_format == "excel" or file_format in ["xls", "xlsx"]:
            return pd.read_excel(file_path, **options.get("read_options", {}))
        else:
            raise NotImplementedError(f"File format '{file_format}' not supported by Python FileReader.")

class FileWriter(BaseWriter):
    def write(self, data: pd.DataFrame, options: Dict[str, Any]):
        path_str = options.get("path")
        if not path_str:
            raise ValueError("File path ('path') option is required for FileWriter.")

        file_path = Path(path_str)
        if not file_path.is_absolute():
            base_path = Path(self.connection_details.get("base_path", PROJECT_ROOT))
            file_path = base_path / path_str
            logger.debug(f"Resolved relative path for writing to: {file_path}")

        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_format = options.get("format", file_path.suffix[1:]).lower()
        mode = options.get("mode", "overwrite") # overwrite, append
        logger.info(f"Writing file: {file_path} with format: {file_format}, mode: {mode}")

        # Pandas write mode 'w' for overwrite, 'a' for append.
        pandas_mode = 'w'
        if mode == "append":
            pandas_mode = 'a'
        elif mode == "overwrite":
            pandas_mode = 'w'
        elif mode == "ignore":
            if file_path.exists():
                logger.info(f"File {file_path} already exists and mode is 'ignore'. Skipping write.")
                return
            pandas_mode = 'w'
        elif mode == "errorifexists":
            if file_path.exists():
                raise FileExistsError(f"File {file_path} already exists and mode is 'errorifexists'.")
            pandas_mode = 'w'
        else:
            logger.warning(f"Unsupported write mode '{mode}' for Python FileWriter. Defaulting to 'overwrite'.")
            pandas_mode = 'w'

        write_options = options.get("write_options", {})
        if "index" not in write_options: # Default to not writing pandas index
             write_options["index"] = False


        if file_format == "csv":
            data.to_csv(file_path, mode=pandas_mode, header=(mode == 'w' or not file_path.exists() or file_path.stat().st_size == 0), **write_options)
        elif file_format == "json":
            # Pandas to_json doesn't have a direct append mode like CSV.
            # For append, you'd typically read, concat, and write, or write line-delimited JSON.
            if mode == "append" and not options.get("lines", True): # lines=True for append is easier
                logger.warning("Append mode for non-line-delimited JSON is complex. Consider using lines=true or handle externally.")
            data.to_json(file_path, mode=pandas_mode, **write_options)
        elif file_format == "parquet":
            if mode == "append":
                # Parquet append with pandas is tricky, often better done with pyarrow directly or via Spark.
                # For simplicity, this example might overwrite or error.
                # A more robust append would involve reading existing, concatenating, and writing.
                # Or using pyarrow.parquet.write_to_dataset
                logger.warning("Parquet append with pandas to_parquet is not directly supported like CSV. Mode might not behave as expected. Consider Spark for robust appends.")
            data.to_parquet(file_path, **write_options) # `engine` and `compression` can be in write_options
        elif file_format == "excel":
            # Excel append is also complex. Usually, it means writing to new sheets or overwriting.
            data.to_excel(file_path, **write_options)
        else:
            raise NotImplementedError(f"File format '{file_format}' not supported by Python FileWriter.")


# --- Spark Engine File I/O ---
class SparkFileReader(BaseReader):
    def __init__(self, spark_session: Any, connection_details: Optional[Dict[str, Any]] = None):
        super().__init__(connection_details)
        self.spark = spark_session

    def read(self, options: Dict[str, Any]) -> Any: # Returns Spark DataFrame
        path = options.get("path")
        if not path:
            raise ValueError("'path' option is required for SparkFileReader.")
        
        file_format = options.get("format")
        if not file_format:
            raise ValueError("'format' (e.g., csv, parquet, json, orc, text) option is required for SparkFileReader.")
        
        reader = self.spark.read.format(file_format)
        # Pass through Spark reader options directly
        # e.g., header, inferSchema, sep for CSV; mergeSchema for Parquet
        for k, v in options.items():
            if k not in ["path", "format", "dbtable", "query"]: # Reserved/handled elsewhere
                reader.option(k, v)
        
        logger.info(f"Spark reading {file_format} from: {path} with options {options}")
        return reader.load(path)

class SparkFileWriter(BaseWriter):
    def __init__(self, spark_session: Any, connection_details: Optional[Dict[str, Any]] = None):
        super().__init__(connection_details)
        self.spark = spark_session

    def write(self, data: Any, options: Dict[str, Any]): # data is Spark DataFrame
        path = options.get("path")
        if not path:
            raise ValueError("'path' option is required for SparkFileWriter.")

        file_format = options.get("format")
        if not file_format:
            raise ValueError("'format' option is required for SparkFileWriter.")

        mode = options.get("mode", "overwrite") # overwrite, append, ignore, errorifexists
        partition_by = options.get("partition_by") # list of column names or None

        writer = data.write.format(file_format).mode(mode)

        if partition_by:
            if isinstance(partition_by, list):
                writer = writer.partitionBy(*partition_by)
            else:
                logger.warning("partition_by should be a list of column names.")
        
        # Pass through Spark writer options directly
        # e.g., compression for Parquet/ORC, header for CSV
        for k, v in options.items():
            if k not in ["path", "format", "mode", "partition_by", "dbtable", "query"]:
                writer.option(k, v)

        logger.info(f"Spark writing {file_format} to: {path} in mode {mode} with options {options}")
        writer.save(path)