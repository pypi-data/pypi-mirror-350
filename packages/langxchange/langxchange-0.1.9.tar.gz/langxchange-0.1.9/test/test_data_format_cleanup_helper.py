# import os
# import pandas as pd
# import pytest
# from pathlib import Path

# from langxchange.data_format_cleanup_helper import DataFormatCleanupHelper

# class DummyLLM:
#     """Mocks the LLM.chat(...) to always return the same cleaning function."""
#     def chat(self, messages, temperature, max_tokens):
#         # A minimal cleaning function:
#         return """
# def generate_format_clean_data(df):
#     # normalize names
#     df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
#     # trim strings
#     for col in df.select_dtypes(include="object"):
#         df[col] = df[col].str.strip()
#     # convert "NAN" and empty to actual NaN
#     df = df.replace({"NAN": None, "": None})
#     # drop missing
#     df = df.dropna().reset_index(drop=True)
#     return df
# """

# @pytest.fixture(autouse=True)
# def ensure_examples_dir(tmp_path, monkeypatch):
#     # Override examples path to a tmp directory for isolation
#     examples = tmp_path / "examples"
#     examples.mkdir()
#     monkeypatch.chdir(tmp_path)  # work in tmp_path as cwd
#     return examples

# def test_clean_from_samplefile(ensure_examples_dir):
#     examples = ensure_examples_dir

#     # 1) Create a sample CSV in examples/samplefile.txt
#     sample_file = examples / "samplefile.txt"
#     sample_file.write_text(
#         "Name, Signup Date, Score\n"
#         " Alice ,2021-01-05,100\n"
#         "Bob,not a date,NAN\n"
#         "Carol , ,90\n"
#     )

#     # 2) Load into DataFrame
#     df = pd.read_csv(sample_file)

#     # 3) Clean using our helper with DummyLLM
#     helper = DataFormatCleanupHelper(llm_helper=DummyLLM())
#     cleaned = helper.clean(df)

#     # 4) Expectations:
#     #    - Columns normalized to ['name','signup_date','score']
#     #    - Rows with missing or 'NAN' dropped → only first and last survive,
#     #      but second row has 'NAN' in score, third has empty signup_date → both drop,
#     #      so only the first row remains.
#     assert list(cleaned.columns) == ["name", "signup_date", "score"]
#     assert cleaned.shape == (1, 3)
#     assert cleaned.loc[0, "name"] == "Alice"
#     assert cleaned.loc[0, "signup_date"] == "2021-01-05"
#     assert cleaned.loc[0, "score"] == "100"

#     # 5) Write out cleaned CSV
#     output_file = examples / "cleaned_output.csv"
#     cleaned.to_csv(output_file, index=False)

#     # 6) Verify file exists and matches cleaned DataFrame
#     assert output_file.exists()
#     reloaded = pd.read_csv(output_file)
#     pd.testing.assert_frame_equal(reloaded, cleaned)
