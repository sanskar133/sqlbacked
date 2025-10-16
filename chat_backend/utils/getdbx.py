from databricks.vector_search.client import VectorSearchClient


class dbxClient:
    def __init__(self):
        self.vector_store = VectorSearchClient()

    def get_description_index(
        self, index_name: str, query_embedding: list, k: int
    ) -> str:

        index = self.vector_store.get_index(
            index_name="workspace.default.table_desc_index"
        )
        results = index.similarity_search(
            query_vector=query_embedding,
            num_results=k,
            columns=["table_id", "japaneese"],
        )
        final_result = [
            row[1]
            for row in results.get("result", {}).get("data_array", [])
            if len(row) > 1
        ]
        final_result_str = "\n".join(final_result)
        return final_result_str

    def get_query_index(self, index_name: str, query_embedding: list, k: int) -> str:

        index = self.vector_store.get_index(
            index_name="workspace.default.sql_query_index"
        )
        results = index.similarity_search(
            query_vector=query_embedding,
            num_results=k,
            columns=["question_id", "japaneese"],
        )
        final_result = [
            row[1]
            for row in results.get("result", {}).get("data_array", [])
            if len(row) > 1
        ]
        final_result_str = "\n".join(final_result)
        return final_result_str
