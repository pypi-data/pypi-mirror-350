# import pytest
from metaworkflows.engines.python_engine import PythonEngine
from metaworkflows.engines.spark_engine import SparkEngine

def test_python_engine_initialization():
    engine = PythonEngine(engine_config={}, connections={})
    assert engine is not None, "PythonEngine should initialize successfully."

def test_spark_engine_initialization():
    engine = SparkEngine(engine_config={"spark.app.name": "TestApp"}, connections={})
    assert engine is not None, "SparkEngine should initialize successfully."