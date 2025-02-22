import os

import pymupdf4llm
from fastapi import UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter


async def extract_pdf_text(file: UploadFile):
    """Save file manually and extract text."""
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = pymupdf4llm.to_markdown(file_path)

    os.remove(file_path)

    return text


def chunk_text(text, chunk_size=100, chunk_overlap=20):
    """Splits text into chunks of a fixed size with overlap."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)
