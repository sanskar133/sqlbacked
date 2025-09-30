import logging
import os
import re
from typing import Any

import pandas as pd
import pymssql
from databases.base import Database, DatabaseFields

logger = logging.getLogger(__name__)


class Mssql(Database):
    display_name: str = "Mssql"
    description: str = "Connect Your Mssql Database"

    # TODO:
    # 1. Standardise database engine variable
    connection_details: dict = {}
    database_engine: Any = None

    def explain_query(self, query: str):
        # TODO: THIS DOES NOT WORK YET
        """add explain in final sql query to check if the the SQL query has proper table and coloumn names"""
        _explain_query = f"""SET SHOWPLAN_ALL ON;
        GO
        {query}
        GO
        SET SHOWPLAN_ALL OFF;
        GO
        """
        result, message = self.execute_query(_explain_query, validate=False)
        logger.info("Result of Explain Query: %s", result)
        if result:
            return result
        else:
            return f"ERROR: {message}"

    @property
    def field_config(self) -> list[DatabaseFields]:
        # driver = DatabaseFields(field_name="Driver", display_name="Driver")
        server = DatabaseFields(field_name="host", display_name="Host")
        database = DatabaseFields(field_name="database", display_name="Database Name")
        user = DatabaseFields(field_name="user", display_name="User Name")
        password = DatabaseFields(
            field_name="password", display_name="Password", type="password"
        )

        return [server, database, user, password]

    @property
    def has_valid_credentials(self) -> bool:
        logger.info("Checking if the user has valid Mssql Credential")
        try:
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }
            # connection_params = ";".join(
            #     [
            #         f"{field.field_name}={self.connection_details[field.field_name]}"
            #         for field in self.field_config
            #     ]
            # )
            # print("CONNECTIN:", connection_params)
            with pymssql.connect(**connection_params):
                return True

        except Exception as exc:
            logger.error(exc, exc_info=True)

    @property
    def database_schema(self):
        """Get schema of the Postgres table."""
        logger.info("Fetching database schema.")
        try:
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }
            # connection_params = ";".join(
            #     [
            #         f"{field.field_name}={self.connection_details[field.field_name]}"
            #         for field in self.field_config
            #     ]
            # )
            with pymssql.connect(**connection_params) as connection:
                cursor = connection.cursor()
                sql_query = """SELECT
                table_catalog,
                table_name,
                column_name,
                column_default,
                data_type
            FROM
                information_schema.columns
            WHERE
                table_schema IN ('public')
            ORDER BY
                table_schema,
                table_name,
                ordinal_position;"""
                cursor.execute(sql_query)
                data = cursor.fetchall()
                cursor.close()
            data = self.get_structured_schema(data)

            return data

        except Exception as database_schema_exc:
            logger.error(database_schema_exc, exc_info=True)

    def get_engine(self):
        logger.info("Get Engine For Postgres")
        try:
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }
            # connection_params = ";".join(
            #     [
            #         f"{field.field_name}={self.connection_details[field.field_name]}"
            #         for field in self.field_config
            #     ]
            # )
            self.database_engine = pymssql.connect(**connection_params)
            return True

        except Exception as exc:
            logger.error(exc, exc_info=True)

    def get_column_data_types_with_sample_value(self, query, validate: bool = True):
        if validate:
            logger.info("Checking if query should be run on database.")
            if not self._validate_query(query=query):
                return [
                    {
                        "message": "current query is not read query, this might impact the sanctity of your database."
                    }
                ]
        logger.info("Executing query to get column datatypes: %s" % query)
        with self.get_engine() as database_engine:
            try:
                cursor = database_engine.cursor()
                cursor.execute(query)

                desc = cursor.description
                column_info = [
                    {"key": col[0], "data_type": col[1], "sample_value": None}
                    for col in desc
                ]

                row = cursor.fetchone()
                if row:
                    for idx, value in enumerate(row):
                        column_info[idx]["sample_value"] = value

                return column_info
            except Exception as exc:
                print(
                    "Exception in executing postgres query for getting datatypes", exc
                )
                return [], exc
            finally:
                print("Closing cursor successfully")
                cursor.close()

    def execute_query(self, query, validate: bool = True):
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

        with self.database_engine.cursor() as cursor:
            try:
                cursor.execute(query)

                desc = cursor.description
                column_names = [col[0] for col in desc]
                data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
                return data, "COMPLETED"

            except Exception as exc:
                return {}, exc

    def get_column_data_types_with_sample_value(self, query, validate: bool = True):
        if validate:
            logger.info("Checking if query should be run on database.")
            if not self._validate_query(query=query):
                return [
                    {
                        "message": "current query is not read query, this might impact the sanctity of your database."
                    }
                ]
        logger.info("Executing query to get column datatypes: %s" % query)

        if not self.database_engine:
            self.get_engine()

        with self.database_engine.cursor() as cursor:
            try:
                cursor.execute(query)

                desc = cursor.description
                column_info = [
                    {"key": col[0], "data_type": col[1], "sample_value": None}
                    for col in desc
                ]

                row = cursor.fetchone()
                if row:
                    for idx, value in enumerate(row):
                        column_info[idx]["sample_value"] = value

                return column_info

            except Exception as exc:
                logger.error(
                    "Exception in executing postgres query for getting datatypes", exc
                )
                return [], exc

    def get_all_table_names(self):
        """Get a list of all table names in the Postgres database."""
        logger.info("Fetching all table names.")

        if not self.database_engine:
            self.get_engine()

        with self.database_engine.cursor() as cursor:
            try:
                sql_query = """SELECT table_name
                                FROM information_schema.tables
                                WHERE table_schema = 'public' AND table_type = 'BASE TABLE';"""
                cursor.execute(sql_query)
                tables = [table[0] for table in cursor.fetchall()]
                return tables

            except Exception as get_table_names_exc:
                logger.error(get_table_names_exc, exc_info=True)
                return []

    def get_all_columns_from_table(self, table_name):
        """Get a list of all column names in the specified table of the Postgres database."""
        logger.info(f"Fetching all column details for table: {table_name}.")

        if not self.database_engine:
            self.get_engine()

        with self.database_engine.cursor() as cursor:
            try:
                sql_query = f"""SELECT column_name, data_type
                            FROM information_schema.columns
                            WHERE table_schema = 'public' AND table_name = '{table_name}';"""
                cursor.execute(sql_query)
                columns_and_types = cursor.fetchall()
                values_sample = {}

                for column, data_type in columns_and_types:
                    try:
                        subquery = f"""SELECT \"{column}\" FROM \"{table_name}\" WHERE \"{column}\" IS NOT NULL LIMIT 1000"""
                        sql_query = (
                            f'SELECT DISTINCT "{column}" FROM ({subquery}) sub LIMIT 5;'
                        )
                        cursor.execute(sql_query)
                        values_sample[column] = [row[0] for row in cursor.fetchall()]
                    except Exception as e:
                        logger.error(
                            f"Error fetching data for column: {column}. Error: {e}",
                            exc_info=True,
                        )
                        values_sample[column] = []

                columns_info = [
                    {
                        "column_name": column,
                        "data_type": data_type,
                        "values_sample": values_sample[column],
                    }
                    for column, data_type in columns_and_types
                ]
                return columns_info

            except Exception as get_column_details_exc:
                logger.error(get_column_details_exc, exc_info=True)
                return []

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

            self.explain_query(query=sql_query_with_filter)
            return sql_query_with_filter

        except Exception as exc:
            logger.error(f"Exception in executing filtered query: {exc}", exc_info=True)
            return False

    def fetch_results_and_save_in_a_file(self, query, data_model_id):
        batch_size = 100000
        offset = 0
        file_name = f"source_data_files/data_source_{data_model_id}.csv"
        length = 0

        if not self.database_engine:
            self.get_engine()

        with self.database_engine.cursor() as cursor:

            try:
                while True:
                    query_with_limit_offset = (
                        f"{query} LIMIT {batch_size} OFFSET {offset}"
                    )
                    cursor.execute(query_with_limit_offset)
                    column_names = [desc[0] for desc in cursor.description]
                    results = cursor.fetchall()
                    length += len(results)
                    if not results:
                        if offset == 0:
                            return None
                        break

                    df = pd.DataFrame(results, columns=column_names)
                    if os.path.exists(file_name):
                        df.to_csv(file_name, mode="a", index=False, header=False)
                    else:
                        df.to_csv(file_name, index=False)
                    offset += batch_size

            except Exception as exc:
                logger.error("Exception in executing query:", exc)
                if os.path.exists(file_name):
                    os.remove(file_name)
                return None
            return file_name
