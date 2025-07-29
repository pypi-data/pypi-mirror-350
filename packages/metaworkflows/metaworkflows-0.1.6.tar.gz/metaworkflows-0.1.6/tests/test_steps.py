# import pytest
# from pathlib import Path
# from unittest.mock import MagicMock, patch
# from metaworkflows.core.pipeline import Pipeline
# from metaworkflows.core.job import Job

# FIXTURES_DIR = Path(__file__).parent / "fixtures"

# @pytest.fixture
# def mock_job_yaml():
#     """Fixture to provide a mock job YAML for testing."""
#     return """
# job_name: test_pipeline_steps
# description: "Test pipeline with all steps."
# version: "1.0"

# engine:
#   type: python
#   config: {}

# steps:
#   - step_name: read_test_data
#     type: read
#     connector: file
#     options:
#       path: "tests/fixtures/input_data.csv"
#       format: "csv"
#     output_alias: "df_input"

#   - step_name: transform_test_data
#     type: transform
#     engine_specific:
#       python:
#         module: "tests.fixtures.transformations"
#         function: "transform_data"
#     input_aliases: ["df_input"]
#     output_alias: "df_transformed"

#   - step_name: write_test_data
#     type: write
#     connector: file
#     input_alias: "df_transformed"
#     options:
#       path: "tests/fixtures/output_data.csv"
#       format: "csv"
#       mode: "overwrite"
# """

# @pytest.fixture
# def mock_job_file(mock_job_yaml, tmp_path):
#     """Fixture to create a temporary job YAML file."""
#     job_file = tmp_path / "mock_job.yaml"
#     job_file.write_text(mock_job_yaml)
#     return job_file

# @patch("metaworkflows.core.pipeline.Pipeline._execute_step")
# @patch("metaworkflows.core.pipeline.Pipeline.engine")
# def test_pipeline_steps(mock_engine, mock_execute_step, mock_job_file):
#     """
#     Test the pipeline execution for all steps (read, transform, write).
#     """
#     # Mock the engine's read, transform, and write methods
#     mock_engine.read.return_value = "mock_dataframe"
#     mock_engine.transform.return_value = "transformed_dataframe"
#     mock_engine.write.return_value = None

#     # Load the job and execute the pipeline
#     job = Job.from_yaml(str(mock_job_file))
#     pipeline = Pipeline(job)
#     pipeline.run()

#     # Validate that all steps were executed
#     assert mock_execute_step.call_count == len(job.steps), "Not all steps were executed."

#     # Validate the engine's methods were called with correct arguments
#     mock_engine.read.assert_called_once_with(
#         connector_type="file",
#         connection_ref=None,
#         options={"path": "tests/fixtures/input_data.csv", "format": "csv"}
#     )
#     mock_engine.transform.assert_called_once_with(
#         step_config=job.steps[1],
#         dataframes={"df_input": "mock_dataframe"}
#     )
#     mock_engine.write.assert_called_once_with(
#         dataframe="transformed_dataframe",
#         connector_type="file",
#         connection_ref=None,
#         options={"path": "tests/fixtures/output_data.csv", "format": "csv", "mode": "overwrite"}
#     )