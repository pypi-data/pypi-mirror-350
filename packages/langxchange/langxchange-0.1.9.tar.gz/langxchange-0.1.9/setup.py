from setuptools import setup, find_packages
from pathlib import Path
import sys

# 1) Locate this script’s directory reliably
this_dir = Path(__file__).resolve().parent

# 2) Find any README.* file, case‐insensitive
readme_candidates = list(this_dir.glob("[Rr][Ee][Aa][Dd][Mm][Ee]"))
if not readme_candidates:
    print(f"❌ Could not find a README.* file in {this_dir}", file=sys.stderr)
    print("Files present:", [p.name for p in this_dir.iterdir()], file=sys.stderr)
    sys.exit(1)

# Prefer README.md if present
readme_path = next((p for p in readme_candidates if p.name.lower() == "readme.md"), readme_candidates[0])
long_description = readme_path.read_text(encoding="utf-8")

setup(
    name="langxchange",
    version="0.1.9",
    description="AI Toolkit for fast integration of Private Data and LLM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Timothy Owusu",
    author_email="ikolilu.tim.owusu@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "sentence-transformers",
        "chromadb",
        "pinecone-client",
        "sqlalchemy",
        "pymongo",
        "pymysql",
        "numpy",
        "google-generativeai",
        "openai",
        "anthropic",
        "weaviate-client",
        "qdrant-client",
        "elasticsearch",
        "elasticsearch-dsl",
        "opensearch-py",
        "faiss-cpu"
    ],
    python_requires=">=3.8",
)
