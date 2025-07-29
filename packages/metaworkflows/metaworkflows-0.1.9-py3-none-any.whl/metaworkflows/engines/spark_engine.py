import logging
import subprocess
from typing import Any, Dict, Optional
from pyspark.sql import SparkSession, DataFrame
# from pyspark.sql.utils import AnalysisException

from metaworkflows.engines.base import BaseEngine
# Needs to be created
from metaworkflows.io.database import SparkDatabaseReader, SparkDatabaseWriter
# Needs to be created
from metaworkflows.io.object_storage import SparkObjectStorageReader, SparkObjectStorageWriter
from metaworkflows.io.file import SparkFileReader, SparkFileWriter  # Needs to be created
from metaworkflows.transformers.sql import SparkSQLTransformer
from metaworkflows.core.connections import BaseConnectionManager

logger = logging.getLogger(__name__)


class SparkEngine(BaseEngine):
    def __init__(self, engine_config: Dict[str, Any], connections: BaseConnectionManager):
        super().__init__(engine_config, connections)
        self.spark_session: Optional[SparkSession] = None
        self.sql_transformer = SparkSQLTransformer()
        logger.info("SparkEngine initialized.")

    def initialize(self):
        if self.spark_session:
            logger.warning("SparkSession already initialized.")
            return

        builder = SparkSession.builder
        app_name = self.engine_config.get("spark.app.name", "MetaETLSparkJob")
        builder.appName(app_name)

        # Set Spark configurations
        for key, value in self.engine_config.items():
            if key != "spark.app.name":  # appName is already set
                builder.config(key, value)

        # Example: Add JDBC jar for PostgreSQL if it's listed in packages
        # packages = self.engine_config.get("spark.jars.packages")
        # if packages:
        #    builder.config("spark.jars.packages", packages)

        try:
            self.spark_session = builder.getOrCreate()
            logger.info(
                f"SparkSession initialized/retrieved. AppName: {self.spark_session.conf.get('spark.app.name')}")
            logger.info(f"Spark version: {self.spark_session.version}")
            # You can log other useful Spark context info here, like master URL
            # logger.info(f"Spark Master: {self.spark_session.conf.get('spark.master')}")
        except Exception as e:
            logger.error(
                f"Failed to initialize SparkSession: {e}", exc_info=True)
            raise

    # io_type 'read' or 'write'
    def _get_io_handler(self, connector_type: str, connection_ref: Optional[str], io_type: str):
        conn_details = {}
        if connection_ref:
            conn_details = self.get_connection_details(connection_ref)

        # Determine specific type from connection_ref if connector_type is generic (e.g., "database")
        specific_connector_type = conn_details.get(
            "type", connector_type).lower()

        if specific_connector_type == "file":
            # File reader/writer might not need full connection_details if path is absolute in options
            return SparkFileReader(self.spark_session, conn_details) if io_type == 'read' else SparkFileWriter(self.spark_session, conn_details)
        # Generalize JDBC
        elif specific_connector_type in ["jdbc", "postgresql", "mysql"]:
            return SparkDatabaseReader(self.spark_session, conn_details) if io_type == 'read' else SparkDatabaseWriter(self.spark_session, conn_details)
        # Object storage
        elif specific_connector_type in ["gcp_cloud_storage", "gcs", "aws_s3", "s3"]:
            return SparkObjectStorageReader(self.spark_session, conn_details) if io_type == 'read' else SparkObjectStorageWriter(self.spark_session, conn_details)
        else:
            raise ValueError(
                f"Unsupported connector type '{specific_connector_type}' for SparkEngine.")

    def read(self, connector_type: str, connection_ref: Optional[str], options: Dict[str, Any]) -> DataFrame:
        if not self.spark_session:
            raise RuntimeError(
                "SparkSession is not initialized. Call initialize() first.")
        logger.info(
            f"SparkEngine reading from {connector_type} (ref: {connection_ref}) with options: {options}")

        handler = self._get_io_handler(connector_type, connection_ref, 'read')
        return handler.read(options)

    def transform(self, step_config: Any, dataframes: Dict[str, DataFrame]) -> DataFrame:
        if not self.spark_session:
            raise RuntimeError("SparkSession is not initialized.")

        transform_config = step_config.engine_specific
        if "spark_sql" in transform_config:
            sql_query_config = transform_config["spark_sql"]
            return self.sql_transformer.transform(
                spark=self.spark_session,
                config=sql_query_config,
                dataframes=dataframes
            )
        # Add other transformation types specific to Spark if needed (e.g., calling a PySpark script)
        # elif "pyspark_script" in transform_config:
        #    script_path = transform_config["pyspark_script"]["path"]
        #    # Logic to execute a PySpark script, potentially passing dataframes
        #    raise NotImplementedError("PySpark script transformation not yet implemented.")
        else:
            raise ValueError(
                "Unsupported Spark transformation type in engine_specific config.")
    def write(self, dataframe: DataFrame, connector_type: str, connection_ref: Optional[str], options: Dict[str, Any]):
        if not self.spark_session:
            raise RuntimeError(
                "SparkSession is not initialized. Call initialize() first.")
        logger.info(
            f"SparkEngine writing to {connector_type} (ref: {connection_ref}) with options: {options}")

        handler = self._get_io_handler(connector_type, connection_ref, 'write')
        handler.write(dataframe, options)

    def custom_script(self, step_config: Any):
        # if not self.spark_session:
        #     raise RuntimeError("SparkSession is not initialized.")

        transform_config = step_config.options
        # print(vars(transform_config))
        if "command" in transform_config:
            script = transform_config["command"]
            logger.info(f"Executing bash command: {script}")
            result = subprocess.run(
                script, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"Command succeeded: {result.stdout.strip()}")
            else:
                logger.error(
                    f"Command failed with error: {result.stderr.strip()}")
            return
        # Add other transformation types specific to Spark if needed (e.g., calling a PySpark script)
        # elif "pyspark_script" in transform_config:
        #    script_path = transform_config["pyspark_script"]["path"]
        #    # Logic to execute a PySpark script, potentially passing dataframes
        #    raise NotImplementedError("PySpark script transformation not yet implemented.")
        else:
            raise ValueError(
                "Unsupported Spark transformation type in engine_specific config.")

    def cleanup(self):
        if self.spark_session:
            try:
                # Unpersist cached RDDs/DataFrames if any were explicitly cached by jobs
                # This is more of an advanced feature; typically Spark manages this.
                # For temp views, they are session-scoped.
                # Clearing catalog cache might be an option too.
                # self.spark_session.catalog.clearCache()

                # Stop the SparkSession
                self.spark_session.stop()
                logger.info("SparkSession stopped.")
            except Exception as e:
                logger.error(
                    f"Error stopping SparkSession: {e}", exc_info=True)
            finally:
                self.spark_session = None
        else:
            logger.info("SparkEngine cleanup: No active SparkSession to stop.")
