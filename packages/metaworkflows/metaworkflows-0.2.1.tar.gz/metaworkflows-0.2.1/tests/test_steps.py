import pytest
from pyspark.sql import SparkSession
from metaworkflows.core.job import Job
from metaworkflows.core.pipeline import Pipeline


@pytest.fixture(scope="session")
def spark():
    """Create a SparkSession for testing."""
    spark = SparkSession.builder \
        .appName("TestSparkPipeline") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "1") \
        .getOrCreate()
    
    yield spark
    

def test_full_pipeline(spark, tmp_path):
    """Test a complete pipeline with read, transform and write steps."""
    # Create sample data
    input_data = [("Alice", 100), ("Bob", 200), ("Charlie", 300)]
    input_df = spark.createDataFrame(input_data, ["name", "value"])
    input_path = str(tmp_path / "input.parquet")
    output_path = str(tmp_path / "output.parquet")
    input_df.write.parquet(input_path)

    # Create job config
    job_yaml = f"""
job_name: test_full_pipeline
engine:
  type: spark
  config:
    spark.app.name: "TestFullPipeline"
steps:
  - step_name: read_data
    type: read
    connector: file
    options:
      path: {input_path}
      format: parquet
    output_alias: df_input

  - step_name: transform_data
    type: transform
    engine_specific:
      spark_sql:
        temp_views:
          - alias: source_view
            dataframe: df_input
        query: |
          SELECT 
            name,
            value,
            value * 2 as doubled_value
          FROM source_view
    input_aliases: ["df_input"]
    output_alias: df_transformed

  - step_name: write_data
    type: write
    connector: file
    options:
      path: {output_path}
      format: parquet
      mode: overwrite
    input_alias: df_transformed
"""
    job_file = tmp_path / "job.yaml"
    job_file.write_text(job_yaml)

    # Run pipeline
    job = Job.from_yaml(str(job_file))
    pipeline = Pipeline(job)
    pipeline.engine.spark_session = spark
    pipeline.run()

    # Reinitialize Spark session after pipeline.run()
    spark = SparkSession.builder \
        .appName("TestSparkPipeline") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "1") \
        .getOrCreate()

    # Verify final output
    df_output = spark.read.parquet(output_path)
    assert df_output.count() == 3
    assert set(df_output.columns) == {"name", "value", "doubled_value"}
    
    total_doubled_value = df_output.groupBy().sum("doubled_value").collect()[0][0]
    assert total_doubled_value == 1200