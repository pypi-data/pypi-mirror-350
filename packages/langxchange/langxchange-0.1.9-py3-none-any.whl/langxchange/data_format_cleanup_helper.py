# langxchange/data_format_cleanup_helper.py

import re
import time
import os
import uuid
import pandas as pd
import numpy as np


# Precompile regex to extract the cleaning function definition
_CLEAN_FUNC_PATTERN = re.compile(
    r"(def generate_format_clean_data\(df, output_path=None, output_format=['\"]\w+['\"]\):(?:\n {4}.*)+)",
    flags=re.MULTILINE
)


class DataFormatCleanupHelper:
    """
    Dynamically generates and applies a DataFrame cleaning function via an LLM helper,
    using the first 10 rows of the DataFrame as context, tracks timing, and can persist
    both the generated function source and cleaned output in a specified format.
    """

    def __init__(
        self,
        llm_helper,
        func_file_path: str = None,
        default_format: str = "csv"
    ):
        if not hasattr(llm_helper, "chat"):
            raise ValueError("llm_helper must provide a .chat(...) method")
        self.llm = llm_helper
        self.func_file_path = func_file_path
        self.default_format = default_format.lower()
        if self.default_format not in ("csv", "json", "txt"):
            raise ValueError(f"Unsupported default_format: {self.default_format}")

        # Validate func_file_path if provided
        if self.func_file_path:
            # If it's a directory, it's fine; if it's a file, ensure parent exists
            if not os.path.isdir(self.func_file_path):
                raise ValueError(f"File Path Supplied: {self.default_format} must be a folder")
                # parent = os.path.dirname(self.func_file_path)
                # if parent and not os.path.exists(parent):
                #     os.makedirs(parent, exist_ok=True)

        # Cached cleaning function and stats
        self._clean_func = None
        self.stats = {
            "prompt_time": 0.0,
            "extract_time": 0.0,
            "exec_time": 0.0,
            "clean_time": 0.0,
            "total_time": 0.0,
            "percent_complete": {},
        }

    def _get_clean_func(self, sample_context: pd.DataFrame) -> callable:
        """
        Calls the LLM to retrieve and exec the cleaning function code, tracking time.
        The generated function will accept (df, output_path=None, output_format='<fmt>')
        and write the cleaned DataFrame to disk accordingly.
        """
        # 1) Prompt + context
        t0 = time.perf_counter()
        snippet = sample_context.to_dict(orient="records")
        prompt = f"""
You are an expert Python developer. Here is a sample of the data (first {len(snippet)} rows):

{snippet}

Write a complete Python function definition:

def generate_format_clean_data(df, output_path=None, output_format="{self.default_format}"):

which:
- Normalizes column names to snake_case (strip, lowercase, replace spaces with underscores).
- Trims whitespace on all string columns.
- Converts literal "NAN" or empty strings in any column to actual NaN.
- Parses any column with "date" in its name into datetime.
- Drops rows with any NaN values.
- If `output_path` is provided, writes the cleaned DataFrame there in the given `output_format` 
  (one of 'csv', 'json', or 'txt'; default is '{self.default_format}').
- Returns the cleaned DataFrame to be stored in a vector database

Include only the function code (no additional text).
"""
        
       # print(prompt)
        response = self.llm.chat(
            messages=[
                {"role": "system", "content": "You are a helpful Python coding assistant."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )
        t1 = time.perf_counter()

        # 2) Extract via regex
        t2 = time.perf_counter()
        match = _CLEAN_FUNC_PATTERN.search(response)
        if not match:
            raise RuntimeError("Failed to extract cleaning function from LLM response.")
        func_src = match.group(1)
        t3 = time.perf_counter()

        # 3) Optionally persist function source to file or directory
        if self.func_file_path:
            if os.path.isdir(self.func_file_path):
                # write to a new file in this directory
                filename = f"functions_{uuid.uuid4().hex}.py"
                #file_path = os.path.join(self.func_file_path, filename)
                file_path = self.func_file_path + filename
            else:
                # treat as file path
                file_path = self.func_file_path
           
            with open(file_path, "w") as f:
                f.write(func_src)

        # 4) Exec to get function, providing np and pd
        t4 = time.perf_counter()
        local_ns = {}
        exec(func_src, {"np": np, "pd": pd}, local_ns)
        func = local_ns.get("generate_format_clean_data")
        if not callable(func):
            raise RuntimeError("generate_format_clean_data not defined after exec.")
        t5 = time.perf_counter()

        # Record stats
        self.stats["prompt_time"] = t1 - t0
        self.stats["extract_time"] = t3 - t2
        self.stats["exec_time"] = t5 - t4

        return func

    def clean(
        self,
        df: pd.DataFrame,
        output_path: str = None,
        output_format: str = None
    ) -> pd.DataFrame:
        """
        Generates (or regenerates) the cleaning function, applies it,
        tracks timing, and optionally writes the cleaned DataFrame to output_path
        in one of 'csv', 'json', or 'txt'. Uses default_format if output_format
        is not provided.
        """
        fmt = (output_format or self.default_format).lower()
        if fmt not in ("csv", "json", "txt"):
            raise ValueError(f"Unsupported format: {fmt}")

        # 1) Generate or retrieve the cleaning function
        sample = df.head(10)
        clean_fn = self._get_clean_func(sample)

        # 2) Clean the DataFrame
        t0 = time.perf_counter()
        cleaned = clean_fn(df, output_path, fmt)
        t1 = time.perf_counter()

        # 3) Record timing
        full_total = (
            self.stats["prompt_time"]
            + self.stats["extract_time"]
            + self.stats["exec_time"]
            + (t1 - t0)
        )
        self.stats["clean_time"] = t1 - t0
        self.stats["total_time"] = full_total

        # 4) Percent complete per stage
        for stage in ("prompt", "extract", "exec", "clean"):
            key = f"{stage}_time"
            self.stats["percent_complete"][stage] = (
                self.stats[key] / full_total * 100 if full_total > 0 else 0.0
            )

        return cleaned
