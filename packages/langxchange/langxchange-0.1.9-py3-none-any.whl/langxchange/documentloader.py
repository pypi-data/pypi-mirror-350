# langxchange/document_loader_helper.py

import os
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None


class DocumentLoaderHelper:
    """
    Helper to load and extract textual content from various document types
    (txt, csv, json, pdf, excel, docx) in parallel, with progress tracking.
    """

    def __init__(self, chunk_size: int = None, csv_chunksize: int = 1000, max_workers: int = 4):
        """
        :param chunk_size: maximum characters per text chunk
        :param csv_chunksize: number of rows per chunk when loading CSV
        :param max_workers: threads to use for parallel extraction/chunking
        """
        self.chunk_size = chunk_size
        self.csv_chunksize = csv_chunksize
        self.max_workers = max_workers

        # Stats
        self.stats = {
            "total_units": 0,
            "processed_units": 0,
            "times": {
                "load": 0.0,
                "chunk": 0.0,
                "total": 0.0
            }
        }

    def load(self, file_path: str):
        """
        Extract text chunks from the file in parallel and yield them.
        Updates self.stats with timing and progress.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        start_total = time.perf_counter()

        ext = os.path.splitext(file_path)[1].lower()

        # 1) gather raw units
        t0 = time.perf_counter()
        if ext == ".txt":
            units = self._load_txt_units(file_path)
        elif ext == ".csv":
            units = self._load_csv_units(file_path)
        elif ext == ".json":
            units = self._load_json_units(file_path)
        elif ext == ".pdf":
            units = self._load_pdf_units(file_path)
        elif ext in (".xls", ".xlsx"):
            units = self._load_excel_units(file_path)
        elif ext == ".docx":
            units = self._load_docx_units(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        t1 = time.perf_counter()
        self.stats["times"]["load"] = t1 - t0

        self.stats["total_units"] = len(units)
        self.stats["processed_units"] = 0

        # 2) process units in parallel: chunking if needed
        t2 = time.perf_counter()
        with ThreadPoolExecutor(max_workers=self.max_workers) as exe:
            futures = {exe.submit(self._chunk_unit, u): u for u in units}
            for future in as_completed(futures):
                chunks = future.result()
                self.stats["processed_units"] += 1
                for c in chunks:
                    yield c
        t3 = time.perf_counter()
        self.stats["times"]["chunk"] = t3 - t2
        self.stats["times"]["total"] = time.perf_counter() - start_total

    def _chunk_unit(self, text: str):
        """
        Split a single text unit into chunk_size pieces.
        """
        if not self.chunk_size or len(text) <= self.chunk_size:
            return [text]
        chunks = []
        start = 0
        n = len(text)
        while start < n:
            end = min(start + self.chunk_size, n)
            seg = text[start:end]
            # break on newline or space
            cut = max(seg.rfind("\n"), seg.rfind(" "))
            if cut > 0:
                chunks.append(text[start:start + cut])
                start += cut
            else:
                chunks.append(seg)
                start = end
        return chunks

    def _load_txt_units(self, path: str):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            if self.chunk_size:
                units = []
                while True:
                    buf = f.read(self.chunk_size * 4)
                    if not buf:
                        break
                    units.append(buf)
                return units
            return [f.read()]

    def _load_csv_units(self, path: str):
        units = []
        for df_chunk in pd.read_csv(path, chunksize=self.csv_chunksize, dtype=str):
            text = df_chunk.fillna("").astype(str).agg(" ".join, axis=1)
            units.append("\n".join(text.tolist()))
        return units

    def _load_json_units(self, path: str):
        """
        Load JSON file and produce text units per record.
        Supports both arrays-of-objects and object-of-arrays.
        """
        df = pd.read_json(path, dtype=str)
        # Normalize nested structures into flat table
        df = pd.json_normalize(df.to_dict(orient="records"))
        rows = df.fillna("").astype(str).agg(" ".join, axis=1)
        return ["\n".join(rows.tolist())]

    def _load_pdf_units(self, path: str):
        if PyPDF2 is None:
            raise ImportError("PyPDF2 is required for PDF support")
        units = []
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                units.append(page.extract_text() or "")
        return units

    def _load_excel_units(self, path: str):
        df = pd.read_excel(path, dtype=str, engine="openpyxl")
        rows = df.fillna("").astype(str).agg(" ".join, axis=1)
        return ["\n".join(rows.tolist())]

    def _load_docx_units(self, path: str):
        if docx is None:
            raise ImportError("python-docx is required for DOCX support")
        document = docx.Document(path)
        return [p.text for p in document.paragraphs if p.text]
