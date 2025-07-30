import logging
from typing import Any, Dict
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.utils import AnalysisException

from metaworkflows.transformers.base import BaseTransformer

logger = logging.getLogger(__name__)

class SparkSQLTransformer(BaseTransformer):
    def transform(self, spark: SparkSession, config: Dict[str, Any], dataframes: Dict[str, DataFrame]) -> DataFrame:
        """
        Transforms data using Spark SQL.
        :param spark: The SparkSession.
        :param config: Dictionary containing 'query' and optionally 'temp_views'.
                      'temp_views' is a list of dicts, each with 'alias' and 'dataframe' (key from dataframes dict).
        :param dataframes: A dictionary of input Spark DataFrames.
        :return: A Spark DataFrame result of the SQL query.
        """
        if not spark:
            raise ValueError("SparkSession must be provided for SparkSQLTransformer.")
        
        query = config.get("query")
        if not query:
            raise ValueError("SQL 'query' not specified in transformation config.")

        temp_views_config = config.get("temp_views", [])

        # Register temporary views
        registered_views = []
        for view_conf in temp_views_config:
            alias = view_conf.get("alias")
            df_key = view_conf.get("dataframe") # This is the key from the input `dataframes` dict
            if not alias or not df_key:
                logger.error("Temp view config missing 'alias' or 'dataframe' key.")
                continue
            if df_key not in dataframes:
                logger.error(f"DataFrame key '{df_key}' for temp view '{alias}' not found in input dataframes.")
                raise ValueError(f"DataFrame key '{df_key}' for temp view '{alias}' not found.")
            
            try:
                dataframes[df_key].createOrReplaceTempView(alias)
                registered_views.append(alias)
                logger.info(f"Registered DataFrame '{df_key}' as temporary view '{alias}'.")
            except Exception as e:
                logger.error(f"Error registering temp view '{alias}' for DataFrame '{df_key}': {e}")
                raise

        logger.info(f"Executing Spark SQL query: {query[:200]}...")
        try:
            result_df = spark.sql(query)
        except AnalysisException as e:
            logger.error(f"Spark SQL AnalysisException: {e}\nQuery: {query}")
            raise
        except Exception as e:
            logger.error(f"Error executing Spark SQL query: {e}\nQuery: {query}")
            raise
        finally:
            # Clean up temporary views if desired, though they are session-scoped
            # for view_alias in registered_views:
            #     try:
            #         spark.catalog.dropTempView(view_alias)
            #         logger.debug(f"Dropped temporary view: {view_alias}")
            #     except Exception as e:
            #         logger.warning(f"Could not drop temp view {view_alias}: {e}")
            pass

        return result_df