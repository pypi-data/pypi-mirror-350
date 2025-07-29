import logging
from typing import Dict, Any
from metaworkflows.io.base import BaseReader, BaseWriter
# For Python direct DB access (example for SQLAlchemy, you'd pick a library)
# import sqlalchemy

logger = logging.getLogger(__name__)

# --- Python Engine Generic Database (Illustrative - Requires specific driver implementations) ---


# This would be an abstract class for Python DB readers
class DatabaseReader(BaseReader):
    def read(self, options: Dict[str, Any]) -> Any:  # pd.DataFrame
        # Typically, you'd use connection_details to establish a connection
        # and 'options' for query/table.
        # Example:
        # engine = sqlalchemy.create_engine(self.connection_details['url'])
        # query_or_table = options.get("query") or options.get("dbtable")
        # return pd.read_sql(query_or_table, engine)
        raise NotImplementedError(
            "Generic Python DatabaseReader needs specific implementation.")


class DatabaseWriter(BaseWriter):  # Abstract for Python DB writers
    # data is pd.DataFrame
    def write(self, data: Any, options: Dict[str, Any]):
        # Example:
        # table_name = options.get("dbtable")
        # mode = options.get("mode", "fail") # fail, replace, append
        # engine = sqlalchemy.create_engine(self.connection_details['url'])
        # data.to_sql(table_name, engine, if_exists=mode, index=False)
        raise NotImplementedError(
            "Generic Python DatabaseWriter needs specific implementation.")


# --- Spark Engine Database I/O (using JDBC) ---
class SparkDatabaseReader(BaseReader):
    def __init__(self, spark_session: Any, connection_details: Dict[str, Any]):
        super().__init__(connection_details)
        self.spark = spark_session
        if not self.connection_details:
            raise ValueError(
                "Connection details are required for SparkDatabaseReader.")

    def read(self, options: Dict[str, Any]) -> Any:  # Returns Spark DataFrame
        reader = self.spark.read.format("jdbc")

        # Standard JDBC options from connection_details
        # Construct URL if not directly provided
        reader.option("url", self.connection_details.get("url"))
        reader.option("driver", self.connection_details.get(
            "driver"))  # e.g., org.postgresql.Driver
        reader.option("user", self.connection_details.get("user"))
        reader.option("password", self.connection_details.get("password"))

        if "dbtable" in options:  # Reading a whole table
            reader.option("dbtable", options["dbtable"])
        elif "query" in options:  # Reading using a query
            reader.option("query", options["query"])
        else:
            raise ValueError(
                "Either 'dbtable' or 'query' must be specified in options for Spark JDBC read.")

        # Allow overriding or adding more JDBC options from the step's 'options'
        for k, v in options.items():
            if k not in ["dbtable", "query"]:  # Already handled
                if k in ["user", "password", "url", "driver"] and k in self.connection_details:
                    logger.debug(
                        f"JDBC option '{k}' from step options overrides connection_details.")
                reader.option(k, v)

        # Add specific connection properties like schema for postgres
        if self.connection_details.get("schema"):
            reader.option("customSchema", self.connection_details.get(
                "schema"))  # For some drivers
            # Or it might be part of dbtable: schema.table

        print(vars(reader))
        logger.info(f"Spark reading from JDBC source: {self.connection_details.get('url')} "
                    f"(table/query: {options.get('dbtable') or options.get('query')[:50]+'...'}), options: {options}")
        return reader.load()


class SparkDatabaseWriter(BaseWriter):
    def __init__(self, spark_session: Any, connection_details: Dict[str, Any]):
        super().__init__(connection_details)
        self.spark = spark_session
        if not self.connection_details:
            raise ValueError(
                "Connection details are required for SparkDatabaseWriter.")

    # data is Spark DataFrame
    def write(self, data: Any, options: Dict[str, Any]):
        table_name = options.get("dbtable")
        if not table_name:
            raise ValueError(
                "'dbtable' option (target table name) is required for Spark JDBC write.")

        # errorifexists, append, overwrite, ignore
        mode = options.get("mode", "errorifexists")

        writer = data.write.format("jdbc")
        writer.option("url", self.connection_details.get("url"))
        writer.option("driver", self.connection_details.get("driver"))
        writer.option("dbtable", table_name)
        writer.option("user", self.connection_details.get("user"))
        writer.option("password", self.connection_details.get("password"))

        # Allow overriding or adding more JDBC options
        for k, v in options.items():
            if k not in ["dbtable", "mode"]:  # Already handled
                if k in ["user", "password", "url", "driver"] and k in self.connection_details:
                    logger.debug(
                        f"JDBC option '{k}' from step options overrides connection_details.")
                writer.option(k, v)

        # Add specific connection properties like schema for postgres
        if self.connection_details.get("schema"):
            writer.option("customSchema",
                          self.connection_details.get("schema"))

        logger.info(
            f"Spark writing to JDBC table: {table_name} at {self.connection_details.get('url')}, mode: {mode}, options: {options}")
        writer.mode(mode).save()
