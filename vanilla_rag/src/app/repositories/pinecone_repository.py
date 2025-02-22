# src/app/repositories/pinecone_repository.py
import uuid

from pinecone import PineconeAsyncio, ServerlessSpec

from ..config.settings import settings


class PineconeRepository:
    def __init__(self):
        self.index_name = "llama-text-index"
        self.pc = None
        self.index = None

    async def create_index(self):
        """Creates the Pinecone index if it does not exist."""
        async with PineconeAsyncio(api_key=settings.PINECONE_API_KEY) as pc:
            if not await pc.has_index(self.index_name):
                await pc.create_index(
                    name=self.index_name,
                    dimension=1536,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                    deletion_protection="disabled",
                    tags={"environment": "development"},
                )
            self.pc = pc
            self.index = pc.IndexAsyncio(
                host="https://llama-text-index-hcrgmb6.svc.aped-4627-b74a.pinecone.io"
            )

    async def embed_pinecone_hosted(self, chunks):
        """Use Pinecone's hosted embeddings and store in the index."""

        # Create Index
        await self.create_index()

        # Embed & Upsert
        # Prepare data with UUIDs
        data = [{"id": str(uuid.uuid4()), "text": chunk} for chunk in chunks]
        embeddings = await self.pc.inference.embed(
            model="llama-text-embed-v2",
            inputs=[d["text"] for d in data],
            parameters={"input_type": "passage", "truncate": "END"},
        )

        vectors = []
        for d, e in zip(data, embeddings):
            vectors.append(
                {"id": d["id"], "values": e["values"], "metadata": {"text": d["text"]}}
            )

        self.index.upsert(vectors=vectors, namespace="example-namespace")

        # data = [{"id": str(i), "values": chunk} for i, chunk in enumerate(chunks)]
        # await index.upsert(vectors=data, namespace="ns1")

    async def embed_minilm(self, chunks):
        """Use MiniLM embeddings and store manually in Pinecone"""
        embeddings = self.pc.inference.embed(
            model="llama-text-embed-v2",
            inputs=chunks,
            parameters={"input_type": "passage", "truncate": "END"},
        )
        vectors = [
            {"id": str(i), "values": e["values"], "metadata": {"text": chunks[i]}}
            for i, e in enumerate(embeddings)
        ]
        self.index.upsert(vectors=vectors, namespace="example-namespace")
