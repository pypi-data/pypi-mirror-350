import logging
import pandas as pd
from typing import Dict, Any
from io import BytesIO, StringIO
from google.cloud import storage
from google.oauth2 import service_account

from metaworkflows.io.base import BaseReader, BaseWriter

logger = logging.getLogger(__name__)

class GCSObjectReader(BaseReader):
    def _get_client(self) -> storage.Client:
        creds_path = self.connection_details.get("credentials_path")
        project_id = self.connection_details.get("project_id")
        if creds_path:
            credentials = service_account.Credentials.from_service_account_file(creds_path)
            return storage.Client(credentials=credentials, project=project_id or credentials.project_id)
        else: # Try Application Default Credentials
            return storage.Client(project=project_id)


    def read(self, options: Dict[str, Any]) -> pd.DataFrame:
        path_str = options.get("path") # Should be "bucket_name/blob_name.ext" or just "blob_name.ext" if bucket in connection
        if not path_str:
            raise ValueError("GCS path ('path') option is required for GCSObjectReader.")

        bucket_name = self.connection_details.get("bucket_name")
        blob_name = path_str
        if "/" in path_str and not bucket_name: # path_str likely includes bucket
            bucket_name, blob_name = path_str.split('/', 1)
        elif not bucket_name:
             raise ValueError("Bucket name must be provided either in connection_details or in the 'path' option.")


        client = self._get_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        file_format = options.get("format", blob_name.split('.')[-1]).lower()
        logger.info(f"Reading from GCS: gs://{bucket_name}/{blob_name} with format: {file_format}")

        try:
            content = blob.download_as_bytes()
        except Exception as e:
            logger.error(f"Failed to download gs://{bucket_name}/{blob_name}: {e}")
            raise

        if file_format == "csv":
            # Pandas read_csv options can be passed via options.get("read_options", {})
            return pd.read_csv(BytesIO(content), **options.get("read_options", {}))
        elif file_format == "json":
             # For line-delimited JSON, common in data lakes
            if options.get("lines", False):
                return pd.read_json(BytesIO(content), lines=True, **options.get("read_options", {}))
            return pd.read_json(BytesIO(content), **options.get("read_options", {}))
        elif file_format == "parquet":
            return pd.read_parquet(BytesIO(content), **options.get("read_options", {}))
        else:
            raise NotImplementedError(f"File format '{file_format}' not supported by GCSObjectReader for Python engine.")


class GCSObjectWriter(BaseWriter):
    def _get_client(self) -> storage.Client: # Duplicated, refactor
        creds_path = self.connection_details.get("credentials_path")
        project_id = self.connection_details.get("project_id")
        if creds_path:
            credentials = service_account.Credentials.from_service_account_file(creds_path)
            return storage.Client(credentials=credentials, project=project_id or credentials.project_id)
        return storage.Client(project=project_id)

    def write(self, data: pd.DataFrame, options: Dict[str, Any]):
        path_str = options.get("path") # "bucket_name/blob_name.ext" or "blob_name.ext"
        if not path_str:
            raise ValueError("GCS path ('path') option is required for GCSObjectWriter.")

        bucket_name = self.connection_details.get("bucket_name")
        blob_name = path_str
        if "/" in path_str and not bucket_name:
            bucket_name, blob_name = path_str.split('/', 1)
        elif not bucket_name:
             raise ValueError("Bucket name must be provided either in connection_details or in the 'path' option.")

        client = self._get_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name) # blob_name can include prefixes/directories

        file_format = options.get("format", blob_name.split('.')[-1]).lower()
        # Mode (overwrite, append etc.) handling for GCS:
        # GCS blobs are immutable in terms of direct append. "overwrite" is implicit on upload.
        # "append" would mean read, concat, write (complex for large files).
        # "errorifexists" or "ignore" needs a check.
        mode = options.get("mode", "overwrite")

        logger.info(f"Writing to GCS: gs://{bucket_name}/{blob_name} with format: {file_format}, mode: {mode}")

        if mode == "errorifexists" and blob.exists():
            raise FileExistsError(f"Blob gs://{bucket_name}/{blob_name} already exists and mode is 'errorifexists'.")
        if mode == "ignore" and blob.exists():
            logger.info(f"Blob gs://{bucket_name}/{blob_name} already exists and mode is 'ignore'. Skipping write.")
            return

        # Pandas write options
        write_options = options.get("write_options", {})
        if "index" not in write_options: # Default to not writing pandas index
             write_options["index"] = False

        content_type = None
        buffer = None

        if file_format == "csv":
            buffer = StringIO()
            data.to_csv(buffer, **write_options)
            content_type = "text/csv"
        elif file_format == "json":
            buffer = StringIO()
            # For line-delimited JSON
            if options.get("lines", False):
                 data.to_json(buffer, orient="records", lines=True, **write_options)
                 content_type = "application/x-ndjson" # or application/jsonlines
            else:
                data.to_json(buffer, orient="records", **write_options) # Default to list of records
                content_type = "application/json"
        elif file_format == "parquet":
            buffer = BytesIO()
            data.to_parquet(buffer, **write_options)
            content_type = "application/octet-stream" # Or more specific parquet type if known
        else:
            raise NotImplementedError(f"File format '{file_format}' not supported by GCSObjectWriter for Python engine.")

        if buffer:
            try:
                blob.upload_from_string(buffer.getvalue(), content_type=content_type)
                logger.info(f"Successfully uploaded to gs://{bucket_name}/{blob_name}")
            except Exception as e:
                logger.error(f"Failed to upload to gs://{bucket_name}/{blob_name}: {e}")
                raise
            finally:
                buffer.close()