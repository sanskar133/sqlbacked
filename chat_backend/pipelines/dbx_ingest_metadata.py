from databases.dbx.tools.dbx_sql_query_execution import (
    DatabricksSqlQueryExecution,
)
from databases.dbx.vectorizers.dbx_vector_store import DBXVectorStore
from databases.dbx.embeddings.dbx_embedding_model import DBXEmbeddingModel
from engine.llms.dbx_language_translater import DBXLanguageTranslater
from typing import Dict, List, Tuple, Any
import uuid


class DBXIngestMetaData:
    """Pipeline to ingest database metadata into Databricks Vector Search."""

    def __init__(self, endpoint_name: str):

        self.dbx_sql_tool = DatabricksSqlQueryExecution()
        self.vector_store = DBXVectorStore(endpoint_name=endpoint_name)
        self.embedding_model = DBXEmbeddingModel()
        self.translater = DBXLanguageTranslater()

    def process_metadata(
        self, tables: List[str], metadata: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Process raw metadata into structured format for embedding."""

        processed_metadata = {}
        processed_table_descriptions = {}

        for table in tables:
            if table in metadata:

                column_data = metadata[table]["columns"]
                table_data = metadata[table]["table_description"]

                # combine column name and column description as a single string
                metadata_text = [
                    f"Column name: {item['column_name']}. Description: {item['column_description']}."
                    for item in column_data
                ]
                # combine table name and table description as a single string
                table_text = [
                    f"Table name: {table}. Description: {desc}." for desc in table_data
                ]

                column_names = [item["column_name"] for item in column_data]
                data_type = [item["data_type"] for item in column_data]

                processed_metadata[table] = {
                    "name": column_names,
                    "data_types": data_type,
                    "embed": metadata_text,
                }

                processed_table_descriptions[table] = {
                    "name": tables,
                    "data_types": [],
                    "embed": table_text,
                }

        return processed_metadata, processed_table_descriptions

    def fetch_metadata(
        self, tables: List[str] = []
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Fetch and process metadata for given tables."""

        raw_metadata = self.dbx_sql_tool.fetch_metadata(tables=tables)

        processed_metadata, processed_table_descriptions = self.process_metadata(
            tables=tables, metadata=raw_metadata
        )

        return processed_metadata, processed_table_descriptions

    def _create_item_dict(
        self,
        name: str,
        data_type: str,
        desc: str,
        vector: List[float],
        table: str,
        ingest_tables: bool = False,
    ) -> Dict[str, Any]:
        """Create a standardized item dictionary for vector store ingestion."""

        base_item = {
            "table_id": table,
            "name": name,
            "description": desc,
            "translated_description": "",
            "vector": vector,
        }

        if not ingest_tables:
            base_item.update(
                {
                    "column_id": str(uuid.uuid4()),
                    "data_type": data_type,
                }
            )

        return base_item

    def _get_collection_config(
        self, table: str, ingest_tables: bool
    ) -> Tuple[str, str]:
        """Get collection configuration based on ingestion type."""

        if ingest_tables:
            collection_name = f"{table}_index"
            primary_key = "table_id"
        else:
            collection_name = f"{table}_columns_index"
            primary_key = "column_id"

        return collection_name, primary_key

    def ingest_metadata(
        self,
        metadata: Dict[str, Any] = {},
        schemas: Dict[str, Any] = {},
        ingest_tables: bool = False,
    ) -> None:
        """Ingest metadata into vector store collections."""

        for table, meta in metadata.items():
            schema = schemas.get(
                table, {}
            ).copy()  # Create a copy to avoid modifying original

            # Get collection configuration
            collection_name, primary_key = self._get_collection_config(
                table, ingest_tables
            )

            # Prepare schema for collection creation
            if ingest_tables:
                schema.pop("data_type", None)
                schema.pop("column_id", None)

            dimension = 768
            embedding_column_name = "vector"
            schema[embedding_column_name] = "array<float>"

            # Create collection
            self.vector_store.create_collection(
                collection_name=collection_name,
                primary_key=primary_key,
                dimension=dimension,
                embedding_column_name=embedding_column_name,
                schema=schema,
            )

            # Generate embeddings and create records
            embeddings = self.embedding_model.get_embedding(text=meta["embed"])
            records = [
                self._create_item_dict(
                    name=name,
                    data_type=data_type,
                    desc=desc,
                    vector=vector,
                    table=table,
                    ingest_tables=ingest_tables,
                )
                for name, data_type, desc, vector in zip(
                    meta["name"],
                    meta["data_types"],
                    meta["embed"],
                    embeddings,
                )
            ]

            # Upsert records to vector store
            self.vector_store.upsert(
                collection_name=collection_name,
                items=records,
            )

    def __call__(self, tables: List[str] = [], schemas: Dict[str, Any] = {}) -> None:
        """Main entry point for metadata ingestion pipeline.

        Args:
            tables: List of table names to ingest metadata for.
            schemas: dictionary specifying schema details for each table.

            example:
            {"table_name": {
                "column_id": "string",
                "table_id": "string",
                "name": "string",
                ...
            }
        """

        # STEP 1: Fetch table and column metadata from the database
        column_data, table_data = self.fetch_metadata(tables=tables)
        # STEP 2: Translate metadata into English using LLM
        translated_data = self.translater(
            text=str({"columns": column_data, "tables": table_data})
        )
        translated_column_data = translated_data.get("columns", {})
        translated_table_data = translated_data.get("tables", {})
        # STEP 3: Ingest translated metadata into vector store
        # TODO: Implement multi-threading/multiprocessing for ingestion
        self.ingest_metadata(
            metadata=translated_column_data, schemas=schemas, ingest_tables=False
        )
        self.ingest_metadata(
            metadata=translated_table_data, schemas=schemas, ingest_tables=True
        )
