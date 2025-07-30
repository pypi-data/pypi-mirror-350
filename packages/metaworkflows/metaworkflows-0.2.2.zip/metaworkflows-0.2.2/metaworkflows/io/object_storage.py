import logging
from typing import Dict, Any
from metaworkflows.io.base import BaseReader, BaseWriter
# For Python direct access (example, you'd pick a library like google-cloud-storage or boto3)

logger = logging.getLogger(__name__)

# --- Python Engine Generic Object Storage (Abstract) ---
class ObjectStorageReader(BaseReader):
    def read(self, options: Dict[str, Any]) -> Any: # pd.DataFrame
        raise NotImplementedError("Generic Python ObjectStorageReader needs specific implementation.")

class ObjectStorageWriter(BaseWriter):
    def write(self, data: Any, options: Dict[str, Any]): # data is pd.DataFrame
        raise NotImplementedError("Generic Python ObjectStorageWriter needs specific implementation.")


# --- Spark Engine Object Storage I/O (Relies on Spark's native capabilities) ---
# Spark usually handles GCS, S3, Azure Blob Storage paths directly if Hadoop/cloud connectors
# are configured in Spark environment (e.g., via spark.jars.packages and fs configurations)
class SparkObjectStorageReader(BaseReader):
    def __init__(self, spark_session: Any, connection_details: Dict[str, Any]):
        super().__init__(connection_details)
        self.spark = spark_session
        # connection_details might contain bucket_name, project_id (for GCS), etc.
        # but often these are part of the path (e.g., "gs://bucket/path") or configured globally in Spark.

    def read(self, options: Dict[str, Any]) -> Any: # Returns Spark DataFrame
        path = options.get("path") # e.g., "gs://my-bucket/data/input.parquet", "s3a://my-bucket/..."
        if not path:
            raise ValueError("'path' option is required for SparkObjectStorageReader (e.g., gs://bucket/file, s3a://bucket/file).")
        
        file_format = options.get("format")
        if not file_format:
            raise ValueError("'format' (e.g., csv, parquet, json) option is required.")
        
        reader = self.spark.read.format(file_format)
        # Pass through Spark reader options
        for k, v in options.items():
            if k not in ["path", "format"]:
                reader.option(k, v)
        
        logger.info(f"Spark reading {file_format} from object storage path: {path} with options {options}")
        # Spark uses Hadoop FileSystem APIs; ensure appropriate connectors are on classpath
        # and auth is configured (e.g., service account for GCS, IAM roles for S3).
        # For GCS, if 'credentials_path' is in connection_details, it might need to be set in Spark conf:
        # self.spark.conf.set("google.cloud.auth.service.account.json.keyfile", self.connection_details["credentials_path"])
        # This should ideally be done during SparkSession initialization based on all connection types.
        return reader.load(path)

class SparkObjectStorageWriter(BaseWriter):
    def __init__(self, spark_session: Any, connection_details: Dict[str, Any]):
        super().__init__(connection_details)
        self.spark = spark_session

    def write(self, data: Any, options: Dict[str, Any]): # data is Spark DataFrame
        path = options.get("path") # e.g., "gs://my-bucket/data/output/", "s3a://my-bucket/output/"
        if not path:
            raise ValueError("'path' option is required for SparkObjectStorageWriter.")

        file_format = options.get("format")
        if not file_format:
            raise ValueError("'format' option is required.")

        mode = options.get("mode", "overwrite")
        partition_by = options.get("partition_by")

        writer = data.write.format(file_format).mode(mode)

        if partition_by:
            if isinstance(partition_by, list):
                writer = writer.partitionBy(*partition_by)
            else:
                logger.warning("partition_by should be a list of column names.")
        
        for k, v in options.items():
            if k not in ["path", "format", "mode", "partition_by"]:
                writer.option(k, v)

        logger.info(f"Spark writing {file_format} to object storage path: {path} in mode {mode} with options {options}")
        writer.save(path)