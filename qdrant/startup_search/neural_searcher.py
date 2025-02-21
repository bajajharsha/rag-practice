from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        # initialize Qdrant client
        self.qdrant_client = QdrantClient("http://localhost:6333")

    def search(self, text: str):
        # Convert text query into vector
        vector = self.model.encode(text).tolist()

        # Use `vector` for search for closest vectors in the collection
        search_result = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=vector,
            query_filter=None,  # If you don't want any filters for now
            limit=5,  # 5 the most closest results is enough
        ).points
        # `search_result` contains found vector ids with similarity scores along with the stored payload
        # In this function you are interested in payload only
        payloads = [hit.payload for hit in search_result]
        return payloads

    # city_of_interest = "Berlin"

    # # Define a filter for cities
    # city_filter = Filter(
    #     **{
    #         "must": [
    #             {
    #                 "key": "city",  # Store city information in a field of the same name
    #                 "match": {  # This condition checks if payload field has the requested value
    #                     "value": city_of_interest
    #                 },
    #             }
    #         ]
    #     }
    # )

    # search_result = self.qdrant_client.query_points(
    #     collection_name=self.collection_name,
    #     query=vector,
    #     query_filter=city_filter,
    #     limit=5,
    # ).points
    # ...
