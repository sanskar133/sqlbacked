import logging
import os
import re
from datetime import datetime
from typing import Any

import pandas as pd
import pyodbc
from databases.base import Database, DatabaseFields, Table, TableCatalog

logger = logging.getLogger(__name__)


class Ibm_i_db2(Database):
    display_name: str = "Ibm_i_db2"
    description: str = "Connect Your IBM db2 Database"

    # TODO:
    # 1. Standardise database engine variable
    connection_details: dict = {}
    database_engine: Any = None

    @property
    def field_config(self) -> list[DatabaseFields]:
        database = DatabaseFields(field_name="DATABASE", display_name="Database Name")
        dsn = DatabaseFields(field_name="DSN", display_name="DSN")
        user = DatabaseFields(field_name="UID", display_name="user")
        password = DatabaseFields(
            field_name="PWD", display_name="password", type="password"
        )

        return [database, dsn, user, password]

    @property
    def has_valid_credentials(self) -> bool:
        logger.info("Checking if the user has valid IBM db2 Credential")
        try:
            connection_params = ";".join(
                f"{field.field_name}={self.connection_details[field.field_name]}"
                for field in self.field_config[1:]
            )
            with pyodbc.connect(connection_params):
                return True

        except pyodbc.Error:
            logger.error("Error in connecting ibm db2 database", exc_info=True)
            return False

        except Exception as exc:
            logger.error(exc, exc_info=True)

    @property
    def database_schema(self):
        """Get schema of the IBM db2 table."""
        logger.info("Fetching database schema.")
        try:
            connection_params = ";".join(
                f"{field.field_name}={self.connection_details[field.field_name]}"
                for field in self.field_config[1:]
            )
            with pyodbc.connect(connection_params) as connection:
                sql_query = f"""SELECT
                    TABLE_SCHEMA AS TABLE_CATALOG,
                    TABLE_NAME,
                    COLUMN_NAME,
                    COLUMN_DEFAULT,
                    DATA_TYPE
                FROM
                    QSYS2.SYSCOLUMNS
                WHERE
                    TABLE_SCHEMA IN ('{self.connection_details[self.field_config[0].field_name]}')
                ORDER BY
                    TABLE_SCHEMA,
                    TABLE_NAME,
                    ORDINAL_POSITION
                """

                cursor = connection.cursor()
                cursor.execute(sql_query)

                data = cursor.fetchall(cursor)
                cursor.close()
                connection.close()
            data = self.get_structured_schema(data)

            return data

        except pyodbc.Error:
            logger.error("Error in connecting IBM db2 database", exc_info=True)
            return False

        except Exception as database_schema_exc:
            logger.error(database_schema_exc, exc_info=True)

    # overriding base method due to special case of ibm i db2
    def get_structured_schema(self, table_schema: list[tuple]):
        table_catalogs = []

        for row in table_schema:
            if (not table_catalogs) or (table_catalogs[-1].TABLE_CATALOG != row[0]):
                table_catalogs.append(TableCatalog(row[0]))
            if (not table_catalogs[-1].tables) or (
                table_catalogs[-1].tables[-1].TABLE_NAME != row[1]
            ):
                table_catalogs[-1].tables.append(Table(row[1]))
            table_catalogs[-1].tables[-1].columns.append(TableColumn(*row[2:]))

        schema_format = """"""
        for table_catalog in table_catalogs:
            schema_format += f"table_catalog: {table_catalog.TABLE_CATALOG}\n"
            for table in table_catalog.tables:
                schema_format += f"\ttable_name: {table.TABLE_NAME}\n"
                for column in table.columns:
                    schema_format += f"\t\tcolumn_name: {column.COLUMN_NAME}, column_default: {column.COLUMN_DEFAULT}, data_type: {column.DATA_TYPE}\n"

        return schema_format

    def get_engine(self):
        logger.info("Get Engine For IBM db2")
        try:
            connection_params = ";".join(
                f"{field.field_name}={self.connection_details[field.field_name]}"
                for field in self.field_config[1:]
            )
            self.database_engine = pyodbc.connect(connection_params)
            return True

        except pyodbc.Error:
            logger.error("Error in connecting ibm database", exc_info=True)
            return False

        except Exception as exc:
            logger.error(exc, exc_info=True)

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

        with self.database_engine as database_engine:
            try:
                cursor = database_engine.cursor()
                cursor.execute(
                    f"SET CURRENT SCHEMA = {self.connection_details[self.field_config[0].field_name]}"
                )
                cursor.execute(query)

                desc = cursor.description
                column_names = [col[0] for col in desc]
                data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
                return data, "COMPLETED"

            except Exception as exc:
                return {}, f"ERROR: {exc}"

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

        with self.database_engine as database_engine:
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
                logger.error(
                    "Exception in executing ibm db2 query for getting datatypes", exc
                )
                return [], exc
            finally:
                print("Closing cursor successfully")
                cursor.close()
                database_engine.close()

    def get_all_table_names(self):
        """Get a list of all table names in the IBM db2 database."""
        logger.info("Fetching all table names.")

        if not self.database_engine:
            self.get_engine()

        with self.database_engine as database_engine:
            try:
                sql_query = f"""SELECT TABLE_NAME FROM QSYS2.SYSTABLES WHERE
                TABLE_SCHEMA = '{self.connection_details[self.field_config[0].field_name]}' AND TABLE_TYPE = 'T'"""
                cursor = database_engine.cursor()
                cursor.execute(sql_query)
                tables = [table[0] for table in cursor.fetchall()]
                return tables

            except pyodbc.Error:
                logger.error(
                    "Error in connecting to the ibm db2 database", exc_info=True
                )
                return []

            except Exception as get_table_names_exc:
                logger.error(get_table_names_exc, exc_info=True)
                return []

    def get_all_columns_from_table(self, table_name):
        """Get a list of all column names in the specified table of the IBM db2 database."""
        logger.info(f"Fetching all column details for table: {table_name}.")

        if not self.database_engine:
            self.get_engine()

        with self.database_engine as database_engine:
            try:
                sql_query = f"""SELECT COLUMN_NAME, DATA_TYPE FROM QSYS2.SYSTABLES WHERE
                TABLE_SCHEMA = '{self.connection_details[self.field_config[0].field_name]}' AND TABLE_NAME = '{table_name}' """
                cursor = database_engine.cursor()
                cursor.execute(sql_query)
                columns_and_types = cursor.fetchall()
                values_sample = {}

                for column, data_type in columns_and_types:
                    try:
                        subquery = f"""SELECT \"{column}\" FROM \"{table_name}\" WHERE \"{column}\" IS NOT NULL FETCH FIRST 1000 ROWS ONLY"""
                        sql_query = f'SELECT DISTINCT "{column}" FROM ({subquery}) sub FETCH FIRST 5 ROWS ONLY'
                        cursor = database_engine.cursor()
                        cursor.execute(
                            f"SET CURRENT SCHEMA = {self.connection_details[self.field_config[0].field_name]}"
                        )
                        cursor.execute(sql_query)
                        values_sample[column] = [
                            row[0] for row in cursor.fetchall(cursor)
                        ]
                    except pyodbc.Error as e:
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

            except pyodbc.Error:
                logger.error(
                    "Error in connecting to the ibm db2 database", exc_info=True
                )
                return []

            except Exception as get_column_details_exc:
                logger.error(get_column_details_exc, exc_info=True)
                return []

    def execute_query_with_limit(self, query, limit=5):

        try:
            logger.info(f"Applying limit {limit} to SQL query: {query}")
            if "LIMIT" in query.upper():
                sql_query_with_limit = re.sub(
                    r"(LIMIT\s+\d+)",
                    f"FETCH FIRST {limit} ROWS ONLY",
                    query,
                    flags=re.IGNORECASE,
                )
            else:
                sql_query_with_limit = f"{query.strip()} LIMIT {limit}"
            query_result = self.execute_query(query=sql_query_with_limit)

            return query_result
        except Exception as exc:
            logger.error(
                f"Exception in executing ibm db2 query with limit: {exc}",
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

        with self.database_engine as database_engine:

            try:
                while True:
                    query_with_limit_offset = f"{query} OFFSET {offset} ROWS FETCH FIRST {batch_size} ROWS ONLY"
                    cursor = database_engine.cursor()
                    cursor.execute(query_with_limit_offset)
                    desc = cursor.description
                    column_names = [col[0] for col in desc]
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
