import os
import pandas as pd


class FileHelper:
    def __init__(self):
        pass

    def load_file(self, file_path: str, file_type: str = None, chunk_size: int = None) -> list:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Infer file type if not provided
        if not file_type:
            file_type = file_path.split(".")[-1].lower()

        if file_type == "csv":
            return self._load_csv(file_path, chunk_size)
        elif file_type == "json":
            return self._load_json(file_path)
        elif file_type in ["xls", "xlsx"]:
            return self._load_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    def _load_csv(self, file_path, chunk_size):
        all_records = []
        try:
            if chunk_size:
                for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                    all_records.extend(chunk.fillna("").to_dict(orient="records"))
            else:
                df = pd.read_csv(file_path)
                all_records = df.fillna("").to_dict(orient="records")
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to load CSV: {e}")
        return all_records

    def _load_json(self, file_path):
        try:
            df = pd.read_json(file_path)
            return df.fillna("").to_dict(orient="records")
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to load JSON: {e}")

    def _load_excel(self, file_path):
        try:
            df = pd.read_excel(file_path)
            return df.fillna("").to_dict(orient="records")
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to load Excel file: {e}")
