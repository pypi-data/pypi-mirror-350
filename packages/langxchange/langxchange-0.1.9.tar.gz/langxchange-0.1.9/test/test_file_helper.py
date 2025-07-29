import os
import json
import pandas as pd
import pytest
from langxchange.file_helper import FileHelper


@pytest.fixture
def file_helper():
    return FileHelper()


@pytest.fixture
def sample_files(tmp_path):
    # CSV
    csv_path = tmp_path / "sample.csv"
    pd.DataFrame([{"name": "Alice"}, {"name": "Bob"}]).to_csv(csv_path, index=False)

    # JSON
    json_path = tmp_path / "sample.json"
    with open(json_path, "w") as f:
        json.dump([{"name": "Alice"}, {"name": "Bob"}], f)

    # Excel
    excel_path = tmp_path / "sample.xlsx"
    pd.DataFrame([{"name": "Alice"}, {"name": "Bob"}]).to_excel(excel_path, index=False)

    return {
        "csv": str(csv_path),
        "json": str(json_path),
        "excel": str(excel_path),
        "invalid": str(tmp_path / "file.unsupported"),
        "missing": str(tmp_path / "notfound.csv")
    }


def test_load_csv(file_helper, sample_files):
    records = file_helper.load_file(sample_files["csv"], file_type="csv")
    assert len(records) == 2
    assert records[0]["name"] == "Alice"


def test_load_csv_chunked(file_helper, sample_files):
    records = file_helper.load_file(sample_files["csv"], file_type="csv", chunk_size=1)
    assert len(records) == 2
    assert all("name" in r for r in records)


def test_load_json(file_helper, sample_files):
    records = file_helper.load_file(sample_files["json"], file_type="json")
    assert len(records) == 2
    assert records[1]["name"] == "Bob"


def test_load_excel(file_helper, sample_files):
    records = file_helper.load_file(sample_files["excel"], file_type="xlsx")
    assert len(records) == 2
    assert isinstance(records, list)


def test_infer_file_type(file_helper, sample_files):
    records = file_helper.load_file(sample_files["json"])  # no file_type passed
    assert len(records) == 2


def test_unsupported_file_type(file_helper, sample_files):
    with open(sample_files["invalid"], "w") as f:
        f.write("invalid format")
    with pytest.raises(ValueError):
        file_helper.load_file(sample_files["invalid"])


def test_file_not_found(file_helper, sample_files):
    with pytest.raises(FileNotFoundError):
        file_helper.load_file(sample_files["missing"])
