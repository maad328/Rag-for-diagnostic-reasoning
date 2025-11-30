"""
Simple loader to process all JSON files and create document objects.
"""

import string
import json
import os
from pathlib import Path
import re
from langchain_core.documents import Document


def normalize_val(val):
    """
    Convert NA-like or missing values to empty string and strip whitespace.
    """
    if val is None:
        return ""
    if isinstance(val, str) and val.strip().upper() in ["NA", "N/A", "NONE", "-", ""]:
        return ""
    return str(val).strip()


def create_document_simple(json_file_path):
    """
    Simple, practical document creation with neutral headings.
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract diagnosis hierarchy (skip input keys)
    first_key = list(data.keys())[0]
    specific_diagnosis = first_key.split('$')[0]  # e.g., "NSTEMI"
    # Extract folder structure for category (keep in metadata only, not in text)
    path_parts = json_file_path.split(os.sep)
    category = path_parts[-2] if len(path_parts) >= 2 else "Unknown"

    # Build document text safely
    sections = [f"DIAGNOSIS: {specific_diagnosis}"]

    # Only include inputs with actual content
    for i in range(1, 7):  # input1..input6
        val = normalize_val(data.get(f"input{i}", ""))
        if val:
            val = clean_text1(val)
            sections.append(f"INPUT {i}:\n{val}")

    document_text = "\n\n".join(sections)

    return Document(
        page_content=document_text,
        metadata={"diagnosis": specific_diagnosis}
    )


def clean_text1(text: str) -> str:
    """
    Clean the document text for embeddings:
    - Remove repeated underscores, dashes, or other filler symbols
    - Replace multiple newlines with a single newline
    - Remove extra spaces
    - Remove non-printable characters
    - Strip leading/trailing whitespace
    """
    if not text:
        return ""

    # Remove non-printable characters
    text = ''.join(c for c in text if c in string.printable)

    # Remove repeated underscores or dashes
    text = re.sub(r'[_-]{2,}', ' ', text)

    # Remove repeated periods (e.g., "....") or colons
    text = re.sub(r'[.:]{2,}', '', text)

    # Replace multiple newlines with two newlines (for separation)
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'[ ]{2,}', ' ', text)

    # Strip leading/trailing whitespace on each line
    text = '\n'.join(line.strip() for line in text.splitlines())

    # Final strip
    return text.strip()


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_FINISHED_DIR = BASE_DIR / "mimic-iv-ext-direct-1.0.0" / "Finished"


def load_all_documents(root_dir):
    """
    Walk through all JSON files and create documents.

    Args:
        root_dir: Path to the 'Finished' directory

    Yields:
        Document dicts with id, text, and metadata
    """
    root_path = Path(root_dir)

    for json_file in root_path.rglob("*.json"):
        # Skip macOS metadata files
        if json_file.name.startswith("._"):
            continue

        yield create_document_simple(str(json_file))


def create_all_documents():
    """Create and return all documents as a list."""
    documents = list(load_all_documents(DEFAULT_FINISHED_DIR))
    print(f"Created {len(documents)} documents")
    return documents


