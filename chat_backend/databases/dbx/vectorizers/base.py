from abc import ABC, abstractmethod
from typing import List, Optional

from dbx.schema import GetResult, SearchResult, VectorItem


class BaseVectorModel(ABC):
    def __init__(self, name, **kwargs):
        self.name = name

    @abstractmethod
    def create_collection(self, collection_name: str, primary_key: str, dimension: int):
        """Create a new collection (vector index table) in the vector store."""
        pass

    @abstractmethod
    def has_collection(self, collection_name: str) -> bool:
        """Check if the collection exists based on the collection name."""
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        """Delete the collection based on the collection name."""
        pass

    @abstractmethod
    def search(
        self, collection_name: str, vectors: list[list[float | int]], limit: int
    ) -> Optional[SearchResult]:
        """Search for the nearest neighbor items based on the vectors and return 'limit' number of results."""
        pass

    @abstractmethod
    def query(
        self, collection_name: str, filter: dict, limit: Optional[int] = None
    ) -> Optional[GetResult]:
        """Query the items from the collection based on the filter."""
        pass

    @abstractmethod
    def get(self, collection_name: str) -> Optional[GetResult]:
        """Get all the items in the collection."""
        pass

    @abstractmethod
    def insert(self, collection_name: str, items: list[VectorItem]):
        """Insert the items into the collection, if the collection does not exist, it will be created."""
        pass

    @abstractmethod
    def upsert(self, collection_name: str, items: list[VectorItem]):
        """Update the items in the collection, if the items are not present, insert them. If the collection does not exist, it will be created."""
        pass

    @abstractmethod
    def delete(
        self,
        collection_name: str,
        ids: Optional[list[str]] = None,
        filter: Optional[dict] = None,
    ):
        """Delete the items from the collection based on the ids."""
        pass

    @abstractmethod
    def reset(self):
        """Resets the database. This will delete all collections and item entries."""
        pass
