# import pytest
# from pathlib import Path
# import pandas as pd
# from metaworkflows.core.job import Job
# from metaworkflows.core.pipeline import Pipeline

# FIXTURES_DIR = Path(__file__).parent / "fixtures"

# def test_pipeline_execution():
#     # Define paths
#     input_file = FIXTURES_DIR / "input_data.csv"
#     output_file = FIXTURES_DIR / "output_data.csv"
#     pipeline_yaml = FIXTURES_DIR / "test_pipeline.yaml"

#     # Ensure output file does not exist before the test
#     if output_file.exists():
#         output_file.unlink()

#     # Load the job and execute the pipeline
#     job = Job.from_yaml(str(pipeline_yaml))
#     pipeline = Pipeline(job)
#     pipeline.run()

#     # Validate the output
#     assert output_file.exists(), "Output file was not created."

#     # Load the output data and validate its contents
#     df_output = pd.read_csv(output_file)
#     assert "value_doubled" in df_output.columns, "Transformation did not add 'value_doubled' column."
#     assert df_output["value_doubled"].tolist() == [200, 400, 600], "Transformation logic is incorrect."

#     # Clean up
#     output_file.unlink()
