import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("pytest-pyspark") \
        .getOrCreate()
    yield spark
    spark.stop()

def test_simple_transformation(spark):
    # Create a sample DataFrame
    data = [("Alice", 1), ("Bob", 2)]
    df = spark.createDataFrame(data, ["name", "id"])

    # Transformation: add 1 to 'id'
    df2 = df.withColumn("id_plus_one", col("id") + 1)

    result = df2.collect()
    assert result[0]["id_plus_one"] == 2
    assert result[1]["id_plus_one"] == 3