import os

from dotenv import load_dotenv

from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_model = pc.create_index_from_model(
    name="llama-index",
    embed={
        "model": "llama-text-embed-v2",
        "field_map": {"text": "chunk_text"},
    },
)

index = pc.Index("llama-text-index")

data = [
    {
        "id": "1",
        "chunk_text": "Natural language processing is revolutionizing how we interact with computers",
    },
    {
        "id": "2",
        "chunk_text": "Machine learning algorithms can identify patterns in large datasets",
    },
    {
        "id": "3",
        "chunk_text": "Deep learning models have achieved remarkable results in computer vision",
    },
    {
        "id": "4",
        "chunk_text": "Vector embeddings help computers understand semantic relationships between words",
    },
    {
        "id": "5",
        "chunk_text": "Artificial intelligence is transforming industries across the globe",
    },
]

index.upsert_records("ns1", data)

response = index.search(
    namespace="ns1",
    query={"inputs": {"text": "how do computers understand semantics?"}, "top_k": 10},
)
for r in response["results"]["hits"]:
    print(
        f"ID: {r['id']} | Score: {r['score']:.3f} | Text: {r['fields']['chunk_text']}"
    )
