from databases.base import Database
from databases.base import Database, DatabaseFields
import logging
from databricks import sql
from typing import Any
import os
from dotenv import load_dotenv
load_dotenv()  # loads .env file

logger = logging.getLogger(__name__)


class Databricks(Database):
    connection_params: dict

    display_name: str = "Databricks SQL"
    description: str = "Connect to your Databricks SQL Warehouse"

    # You can also store the engine
    database_engine: Any = None
    
    @property
    def field_config(self) -> list[DatabaseFields]:
        return [
            DatabaseFields(
                field_name="host",
                display_name="Host",
                description="The hostname of the Databricks SQL endpoint.",
                type="str",
                required=True,
            ),
            DatabaseFields(
                field_name="http_path",
                display_name="HTTP Path",
                description="The HTTP path to the Databricks SQL warehouse.",
                type="str",
                required=True,
            ),
            DatabaseFields(
                field_name="access_token",
                display_name="Access Token",
                description="The access token for authenticating with Databricks SQL.",
                type="str",
                required=True,
            ),
        ]

    @property
    def has_valid_credentials(self) -> bool:
        try:
            logger.info("Validating Databricks SQL credentials...")
            with self.get_connect() as conn:

                with conn.cursor() as cursor:
                    # Simple test query (lightweight)
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    print(result)
                    logger.info(f"Validation query result: {result}")
                    return result[0] == 1
        except Exception as e:
            logger.error("Failed to validate Databricks credentials", exc_info=True)
            return False
        return True

    @property
    def database_schema(self):
        # Implement logic to fetch and return the database schema
        catalog_name = self.connection_params.get("catalog", "workspace")  # default catalog
         # default schema
        """Get Schema of the Databricks Schema"""
        logger.info("Fetching Database schema.")
        logger.info(f"Catalog name2: {catalog_name}")
        try:
            connection_params = {
                field.field_name: self.connection_params[field.field_name]
                for field in self.field_config
            }
            schema = self.connection_params.get("schema", "default")
            print(connection_params)

            with sql.connect(server_hostname=self.connection_params["host"],http_path=self.connection_params["http_path"],access_token=self.connection_params["access_token"])as connection:
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
            print(data)
            return data
        except sql.Error:
            logger.error("Error in connecting Databricks Database", exc_info=True)
            return False
        except Exception as database_schema_exc:
            logger.error(database_schema_exc, exc_info=True)

    def get_connect(self):
        """
        Central method to get a Databricks connection.
        Use it with a context manager: `with db.get_connect() as conn:`
        """
        try:
            conn = sql.connect(server_hostname=self.connection_params["host"],http_path=self.connection_params["http_path"],
                access_token=self.connection_params["access_token"])
            return conn
        except Exception as e:
            logger.error("Failed to connect to Databricks", exc_info=True)
            raise
        

    def execute_query(self, query: str,validate: bool = True):
        """execute the given query and return the results"""
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
       
    def get_engine(self):
        # Implement logic to return a SQLAlchemy engine if needed
        logger.info("Get Engine for Databricks")
        try:
            connection_params = {
                field.field_name: self.connection_params[field.field_name]
                for field in self.field_config
            }
            print(connection_params)
            self.database_engine =  sql.connect(server_hostname= connection_params["host"],http_path= connection_params["http_path"],
                access_token= connection_params["access_token"])
            return True
        except sql.Error:
            logger.error("Error in connecting Databricks Database", exc_info=True)
            return False
        except Exception as exc:
            logger.error(exc, exc_info=True)
        
    def get_all_table_names(self):
        with self.get_connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
        
            tables = cursor.fetchall()
        
            table_names = [table[1] for table in tables]
            print(table_names)  # Assuming the second column is the table name
            return table_names
        
        
    def get_all_columns_from_table(self, table_name: str):
        with self.get_connect() as conn:
            cursor = conn.cursor()
            query =  f"""
                    SELECT
                        column_name,
                        data_type
                    FROM
                        INFORMATION_SCHEMA.COLUMNS
                    WHERE
                        table_name = '{table_name}'
                """
            cursor.execute(query)
            columns = cursor.fetchall()
            print(columns)  # Assuming the second column is the table name

        """execute database queries to all columns in a table"""
        raise NotImplementedError("This property is not implemented yet.")
    def get_column_data_types_with_sample_value(self, query, validate: bool = True):
        """get column datatypes with sample values"""
        raise NotImplementedError("This property is not implemented yet.")

    def get_column_data_types_with_sample_value(self, query, validate: bool = True):
        """get column datatypes with sample values"""
        raise NotImplementedError("This property is not implemented yet.")
    
    def execute_query_with_limit(self, query, limit):
        """execute the given query with a limit"""
        raise NotImplementedError("This property is not implemented yet.")
    

    def execute_query_with_time_filter(self, query, column_name, from_date, to_date):
        """execute the query with time filter"""
        raise NotImplementedError("This property is not implemented yet.")
    
    
    def fetch_results_and_save_in_a_file(self, query, data_model_id):
        """fetch the results from the db based on the query and then store the data in a csv"""
        raise NotImplementedError("This property is not implemented yet.")


    
    
if __name__ == "__main__":
    params = {
        "host": os.getenv("DB_HOST_DATABRICKS_SQL"),
        "http_path": os.getenv("DB_HTTP_PATH_DATABRICKS_SQL"),
        "access_token": os.getenv("DB_ACCESS_TOKEN_DATABRICKS_SQL")
    }

    db = DatabricksSQL(connection_params=params)

    print(db.database_schema)  # True or False

    


    print(db.has_valid_credentials)  # True or False