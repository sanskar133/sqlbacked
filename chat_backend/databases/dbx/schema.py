from typing import Any, List, Optional

from pydantic import BaseModel


# -----------------Vector Store Schemas-----------------#
class VectorItem(BaseModel):
    id: str
    data: Any
    vector: List[float | int]


class GetResult(BaseModel):
    ids: Optional[List[str]]
    documents: Optional[List[str]]
    metadatas: Optional[List[Any]]


class SearchResult(GetResult):
    distances: Optional[List[float | int]]


# -----------------SQL Query Execution Schemas-----------------#
class TableSchema(BaseModel):
    column_name: str
    data_type: str
    column_description: Optional[str] = None


# -----------------Embedding Model Schemas-----------------#
class EmbeddingResult(BaseModel):
    input: List[str]
    embedding: List[List[float | int]]
