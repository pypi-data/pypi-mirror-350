import logging
from typing import Dict, Any
from metaworkflows.core.job import Job, JobStep
from metaworkflows.engines.base import BaseEngine
from metaworkflows.engines.python_engine import PythonEngine
from metaworkflows.engines.spark_engine import SparkEngine
# Import other engines here
# from metaworkflows.engines.flink_engine import FlinkEngine

from metaworkflows import CONNECTION_MANAGER  # Import global connections

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, job: Job):
        self.job = job
        self.engine: BaseEngine = self._initialize_engine()
        # To store intermediate data (e.g., Spark DataFrames, Pandas DataFrames)
        self.dataframes: Dict[str, Any] = {}

    def _initialize_engine(self) -> BaseEngine:
        engine_type = self.job.get_engine_type()
        engine_config = self.job.engine_config.get("config", {})
        logger.info(
            f"Initializing engine: {engine_type} for job '{self.job.job_name}'")

        if engine_type == "python":
            return PythonEngine(engine_config, CONNECTION_MANAGER)
        elif engine_type == "spark":
            return SparkEngine(engine_config, CONNECTION_MANAGER)
        # elif engine_type == "flink":
        #     return FlinkEngine(engine_config, CONNECTIONS)
        else:
            msg = f"Unsupported engine type: {engine_type}"
            logger.error(msg)
            raise ValueError(msg)

    def _execute_step(self, step: JobStep):
        logger.info(f"Executing step: {step.name} (Type: {step.type})")
        try:
            if step.type == "read":
                if not step.output_alias:
                    raise ValueError(
                        f"Read step '{step.name}' is missing 'output_alias'.")
                df = self.engine.read(
                    connector_type=step.connector,
                    connection_ref=step.connection_ref,
                    options=step.options,
                )
                self.dataframes[step.output_alias] = df
                logger.info(
                    f"Read step '{step.name}' completed. Output alias: {step.output_alias}")

            elif step.type == "transform":
                input_dfs = {alias: self.dataframes[alias]
                             for alias in step.input_aliases if alias in self.dataframes}
                if len(input_dfs) != len(step.input_aliases):
                    missing = set(step.input_aliases) - set(input_dfs.keys())
                    raise ValueError(
                        f"Transform step '{step.name}' missing input dataframes: {missing}")

                if not step.output_alias:
                    raise ValueError(
                        f"Transform step '{step.name}' is missing 'output_alias'.")

                transformed_df = self.engine.transform(
                    step_config=step,  # Pass the whole step for engine-specific logic
                    dataframes=input_dfs
                )
                self.dataframes[step.output_alias] = transformed_df
                logger.info(
                    f"Transform step '{step.name}' completed. Output alias: {step.output_alias}")

            elif step.type == "write":
                if not step.input_alias or step.input_alias not in self.dataframes:
                    raise ValueError(
                        f"Write step '{step.name}' missing or has invalid 'input_alias': {step.input_alias}")
                df_to_write = self.dataframes[step.input_alias]
                self.engine.write(
                    dataframe=df_to_write,
                    connector_type=step.connector,
                    connection_ref=step.connection_ref,
                    options=step.options,
                )
                logger.info(
                    f"Write step '{step.name}' completed for input alias: {step.input_alias}")
                
            elif step.type == "script":
                self.engine.custom_script(
                    step_config=step  # Pass the whole step for engine-specific logic
                )
                logger.info(
                    f"Script step '{step.name}' completed.")
            else:
                logger.warning(
                    f"Unsupported step type: {step.type} for step {step.name}")

        except Exception as e:
            logger.error(
                f"Error executing step '{step.name}': {e}", exc_info=True)
            raise  # Re-raise the exception to stop the pipeline

    def run(self):
        logger.info(
            f"Starting pipeline execution for job: {self.job.job_name}")
        try:
            self.engine.initialize()  # Initialize engine session (e.g., SparkSession)
            for step in self.job.steps:
                self._execute_step(step)
            logger.info(
                f"Pipeline for job '{self.job.job_name}' completed successfully.")
        except Exception as e:
            logger.error(
                f"Pipeline execution failed for job '{self.job.job_name}': {e}", exc_info=True)
            raise
            # Perform any cleanup if necessary
        finally:
            self.engine.cleanup()  # Cleanup engine resources
            logger.info(
                f"Engine cleanup for job '{self.job.job_name}' finished.")
