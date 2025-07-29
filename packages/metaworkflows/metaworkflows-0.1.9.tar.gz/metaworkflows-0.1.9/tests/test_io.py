# import pytest
# from metaworkflows.io.file import FileReader, FileWriter
# from pathlib import Path
# import pandas as pd

# def test_file_reader():
#     test_file = Path("tests/fixtures/test.csv")
#     test_file.write_text("col1,col2\n1,2\n3,4")
#     reader = FileReader()
#     df = reader.read({"path": str(test_file), "format": "csv"})
#     assert isinstance(df, pd.DataFrame), "FileReader should return a DataFrame."
#     assert len(df) == 2, "DataFrame should have 2 rows."
#     test_file.unlink()

# def test_file_writer():
#     test_file = Path("tests/fixtures/output.csv")
#     writer = FileWriter()
#     df = pd.DataFrame({"col1": [1, 3], "col2": [2, 4]})
#     writer.write(df, {"path": str(test_file), "format": "csv"})
#     assert test_file.exists(), "FileWriter should create the output file."
#     test_file.unlink()