# pip install "pinecone[asyncio]"
import asyncio

from pinecone import PineconeAsyncio, ServerlessSpec


async def main():
    async with PineconeAsyncio(
        api_key="pcsk_3wxgrt_ACNDWAkGRoNwG7Tkof4BY2m28ipRChDG1uhpWdupnZ5vRbEfANdv5UCNdtZWTpt"
    ) as pc:
        if not await pc.has_index("llama-text-index"):
            desc = await pc.create_index(
                name="example-index",
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                deletion_protection="disabled",
                tags={"environment": "development"},
            )


asyncio.run(main())
