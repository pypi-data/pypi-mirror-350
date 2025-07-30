# Paths
CONFIG_PATH = "config/"
# CONNECTIONS_PATH_DEV = "gs://mb-kdl-dev-code/connections/connections.yaml"
CONNECTIONS_PATH_LIVE = "gs://mb-kdl-prod-code/connections/connections.yaml"


SUPPORTED_ENGINES = ["spark", "python"]
SUPPORTED_STEP_TYPES = ["read", "transform", "write", "script"]
SUPPORTED_CONNECTORS = ["database", "file", "gcp_cloud_storage", "gcs", "aws_s3", "s3"]
SUPPORTED_FILE_FORMATS = ["csv", "parquet", "json", "avro", "orc"]
SUPPORTED_WRITE_MODES = ["overwrite", "append", "ignore"]
