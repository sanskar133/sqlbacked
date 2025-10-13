from databases.dbx.vectorizers.base import BaseVectorModel
from databricks.vector_search.client import VectorSearchClient
from functools import wraps


def ensure_collection(func):
    """Decorator to ensure the correct collection is set before executing the method."""

    @wraps(func)
    def wrapper(self, collection_name, *args, **kwargs):
        # Set the collection index if needed
        if collection_name != self.current_collection:
            if not self.has_collection(collection_name):
                raise ValueError(f"Collection {collection_name} does not exist.")

            self.collection_index = self.get_index(collection_name)
            self.current_collection = collection_name

        # Call the original method
        return func(self, collection_name, *args, **kwargs)

    return wrapper


class DBXSyncVectorStore(BaseVectorModel):

    def __init__(self, endpoint_name: str = "semantic-search"):

        self.vsc = VectorSearchClient()

        self.endpoint_name = endpoint_name

        self.create_endpoint(endpoint_name=self.endpoint_name)

        self.collections = self.get_all_collections()

        self.current_collection = None

    def create_endpoint(self, endpoint_name: str):

        endpoints = self.vsc.list_endpoints()

        if endpoint_name not in [ep["name"] for ep in endpoints["endpoints"]]:

            self.vsc.create_endpoint(
                name=endpoint_name,
                endpoint_type="STANDARD",  # or "ENTERPRISE"
            )

        else:
            print(f"Endpoint {endpoint_name} already exists.")

    def create_collection(self, collection_name: str, primary_key: str, dimension: int):
        """Create a new collection (vector index table) in the vector store if it does not already exist."""

        if self.has_collection(collection_name):
            print(f"Collection {collection_name} already exists.")
            self.collection_index = self.get_index(collection_name)

        else:
            self.collection_index = self.vsc.create_delta_sync_index(
                endpoint_name=self.endpoint_name,
                source_table_name=collection_name,
                index_name=f"{collection_name}_index",
                pipeline_type="TRIGGERED",
                primary_key=primary_key,
                embedding_dimension=dimension,
                embedding_source_column="text",
                embedding_vector_column="vector",
                embedding_model_endpoint_name="e5-small-v2",
            )

            self.collections = self.get_all_collections()

        self.current_collection = collection_name

    def delete_collection(self, collection_name: str):

        if not self.has_collection(collection_name):
            # print(f"Collection {collection_name} does not exist.")
            raise ValueError(f"Collection {collection_name} does not exist.")

        self.vsc.delete_index(
            endpoint_name=self.endpoint_name,
            index_name=collection_name,
        )

        self.collections = self.get_all_collections()
        self.current_collection = None

    def get_all_collections(self):

        collections = self.vsc.list_indexes(self.endpoint_name)

        # print(collections)
        if collections == {} or "vector_indexes" not in collections:
            return []

        return [col["name"] for col in collections["vector_indexes"]]

    def has_collection(self, collection_name) -> bool:

        if collection_name in self.collections:
            return True

        return False

    def get_index(self, collection_name):

        return self.vsc.get_index(
            endpoint_name=self.endpoint_name,
            index_name=collection_name,
        )

    @ensure_collection
    def insert(self, collection_name, items):

        raise NotImplementedError("Insert method is not implemented yet.")

    @ensure_collection
    def upsert(self, collection_name, items):

        raise NotImplementedError("Upsert method is not implemented yet.")

    @ensure_collection
    def delete(self, collection_name, ids, filter=None):
        self.collection_index.delete(primary_keys=ids)

    @ensure_collection
    def query(self, collection_name, text, columns_to_return, filters=None, limit=5):
        results = self.collection_index.similarity_search(
            columns=columns_to_return,  # ["id", "text", "metadata"],
            query_text=text,
            filters=filters,
            num_results=limit,
            query_type="hybrid",
        )

        return results

    @ensure_collection
    def search(self, collection_name, text, columns_to_return, limit=5):
        results = self.collection_index.similarity_search(
            columns=columns_to_return,
            query_text=text,
            num_results=limit,
            query_type="hybrid",
        )

        return results

    def get(self, collection_name):
        pass

    def reset(self):

        collections = self.vsc.list_indexes(self.endpoint_name)
        for collection in collections["vector_indexes"]:
            self.vsc.delete_index(
                endpoint_name=self.endpoint_name,
                index_name=collection["name"],
            )
