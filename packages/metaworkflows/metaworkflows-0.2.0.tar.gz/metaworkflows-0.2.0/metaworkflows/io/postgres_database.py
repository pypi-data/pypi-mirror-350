import logging
import pandas as pd
from typing import Dict, Any
import psycopg2 # Or use SQLAlchemy for broader compatibility
# from psycopg2.extras import DictCursor

from metaworkflows.io.base import BaseReader, BaseWriter

logger = logging.getLogger(__name__)

class PostgreSQLReader(BaseReader):
    def _get_conn(self):
        # Ensure password is a string, handle None if not provided and let psycopg2 raise error or handle defaults
        password = self.connection_details.get("password")
        if password is None: # psycopg2 expects string or None; if empty string from env, it's fine
             logger.debug("Password not provided directly, relying on other auth methods or psycopg2 defaults if any.")

        conn_params = {
            "host": self.connection_details.get("host"),
            "port": self.connection_details.get("port", 5432),
            "dbname": self.connection_details.get("database"),
            "user": self.connection_details.get("user"),
            "password": password
        }
        # Filter out None values to let psycopg2 use defaults if applicable
        conn_params = {k: v for k, v in conn_params.items() if v is not None}

        conn = psycopg2.connect(**conn_params)
        if self.connection_details.get("schema"):
            with conn.cursor() as cur:
                cur.execute(f"SET search_path TO {self.connection_details.get('schema')};") # Ensure schema is quoted if needed
            conn.commit() # Commit schema change for the session
        return conn

    def read(self, options: Dict[str, Any]) -> pd.DataFrame:
        query = options.get("query")
        table_name = options.get("dbtable")

        if not query and not table_name:
            raise ValueError("Either 'query' or 'dbtable' must be specified for PostgreSQLReader.")
        
        if query and table_name:
            logger.warning("Both 'query' and 'dbtable' specified; 'query' will be used.")
        
        sql_to_execute = query
        if not sql_to_execute:
            # Basic select all from table, can be expanded with where_clause, columns, etc.
            where_clause = options.get("where_clause")
            select_columns = options.get("select_columns", "*") # comma-separated string or list
            if isinstance(select_columns, list):
                select_columns = ", ".join(select_columns)

            sql_to_execute = f"SELECT {select_columns} FROM {table_name}"
            if where_clause:
                sql_to_execute += f" WHERE {where_clause}"
        
        logger.info(f"Reading from PostgreSQL: {sql_to_execute[:100]}...")
        conn = None
        try:
            conn = self._get_conn()
            # Using pandas.read_sql for simplicity, it handles cursor and data loading.
            # For very large datasets, consider chunking or server-side cursors.
            df = pd.read_sql_query(sql_to_execute, conn)
            return df
        except Exception as e:
            logger.error(f"Error reading from PostgreSQL: {e}", exc_info=True)
            raise
        finally:
            if conn:
                conn.close()

class PostgreSQLWriter(BaseWriter):
    def _get_conn(self): # Duplicated from Reader, could be refactored to a common utility
        password = self.connection_details.get("password")
        conn_params = {
            "host": self.connection_details.get("host"),
            "port": self.connection_details.get("port", 5432),
            "dbname": self.connection_details.get("database"),
            "user": self.connection_details.get("user"),
            "password": password
        }
        conn_params = {k: v for k, v in conn_params.items() if v is not None}
        conn = psycopg2.connect(**conn_params)
        if self.connection_details.get("schema"):
            with conn.cursor() as cur:
                cur.execute(f"SET search_path TO {self.connection_details.get('schema')};")
            conn.commit()
        return conn

    def write(self, data: pd.DataFrame, options: Dict[str, Any]):
        table_name = options.get("dbtable")
        if not table_name:
            raise ValueError("'dbtable' (target table name) is required for PostgreSQLWriter.")

        mode = options.get("mode", "fail")  # fail, replace, append (pandas if_exists values)
        # chunksize = options.get("chunksize", 1000) # For writing in chunks

        logger.info(f"Writing {len(data)} rows to PostgreSQL table: {table_name}, mode: {mode}")
        conn = None
        try:
            # For pandas to_sql, it's better to use SQLAlchemy engine for broader compatibility
            # and handling of data types. However, for a direct psycopg2 approach:
            from io import StringIO
            conn = self._get_conn()
            cursor = conn.cursor()

            if mode == "replace":
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};") # Simple drop, be cautious
                # Recreate table (This is very basic, ideally use DataFrame schema to define columns and types)
                # For a robust solution, use SQLAlchemy or inspect df.dtypes to generate CREATE TABLE
                cols = [f'"{col}" TEXT' for col in data.columns] # Default to TEXT, not robust
                create_table_sql = f"CREATE TABLE {table_name} ({', '.join(cols)});"
                cursor.execute(create_table_sql)
                logger.info(f"Table {table_name} replaced (dropped and recreated).")

            elif mode == "append":
                pass # Data will be appended
            elif mode == "fail":
                cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name.split('.')[-1]}' AND table_schema = '{table_name.split('.')[0] if '.' in table_name else self.connection_details.get('schema', 'public')}');")
                if cursor.fetchone()[0]:
                    raise Exception(f"Table {table_name} already exists and mode is 'fail'.")
            else:
                raise ValueError(f"Unsupported mode '{mode}' for PostgreSQLWriter.")

            # Using COPY FROM STDIN for efficient bulk insert with psycopg2
            # Prepare data as CSV in memory
            sio = StringIO()
            data.to_csv(sio, index=False, header=False, sep='\t', na_rep='\\N') # Use tab as sep, handle NULLs
            sio.seek(0)

            # Create a list of column names suitable for the COPY statement
            columns_for_copy = f"({', '.join([f'\"{col}\"' for col in data.columns])})"

            cursor.copy_expert(sql=f"COPY {table_name} {columns_for_copy} FROM STDIN WITH CSV HEADER DELIMITER AS E'\\t' NULL AS '\\N'", file=sio)
            conn.commit()
            logger.info(f"Successfully wrote {len(data)} rows to {table_name} using COPY.")

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error writing to PostgreSQL: {e}", exc_info=True)
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()