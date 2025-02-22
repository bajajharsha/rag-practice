# src/app/services/upload_service.py

import time

from fastapi import Depends

from ..repositories.pinecone_repository import PineconeRepository
from ..utils.text_processing import TextProcessor


class UploadService:
    def __init__(
        self,
        pinecone_repo: PineconeRepository = Depends(),
        text_processor: TextProcessor = Depends(),
    ):
        self.pinecone_repo = pinecone_repo
        self.text_processor = text_processor

    async def process_upload(self, file):
        start_time = time.time()

        text = await self.text_processor.extract_text(file)
        chunks = self.text_processor.chunk_text(text)

        # 1. Use Pinecone-hosted embedding
        index = await self.pinecone_repo.embed_pinecone_hosted(chunks)

        # 2. Use MiniLM for embeddings before storing
        # await self.pinecone_repo.embed_minilm(chunks)

        end_time = time.time()
        print("Processing time:", end_time - start_time)
        return {"result": chunks}
