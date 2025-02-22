# src/app/utils/text_processing.py

import os

import pymupdf4llm
from fastapi import UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter


class TextProcessor:
    async def extract_text(self, file: UploadFile):
        """Extract text from a file."""
        if file.content_type == "application/pdf":
            return await self._extract_pdf_text(file)  # Use _extract_pdf_text for PDFs
        else:
            text = await file.read()
            return text.decode("utf-8")

    def chunk_text(self, text: str, chunk_size: int = 100, chunk_overlap: int = 20):
        """Splits text into chunks of a fixed size with overlap."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        return text_splitter.split_text(text)

    async def _extract_pdf_text(self, file: UploadFile):
        """Save file manually and extract text using pymupdf4llm."""
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)

        # ✅ FIX: Use synchronous open() inside async function
        with open(file_path, "wb") as f:
            f.write(await file.read())  # Sync file writing

        text = pymupdf4llm.to_markdown(file_path)

        os.remove(file_path)  # Cleanup after extraction

        return text
