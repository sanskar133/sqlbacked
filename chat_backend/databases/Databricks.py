import logging
import os
import traceback
from typing import Any

from databases.base import Database, DatabaseFields
from databricks import sql
from dotenv import load_dotenv
load_dotenv()  # loads .env file

logger = logging.getLogger(__name__)


class Databricks(Database):
    display_name: str = "Databricks"
    description: str = "Connect Your Databricks Database"

    connection_details: dict 
    database_engine: Any = None

    connection_type: str = "STANDARD"

    catalog_name: str = os.getenv("DATABRICKS_CATALOG_NAME")

    @property
    def field_config(self) -> list[DatabaseFields]:
        server_hostname = DatabaseFields(
            field_name="server_hostname", display_name="Server Hostname"
        )
        http_path = DatabaseFields(field_name="http_path", display_name="HTTP Path")
        access_token = DatabaseFields(
            field_name="access_token", display_name="Access Token", type="password"
        )

        return [server_hostname, http_path, access_token]

    @property
    def has_valid_credentials(self) -> bool:
        logger.info("Checking if the user has valid Databricks credentials")
        try:
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }
            with sql.connect(**connection_params) as conn:
                cs = conn.cursor()
            return True
        except sql.Error:
            logger.error("Error in connecting to Databricks Account, ", exc_info=True)
            return False
        except Exception as exc:
            logger.error(exc, exc_info=True)

    @property
    def database_schema(self):
        """Get Schema of the Databricks Schema"""
        logger.info("Fetching Database schema.")
        logger.info(f"Catalog name: {self.catalog_name}")   
        try:
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }
            schema = (
                "default" if self.connection_type == "STANDARD" else "processed_tables"
            )

            with sql.connect(**connection_params) as connection:
                cursor = connection.cursor()
                sql_query = f"""SELECT
                table_catalog,
                table_name,
                column_name,
                column_default,
                data_type
            FROM
                system.information_schema.columns
            WHERE table_schema='{schema}'
            ORDER BY
                table_schema,
                table_name,
                ordinal_position;"""
                cursor.execute(sql_query)
                data = cursor.fetchall()
                cursor.close()

            data = self.get_structured_schema(data)
            return data
        except sql.Error:
            logger.error("Error in connecting Databricks Database", exc_info=True)
            return False
        except Exception as database_schema_exc:
            logger.error(database_schema_exc, exc_info=True)

    def get_engine(self):
        logger.info("Get Engine for Databricks")
        try:
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }
            self.database_engine = sql.connect(**connection_params)
            return True
        except sql.Error:
            logger.error("Error in connecting Databricks Database", exc_info=True)
            return False
        except Exception as exc:
            logger.error(exc, exc_info=True)

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

        cursor = self.database_engine.cursor()
        cursor.execute(query)

        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]

        cursor.close()

        logging.info("Data after executing query: %s" % data)

        return data, "COMPLETED"

    # TODO This is only a template code for Databricks. Need to test it after getting the credentials
    # Add sql query after getting credentials
    def get_all_table_names(self):
        """Get a list of all table names in the Databricks database."""
        logger.info("Fetching all table names.")
        try:
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }
            with sql.connect(**connection_params) as connection:
                cursor = connection.cursor()
                sql_query = "SHOW TABLES"
                cursor.execute(sql_query)
                tables = [table[0] for table in cursor.fetchall()]
                cursor.close()
            return tables
        except sql.Error:
            logger.error("Error in connecting to Databricks database", exc_info=True)
            return []
        except Exception as get_table_names_exc:
            logger.error(get_table_names_exc, exc_info=True)
            return []

    def get_all_columns_from_table(self, table_name):
        """Get a list of all column names in the specified table of the Databricks database."""
        logger.info(f"Fetching all column details for table: {table_name}.")
        try:
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }
            with sql.connect(**connection_params) as connection:
                cursor = connection.cursor()

                # SQL query to get all columns from the specified table
                sql_query = f"""
                    SELECT
                        column_name,
                        data_type
                    FROM
                        INFORMATION_SCHEMA.COLUMNS
                    WHERE
                        table_name = '{table_name}'
                """
                cursor.execute(sql_query)
                columns_and_types = cursor.fetchall()

                columns_info = [
                    {
                        "column_name": column,
                        "data_type": data_type,
                        "values_sample": [],  # Initialize with an empty list
                    }
                    for column, data_type in columns_and_types
                ]
                cursor.close()

            return columns_info

        except sql.Error as e:
            logger.error(
                f"Error in connecting to Databricks database: {e}", exc_info=True
            )
            return []
        except Exception as get_column_details_exc:
            logger.error(
                f"Exception occurred while fetching column details: {get_column_details_exc}",
                exc_info=True,
            )
            return []

    def fetch_all_data_from_table(self, table_name):
        """Fetch all data from the specified Databricks table."""
        try:
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }
            with sql.connect(**connection_params) as connection:
                cursor = connection.cursor()
                sql_query = f"SELECT * FROM {table_name}"

                # Execute the SQL query
                cursor.execute(sql_query)

                rows = cursor.fetchall()

                cursor.close()
                print(rows, "ROWS\n" * 100)
                return rows
        except Exception as exc:
            logger.error("Error fetching data from Databricks table: %s", exc)
            return None

    def upload_data_by_chunks(self, table_name, chunk):
        """Bulk upsert a chunk of data into the specified Databricks table."""
        try:
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }
            with sql.connect(**connection_params) as connection:
                cursor = connection.cursor()

                num_columns = len(chunk.columns)

                placeholders = ", ".join(["?" for _ in range(num_columns)])
                sql_query = f"INSERT INTO {table_name} VALUES ({placeholders})"

                values = [tuple(row) for row in chunk.values]

                cursor.executemany(sql_query, values)
                self.fetch_all_data_from_table(table_name)
                connection.commit()  # Explicitly commit the transaction
                logger.info("Chunk uploaded successfully to table: %s", table_name)
                return True
        except Exception as exc:
            logger.error("Error uploading data to Databricks table: %s", exc)
            return False

    def table_exists(self, database_name, table_name):
        try:
            query = f"SHOW TABLES IN {self.catalog_name}.{database_name} LIKE '{table_name}';"
            result, completed = self.execute_query(query)
            return len(result) > 0
        except Exception as e:
            print(f"Error checking if table '{table_name}' exists: {e}")
            return False

    def create_external_master_table(self, table_name, column_definitions, bucket_name):
        try:
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }

            conn = sql.connect(**connection_params)

            if self.table_exists("default", table_name):
                print(
                    f"Table '{self.catalog_name}.default.{table_name}' already exists."
                )
                return True

            column_definitions.append(
                {
                    "key": "created_at_ref",
                    "data_type": "STRING",
                }
            )

            create_table_sql = f"""
            CREATE TABLE {self.catalog_name}.default.{table_name} (
            """

            create_table_sql += ", ".join(
                f"{column['key'].replace('-','_')} {column['data_type']}"
                for column in column_definitions
            )

            create_table_sql += f"""

            )
            USING parquet
            LOCATION 's3://{bucket_name}/{table_name}/'
            """

            result, message = self.execute_query(create_table_sql)
            print(result, "RESTL EXT\n" * 10)

            print(f"Table '{table_name}' created successfully.")
            return result

        except Exception as e:
            print(f"Error creating table '{table_name}': {e}")
            return False

        finally:
            conn.close()

    # TODO: need to change the name of this function to something meaningful
    def create_master_table(self, table_name, ddl):

        try:
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }
            conn = sql.connect(**connection_params)

            result, message = self.execute_query(ddl)
            print(result, "RESTL EXT\n" * 10)

            print(f"Table '{table_name}' created successfully.")
            return result

        except Exception as e:
            print(f"Error creating table '{table_name}': {e}")
            return False

        finally:
            conn.close()

    def map_unified_to_data_mart(
        self, user_id, sql_create_query, sql_drop_query, sql_upsert_query
    ):
        """
        Runs unfieid to data mart.

        Args:
            user_id (str): id of the user who created the tpa
            sql_query (str): sql query to run the join
            transformation_tables_to_check (Array[str]): array of string with l2 table name
            sql_drop_query (str): sql query to drop the l3 table

        Returns:
            result: Query result of the join statement

        """
        try:
            self.execute_query(sql_drop_query)
            result, message = self.execute_query(sql_create_query)
            result, message = self.execute_query(sql_upsert_query)
            print(f"Data mapping from masters to unified table successfully completed.")
            return result

        except Exception as e:
            traceback.print_exc()
            print(f"Error mapping from unified to data mart table: {e}")
            raise Exception(f"Error mapping from unified to data mart table: {e}")

    def create_raw_cogs_external_table(self, user_id, column_definitions, bucket_name):
        """
        Creates an external table in Databricks for raw COGS data.

        Args:
            user_id (str): The user ID.
            column_definitions (list): List of dictionaries containing column definitions.
            bucket_name (str): The name of the S3 bucket.

        Returns:
            bool: True if the table is created successfully, False otherwise.
        """

        try:
            # Extract connection parameters from the field configuration
            connection_params = {
                field.field_name: self.connection_details[field.field_name]
                for field in self.field_config
            }

            # Establish connection to the database
            conn = sql.connect(**connection_params)

            # Generate table name based on user ID
            table_name = f"raw_cogs_data_{user_id}".replace("-", "_").replace("|", "_")

            # Check if the table already exists
            if self.table_exists("business_config", table_name):
                print(
                    f"Table '{self.catalog_name}.business_config.{table_name}' already exists."
                )
                return True

            # Construct SQL query to create the table
            create_table_sql = f"""
            CREATE TABLE {self.catalog_name}.business_config.{table_name} (
            """

            create_table_sql += ", ".join(
                f"{column['key'].replace(' ', '_')} {column['data_type']}"
                for column in column_definitions
            )

            create_table_sql += f"""

            )
            USING csv
            LOCATION 's3://{bucket_name}/{user_id}/cogs/'
            """

            # Execute the SQL query to create the table
            result, message = self.execute_query(create_table_sql)
            print(result, "RESTL EXT\n" * 10)

            print(f"Table '{table_name}' created successfully.")
            return result

        except Exception as e:
            print(f"Error creating table '{table_name}': {e}")
            return False

        finally:
            # Close the database connection
            if conn:
                conn.close()

    def execute_query_with_limit():
        pass

    def execute_query_with_time_filter():
        pass

    def fetch_results_and_save_in_a_file():
        pass

    def get_column_data_types_with_sample_value():
        pass

if __name__ == "__main__":
    # Create an instance of your Databricks class
   

    # Provide your credentials
    params = {
        "server_hostname": os.getenv("DB_HOST_DATABRICKS_SQL"),
        "http_path": os.getenv("DB_HTTP_PATH_DATABRICKS_SQL"),
        "access_token": os.getenv("DB_ACCESS_TOKEN_DATABRICKS_SQL")
    }
    db = Databricks(connection_details=params)

    # Check if the credentials are valid
    if db.has_valid_credentials:
        print("✅ Databricks credentials are valid!")
    else:
        print("❌ Databricks credentials are invalid.")
    print(db.execute_query('select principal from loan_payments '))  # True or False
