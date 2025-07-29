import pytest
from pathlib import Path
from metaworkflows.core.job import Job, JobStep

# Assume you have a sample valid job yaml for testing in tests/fixtures/sample_job.yaml
# And an invalid one in tests/fixtures/invalid_job.yaml

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_load_valid_spark_job():
    # Create a dummy spark_job.yaml for testing
    dummy_job_path = FIXTURES_DIR / "dummy_spark_job.yaml"
    dummy_job_content = """
job_name: test_spark_job
description: "A test Spark job."
version: "1.0"
engine:
  type: spark
  config:
    spark.app.name: "TestApp"
steps:
  - step_name: read_data
    type: read
    connector: file
    options:
      path: "input/data.csv"
      format: "csv"
    output_alias: "df_input"
  - step_name: transform_data
    type: transform
    engine_specific:
      spark_sql:
        query: "SELECT * FROM df_input"
    input_aliases: ["df_input"]
    output_alias: "df_transformed"
"""
    with open(dummy_job_path, "w") as f:
        f.write(dummy_job_content)

    job = Job.from_yaml(str(dummy_job_path))
    assert job.job_name == "test_spark_job"
    assert job.get_engine_type() == "spark"
    assert job.engine_config["config"]["spark.app.name"] == "TestApp"
    assert len(job.steps) == 2
    assert isinstance(job.steps[0], JobStep)
    assert job.steps[0].name == "read_data"
    assert job.steps[0].type == "read"
    assert job.steps[0].output_alias == "df_input"
    assert job.steps[1].type == "transform"
    assert job.steps[1].engine_specific["spark_sql"]["query"] == "SELECT * FROM df_input"
    assert job.steps[1].input_aliases == ["df_input"]
    assert job.steps[1].output_alias == "df_transformed"

    dummy_job_path.unlink() # Clean up

def test_load_job_file_not_found():
    with pytest.raises(FileNotFoundError):
        Job.from_yaml("non_existent_job.yaml")

def test_load_job_missing_engine_type():
    dummy_invalid_job_path = FIXTURES_DIR / "invalid_engine_job.yaml"
    dummy_invalid_content = """
job_name: invalid_job
steps: []
engine: {} # Missing type
"""
    with open(dummy_invalid_job_path, "w") as f:
        f.write(dummy_invalid_content)
    
    with pytest.raises(ValueError, match="missing engine type configuration"):
        Job.from_yaml(str(dummy_invalid_job_path))
    dummy_invalid_job_path.unlink()


def test_load_job_missing_step_type():
    dummy_invalid_job_path = FIXTURES_DIR / "invalid_step_job.yaml"
    dummy_invalid_content = """
job_name: invalid_step_job
engine:
  type: python
steps:
  - step_name: broken_step # no type
    output_alias: "out"
"""
    with open(dummy_invalid_job_path, "w") as f:
        f.write(dummy_invalid_content)

    with pytest.raises(ValueError, match="is missing a 'type'"):
        Job.from_yaml(str(dummy_invalid_job_path))
    dummy_invalid_job_path.unlink()

# Create the fixtures directory if it doesn't exist
FIXTURES_DIR.mkdir(exist_ok=True)