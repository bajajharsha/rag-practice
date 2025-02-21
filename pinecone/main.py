import os
import time

from dotenv import load_dotenv

from pinecone import Pinecone, ServerlessSpec

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# Create Index
index_name = "llama-text-embed-v2"


def integrated_embedding_index():
    if not pc.has_index(index_name):
        index_model = pc.create_index_for_model(
            name=index_name,
            cloud="aws",
            region="us-east-1",
            embed={
                "model": "llama-text-embed-v2",
                "field_map": {"text": "data"},
            },
        )
        print(index_model)


def create_index():
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    index = pc.Index(index_name)

    return index


data = [
    {
        "id": "vec1",
        "text": "Apple is a popular fruit known for its sweetness and crisp texture.",
    },
    {
        "id": "vec2",
        "text": "The tech company Apple is known for its innovative products like the iPhone.",
    },
    {"id": "vec3", "text": "Many people enjoy eating apples as a healthy snack."},
    {
        "id": "vec4",
        "text": "Apple Inc. has revolutionized the tech industry with its sleek designs and user-friendly interfaces.",
    },
    {"id": "vec5", "text": "An apple a day keeps the doctor away, as the saying goes."},
    {
        "id": "vec6",
        "text": "Apple Computer Company was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne as a partnership.",
    },
]

# embeddings = pc.inference.embed(
#     model="llama-text-embed-v2",
#     inputs=[d["text"] for d in data],
#     parameters={"input_type": "passage", "truncate": "END"},
# )

# vectors = []
# for d, e in zip(data, embeddings):
#     vectors.append(
#         {"id": d["id"], "values": e["values"], "metadata": {"text": d["text"]}}
#     )

# index.upsert(vectors=vectors, namespace="example-namespace")


def main():
    start_time = time.time()
    # index = create_index()
    integrated_embedding_index()
    # print(index)
    print("This code runs only when the file is executed directly.")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time elapsed: {elapsed_time} seconds")


if __name__ == "__main__":
    main()
