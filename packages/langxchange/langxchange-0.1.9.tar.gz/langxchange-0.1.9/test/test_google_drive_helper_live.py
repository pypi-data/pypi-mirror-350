import os
import shutil
import pytest
from pathlib import Path
from fpdf import FPDF
from PIL import Image
import pandas as pd

from langxchange.google_drive_helper import GoogleDriveHelper


@pytest.fixture(scope="module")
def drive():
    return GoogleDriveHelper(
        credentials_path="./creds/example.apps.googleusercontent.com.json",
        token_path="./creds/token.pickle"
    )


@pytest.fixture(scope="module")
def example_dir():
    path = Path("./examples")
    path.mkdir(parents=True, exist_ok=True)
    return path


@pytest.fixture(scope="module")
def test_folder_id(drive):
    folder_name = "LangXchange-Test-Folder"
    folder_id = drive.create_folder(folder_name)
    yield folder_id
    drive.delete_file(folder_id)


def upload_and_cleanup(drive, path, mime_type=None):
    file_id = drive.upload_file(str(path), mime_type=mime_type)
    assert file_id is not None
    drive.delete_file(file_id)


def test_upload_txt_file(drive, example_dir):
    file = example_dir / "example.txt"
    file.write_text("LangXchange test content.")
    upload_and_cleanup(drive, file, mime_type="text/plain")


def test_upload_xlsx_file(drive, example_dir):
    file = example_dir / "example.xlsx"
    df = pd.DataFrame({"Name": ["Alice"], "Score": [95]})
    df.to_excel(file, index=False)
    upload_and_cleanup(drive, file, mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def test_upload_pdf_file(drive, example_dir):
    file = example_dir / "example.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="LangXchange PDF Test", ln=1, align='C')
    pdf.output(str(file))
    upload_and_cleanup(drive, file, mime_type="application/pdf")


def test_upload_png_file(drive, example_dir):
    file = example_dir / "example.png"
    Image.new("RGB", (100, 100), color="blue").save(file)
    upload_and_cleanup(drive, file, mime_type="image/png")


def test_upload_jpeg_file(drive, example_dir):
    file = example_dir / "example.jpeg"
    Image.new("RGB", (100, 100), color="red").save(file, format="JPEG")
    upload_and_cleanup(drive, file, mime_type="image/jpeg")


def test_upload_and_list_all_in_folder(drive, example_dir, test_folder_id):
    file_specs = [
        ("example.txt", "LangXchange TXT", "text/plain"),
        ("example.xlsx", pd.DataFrame({"A": [1], "B": [2]}), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        ("example.pdf", "LangXchange PDF", "application/pdf"),
        ("example.png", (100, 100, "green"), "image/png"),
        ("example.jpeg", (100, 100, "orange"), "image/jpeg"),
    ]

    uploaded_ids = []

    for name, content, mime in file_specs:
        file_path = example_dir / name

        if mime == "text/plain":
            file_path.write_text(content)
        elif mime == "application/pdf":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=content, ln=1, align='C')
            pdf.output(str(file_path))
        elif mime.startswith("image"):
            w, h, color = content
            Image.new("RGB", (w, h), color=color).save(file_path)
        elif mime.endswith("sheet"):
            content.to_excel(file_path, index=False)

        file_id = drive.upload_file(str(file_path), parent_id=test_folder_id, mime_type=mime)
        uploaded_ids.append((name, file_id))

    # Verify all files are listed
    files = drive.list_files_in_folder(test_folder_id)
    names = [f["name"] for f in files]

    for name, _ in uploaded_ids:
        assert name in names

    # Cleanup
    for _, file_id in uploaded_ids:
        drive.delete_file(file_id)
