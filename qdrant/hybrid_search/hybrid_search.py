import json
import logging

from qdrant_client import QdrantClient
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    filename="qdrant_upload.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("Starting Qdrant data upload script...")

# Initialize Qdrant client
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "startups_hybrid"

try:
    client = QdrantClient(url=QDRANT_URL)
    logging.info(f"Connected to Qdrant at {QDRANT_URL}")
except Exception as e:
    logging.error(f"Failed to connect to Qdrant: {e}")
    exit(1)

# Load data
payload_path = "qdrant/hybrid_search/startups_demo.json"
documents = []
metadata = []

try:
    with open(payload_path) as fd:
        for line in fd:
            obj = json.loads(line)
            documents.append(obj.pop("description"))
            metadata.append(obj)

    logging.info(f"Loaded {len(documents)} documents from {payload_path}")
except Exception as e:
    logging.error(f"Error loading dataset: {e}")
    exit(1)

# Check if collection exists, else create it
if not client.collection_exists(COLLECTION_NAME):
    try:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=client.get_fastembed_vector_params(),
            sparse_vectors_config=client.get_fastembed_sparse_vector_params(),
        )
        logging.info(f"Created collection: {COLLECTION_NAME}")
    except Exception as e:
        logging.error(f"Failed to create collection: {e}")
        exit(1)
else:
    logging.info(f"Collection '{COLLECTION_NAME}' already exists.")

# Upload data in batches
BATCH_SIZE = 100  # Adjust based on system performance
PARALLEL_WORKERS = 2  # Reduce to avoid CPU overheating

try:
    logging.info("Starting data upload...")
    for i in tqdm(range(0, len(documents), BATCH_SIZE), desc="Uploading batches"):
        batch_docs = documents[i : i + BATCH_SIZE]
        batch_meta = metadata[i : i + BATCH_SIZE]

        client.add(
            collection_name=COLLECTION_NAME,
            documents=batch_docs,
            metadata=batch_meta,
            parallel=PARALLEL_WORKERS,
        )
        logging.info(f"Uploaded batch {i // BATCH_SIZE + 1}")

    logging.info("Data upload completed successfully!")
except Exception as e:
    logging.error(f"Error during upload: {e}")
    exit(1)
