import logging
import re
import os
from google.cloud import bigquery
from google.auth import exceptions as auth_exceptions
from database_connection_management.databases.base import Database, DatabaseFields
from typing import Any

logger = logging.getLogger(__name__)


class Bigquery(Database):
    display_name: str = "Bigquery"
    description: str = "Connect Your Bigquery Dataset"

    # TODO:
    # 1. Standardise database engine variable
    connection_details: dict = {}
    database_engine: Any = None

    @property
    def field_config(self) -> list[DatabaseFields]:
        dataset_id = DatabaseFields(field_name="dataset_id", display_name="Dataset Id")
        credentials = DatabaseFields(
            field_name="credentials", display_name="Credentials File"
        )

        return [dataset_id, credentials]

    @property
    def has_valid_credentials(self) -> bool:
        logger.info("Checking if the user has valid BigQuery Credentials")
        try:
            connection_params = {**self.connection_details["credentials"]}
            client = bigquery.Client.from_service_account_info(connection_params)
            datasets = list(client.list_datasets())
            return True

        except auth_exceptions.DefaultCredentialsError:
            logger.error(
                "Error in connecting to BigQuery. Default credentials not found.",
                exc_info=True,
            )
            return False
        except auth_exceptions.GoogleAuthError:
            logger.error(
                "Error in connecting to BigQuery. Invalid credentials.", exc_info=True
            )
            return False
        except Exception as exc:
            logger.error(exc, exc_info=True)
            return False

    @property
    def database_schema(self):
        """Get schema of the BigQuery dataset."""
        logger.info("Fetching BigQuery dataset schema.")
        try:
            connection_params = {**self.connection_details["credentials"]}
            client = bigquery.Client.from_service_account_info(connection_params)

            dataset_id = self.connection_details["dataset_id"]
            tables = client.list_tables(dataset_id)
            schema_data = []
            for table in tables:
                table_schema = client.get_table(f"{dataset_id}.{table.table_id}").schema
                table_info = {"table_name": table.table_id, "columns": []}
                for field in table_schema:
                    column_info = {
                        "column_name": field.name,
                        "column_default": None,  # Adjust if necessary
                        "data_type": field.field_type,
                    }
                    table_info["columns"].append(column_info)
                schema_data.append(table_info)
            return schema_data
        except Exception as exc:
            logger.error(exc, exc_info=True)
            return False

    def get_engine(self):
        logger.info("Get Engine for BigQuery")

        try:
            connection_params = {**self.connection_details["credentials"]}
            client = bigquery.Client.from_service_account_info(connection_params)
            self.database_engine = client

            return True
        except Exception as exc:
            logger.error(exc, exc_info=True)
            return False

    def execute_query(self, query: str, validate: bool = True) -> dict:
        if validate:
            logger.info("Checking if query should be run on database.")
            if not self._validate_query(query=query):
                return [
                    {
                        "message": "current query is not read query, this might impact the sanctity of your database."
                    }
                ]
        logger.info("Executing query: %s" % query)

        if not self.database_engine:
            self.get_engine()

        try:
            query_job = self.database_engine.query(query)
            results = query_job.result()

            column_names = [field.name for field in results.schema]
            data = [dict(zip(column_names, row.values())) for row in results]

            logging.info("Data after executing query: %s" % data)

            return data

        except Exception as exc:
            logger.error(f"Exception in executing BigQuery query: {exc}", exc_info=True)
            return []

    def get_all_table_names(self):
        """Get a list of all table names in the BigQuery dataset."""
        logger.info("Fetching all table names.")

        if not self.database_engine:
            self.get_engine()

        try:

            # List all tables in the dataset
            tables = self.database_engine.list_tables(
                self.connection_details["dataset_id"]
            )

            # Extract table names
            table_names = [table.table_id for table in tables]

            return table_names

        except Exception as get_table_names_exc:
            logger.error(get_table_names_exc, exc_info=True)
            return []

    def get_all_columns_from_table(self, table_name: str):
        """Get a list of all column names in the specified table of the BigQuery dataset."""
        logger.info(f"Fetching all column details for table: {table_name}.")

        if not self.database_engine:
            self.get_engine()

        try:
            table_ref = f'{self.connection_details["dataset_id"]}.{table_name}'
            table_schema = self.database_engine.get_table(table_ref).schema

            values_sample = {}

            for field in table_schema:
                column = field.name
                try:
                    subquery = f"SELECT `{column}` FROM `{table_ref}` WHERE `{column}` IS NOT NULL LIMIT 1000"
                    sql_query = (
                        f"SELECT DISTINCT `{column}` FROM ({subquery}) sub LIMIT 5;"
                    )
                    query_job = self.database_engine.query(sql_query)
                    values_sample[column] = [row[column] for row in query_job.result()]
                except Exception as e:
                    logger.error(
                        f"Error fetching data for column: {column}. Error: {e}",
                        exc_info=True,
                    )
                    values_sample[column] = []

            columns_info = [
                {
                    "column_name": field.name,
                    "data_type": field.field_type,
                    "values_sample": values_sample[field.name],
                }
                for field in table_schema
            ]

            return columns_info

        except Exception as get_column_details_exc:
            logger.error(get_column_details_exc, exc_info=True)
            return []

    def get_column_data_types_with_sample_value(
        self, query: str, validate: bool = True
    ):
        try:
            if validate and not self._validate_query(query):
                return [{"message": "Query is not a read query"}]

            logger.info(
                "Executing query to get column data types and sample values: %s" % query
            )
            if not self.database_engine:
                self.get_engine()
            query_job = self.database_engine.query(query)  # Execute the query

            # Fetch column information and sample values directly
            column_info = [
                {
                    "column_name": field.name,
                    "data_type": field.field_type,
                    "sample_value": list(
                        set(row[field.name] for row in query_job.result(max_results=5))
                    ),
                }
                for field in query_job.result().schema
            ]

            return column_info

        except Exception as exc:
            logger.error(
                "Exception in executing BigQuery query: %s", exc, exc_info=True
            )
            return [], exc

    def execute_query_with_limit(self, query, limit=5):

        try:
            logger.info(f"Applying limit {limit} to SQL query: {query}")
            if "LIMIT" in query.upper():
                sql_query_with_limit = re.sub(
                    r"(LIMIT\s+\d+)", f"LIMIT {limit}", query, flags=re.IGNORECASE
                )
            else:
                sql_query_with_limit = f"{query.strip()} LIMIT {limit}"
            query_result = self.execute_query(query=sql_query_with_limit)

            return query_result
        except Exception as exc:
            logger.error(
                f"Exception in executing postgres query with limit: {exc}",
                exc_info=True,
            )
            return {}, exc

    def execute_query_with_time_filter(
        self, query, column_name, from_date=None, to_date=None
    ):

        try:
            logger.info(f"Executing filtered query: {query}")
            date_filter = ""

            if from_date and to_date:
                date_filter = f"\"{column_name}\" BETWEEN '{from_date}' AND '{to_date}'"
            elif from_date:
                date_filter = f"\"{column_name}\" >= '{from_date}'"
            elif to_date:
                date_filter = f"\"{column_name}\" <= '{to_date}'"

            sql_query_with_filter = query.strip() + (
                f" WHERE {date_filter}" if date_filter else ""
            )

            return self.execute_query(query=sql_query_with_filter)
        except Exception as exc:
            logger.error(f"Exception in executing filtered query: {exc}", exc_info=True)
            return {}, exc

    def fetch_results_and_save_in_a_file(self, query, data_model_id):
        batch_size = 100000
        offset = 0
        file_name = f"source_data_files/data_source_{data_model_id}.csv"
        length = 0

        try:
            import pandas as pd

            if not self.database_engine:
                self.get_engine()

            while True:

                query_with_limit_offset = f"{query} LIMIT {batch_size} OFFSET {offset}"
                query_job = self.database_engine.query(query_with_limit_offset)
                results = query_job.result()
                df = pd.DataFrame(data=[list(row.values()) for row in results])

                if os.path.exists(file_name):
                    df.to_csv(file_name, mode="a", index=False, header=False)
                else:
                    df.to_csv(file_name, index=False, header=list(results.schema))

                length += len(df)

                if len(df) < batch_size:
                    break

                offset += batch_size

        except Exception as exc:
            logger.error("Exception in executing query:", exc)
            if os.path.exists(file_name):
                os.remove(file_name)
            return None

        return file_name
