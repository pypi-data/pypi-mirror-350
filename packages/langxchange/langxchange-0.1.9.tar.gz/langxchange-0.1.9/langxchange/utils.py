import json
import pandas as pd

def load_data(source, source_type):
    if source_type == "csv":
        return pd.read_csv(source)
    elif source_type == "json":
        return pd.read_json(source)
    elif source_type == "dataframe":
        if isinstance(source, pd.DataFrame):
            return source
        else:
            raise TypeError("Expected a Pandas DataFrame.")
    else:
        raise ValueError(f"Unsupported source_type: {source_type}")
