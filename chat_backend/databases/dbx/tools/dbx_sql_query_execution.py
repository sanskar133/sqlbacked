from databases.dbx.tools.base_sql_tool import BaseSQLTool  # type: ignore
from databricks import sql
import re
import os
import dotenv

dotenv.load_dotenv()


class DatabricksSqlQueryExecution(BaseSQLTool):

    def __init__(self):
        # super().__init__()
        pass

    def _validate_query(self, query: str) -> bool:
        """
        Return True if the query is strictly a read-only SELECT (including CTEs).
        Rejects INSERT/UPDATE/DELETE/DDL or write-like SELECT variants.
        """
        # Normalize whitespace and lowercase
        q = query.strip().lower()
        q = re.sub(r"\s+", " ", q)  # collapse multiple spaces/newlines

        # Quick reject: if query contains any forbidden keywords
        forbidden = [
            "insert",
            "update",
            "delete",
            "drop",
            "alter",
            "truncate",
            "create",
            "replace",
            "grant",
            "revoke",
            "into",  # e.g. SELECT ... INTO table
            "for update",  # e.g. SELECT ... FOR UPDATE
            "lock",
            "merge",
        ]
        if any(f" {kw} " in f" {q} " for kw in forbidden):
            return False

        # Must start with SELECT or WITH ... SELECT
        if q.startswith("select"):
            return True
        if re.match(r"^with\s+.+as\s*\(select.+\)\s*select", q, re.DOTALL):
            return True

        return False

    def fetch_metadata(self, tables: list = []):
        """Fetch and return the metadata of the given tables"""
        with sql.connect(
            server_hostname=os.environ["DATABRICKS_HOST"],
            http_path=os.environ["DATABRICKS_HTTP_PATH"],
            access_token=os.environ["DATABRICKS_TOKEN"],
        ) as connection:

            with connection.cursor() as cursor:

                metadata = {}
                for table_name in tables:
                    # table_name = table[1]

                    try:
                        cursor.execute(f"DESCRIBE {table_name}")
                        columns = cursor.fetchall()
                    except Exception as e:

                        raise ValueError(f"An error occurred: {e}")

                    metadata[table_name] = {
                        "columns": [
                            {
                                "column_name": col[0],
                                "data_type": col[1],
                                "column_description": col[2],
                            }
                            for col in columns
                        ]
                    }

                    cursor.execute(f"DESCRIBE DETAIL {table_name}")
                    columns = cursor.fetchall()
                    metadata[table_name]["table_description"] = [
                        col[3] for col in columns
                    ]

        return metadata

    def __call__(self, query: str):
        """Execute the query and return the result"""

        if not self._validate_query(query):
            raise ValueError("Invalid query: only SELECT queries are allowed.")

        with sql.connect(
            server_hostname=os.environ["DATABRICKS_HOST"],
            http_path=os.environ["DATABRICKS_HTTP_PATH"],
            access_token=os.environ["DATABRICKS_TOKEN"],
        ) as connection:

            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()

            except Exception as e:
                raise ValueError(f"Query execution failed: {e}")

        return result
