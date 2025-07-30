import logging
from typing import Any, Dict, Optional
import pandas as pd
import importlib

from metaworkflows.engines.base import BaseEngine
from metaworkflows.io.file import FileReader, FileWriter # Assuming you have these
# from metaworkflows.io.database import DatabaseReader, DatabaseWriter # For Python direct DB access
# from metaworkflows.io.object_storage import ObjectStorageReader, ObjectStorageWriter
from metaworkflows.core.connections import BaseConnectionManager

logger = logging.getLogger(__name__)

class PythonEngine(BaseEngine):
    def __init__(self, engine_config: Dict[str, Any], connections: BaseConnectionManager):
        super().__init__(engine_config, connections)
        # No specific session for basic Python engine, but could be for things like Dask
        self.session = None
        logger.info("PythonEngine initialized.")

    def initialize(self):
        logger.info("PythonEngine session (no-op) initialized.")
        pass # No specific session to start for basic Python

    def _get_io_handler(self, connector_type: str, io_type: str): # io_type is 'read' or 'write'
        # This is a simplified factory. You'd expand this with more I/O handlers.
        # It might be better to move this factory logic to a dedicated io_factory.py
        connection_details = {} # Will be filled by the read/write methods
        if connector_type == "file":
            return FileReader(connection_details) if io_type == 'read' else FileWriter(connection_details)
        # Add more connectors like:
        # elif connector_type == "postgresql":
        #     from metaworkflows.io.postgres_database import PostgreSQLReader, PostgreSQLWriter # Example
        #     return PostgreSQLReader(connection_details) if io_type == 'read' else PostgreSQLWriter(connection_details)
        # elif connector_type == "gcp_cloud_storage":
        #     from metaworkflows.io.gcp_object_storage import GCSObjectReader, GCSObjectWriter # Example
        #     return GCSObjectReader(connection_details) if io_type == 'read' else GCSObjectWriter(connection_details)
        else:
            raise ValueError(f"Unsupported connector type '{connector_type}' for PythonEngine.")

    def read(self, connector_type: str, connection_ref: Optional[str], options: Dict[str, Any]) -> pd.DataFrame:
        logger.info(f"PythonEngine reading from {connector_type} with options: {options}")
        conn_details = {}
        if connection_ref:
            conn_details = self.get_connection_details(connection_ref)
        
        # Use a more sophisticated I/O handler resolution mechanism
        if connector_type == "file":
            reader = FileReader(conn_details) # conn_details might contain base_path
            return reader.read(options)
        # elif connector_type == "database" and conn_details.get('type') == "postgresql":
        #    from metaworkflows.io.postgres_database import PostgreSQLReader
        #    reader = PostgreSQLReader(conn_details)
        #    return reader.read(options) # options would contain query or table
        else:
            # For simplicity, direct pandas usage for some common cases if no specific handler
            if connector_type == "file" and options.get("format") == "csv":
                return pd.read_csv(options["path"])
            elif connector_type == "file" and options.get("format") == "json":
                return pd.read_json(options["path"], lines=options.get("lines", False))
            elif connector_type == "file" and options.get("format") == "parquet":
                return pd.read_parquet(options["path"])
            # Add more direct pandas readers or integrate with your IO classes
            else:
                raise NotImplementedError(f"PythonEngine read for {connector_type} with format {options.get('format')} not implemented yet.")

    def transform(self, step_config: Any, dataframes: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        transform_config = step_config.engine_specific.get("python", {})
        logger.info(f"PythonEngine transforming data with config: {transform_config}")

        module_name = transform_config.get("module")
        function_name = transform_config.get("function")
        script_content = transform_config.get("script")
        # params = transform_config.get("params", {}) # Parameters for the function

        if module_name and function_name:
            try:
                module = importlib.import_module(module_name)
                transform_func = getattr(module, function_name)
                # Assuming the function takes the dictionary of dataframes as first arg,
                # or specific dataframes if input_aliases are well-defined.
                # For simplicity, let's assume it takes the first input dataframe if only one,
                # or the dict of dataframes.
                if len(step_config.input_aliases) == 1:
                    input_df_name = step_config.input_aliases[0]
                    result_df = transform_func(dataframes[input_df_name]) # , **params if params else {})
                else:
                    result_df = transform_func(dataframes) # , **params if params else {})
                return result_df
            except Exception as e:
                logger.error(f"Error executing Python transform function {module_name}.{function_name}: {e}")
                raise
        elif script_content:
            # Executing arbitrary script content is a security risk and generally not recommended.
            # If used, it should be carefully sandboxed or used only in trusted environments.
            # This is a very basic example:
            local_vars = {"dataframes": dataframes, "pd": pd}
            exec(script_content, {}, local_vars) # Global dict is empty, local_vars for script context
            if "output_data" not in local_vars:
                raise ValueError("Python script transform did not produce 'output_data' variable.")
            return local_vars["output_data"]
        else:
            raise ValueError("Python transform configuration is missing 'module'/'function' or 'script'.")


    def write(self, dataframe: pd.DataFrame, connector_type: str, connection_ref: Optional[str], options: Dict[str, Any]):
        logger.info(f"PythonEngine writing to {connector_type} with options: {options}")
        conn_details = {}
        if connection_ref:
            conn_details = self.get_connection_details(connection_ref)

        if connector_type == "file":
            writer = FileWriter(conn_details)
            writer.write(dataframe, options)
        # elif connector_type == "database" and conn_details.get('type') == "postgresql":
        #     from metaworkflows.io.postgres_database import PostgreSQLWriter
        #     writer = PostgreSQLWriter(conn_details)
        #     writer.write(dataframe, options) # options would contain table name, mode
        else:
            # Direct pandas for common cases
            if connector_type == "file" and options.get("format") == "csv":
                dataframe.to_csv(options["path"], index=options.get("index", False), mode=options.get("mode", "w")[0]) # mode 'w' or 'a'
            elif connector_type == "file" and options.get("format") == "json":
                dataframe.to_json(options["path"], orient=options.get("orient", "records"), lines=options.get("lines", False))
            elif connector_type == "file" and options.get("format") == "parquet":
                dataframe.to_parquet(options["path"], index=options.get("index", False))
            else:
                raise NotImplementedError(f"PythonEngine write for {connector_type} with format {options.get('format')} not implemented yet.")
    
    def custom_script(self, step_config: Any):
        pass
    
    def cleanup(self):
        logger.info("PythonEngine session cleanup (no-op).")
        self.session = None # In case it was used for something