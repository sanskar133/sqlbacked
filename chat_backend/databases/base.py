import logging
import re
from abc import abstractmethod
from dataclasses import dataclass

from pydantic import BaseModel

logger = logging.getLogger(__name__)


@dataclass
class TableColumn:
    def __init__(self, column_name, column_default, data_type, description=None):
        self.column_name = column_name
        self.column_default = column_default
        self.data_type = data_type
        self.description = description


@dataclass
class Table:
    def __init__(self, table_name, description=None):
        self.table_name = table_name
        self.columns = []
        self.description = description


@dataclass
class TableCatalog:
    def __init__(self, table_catalog):
        self.table_catalog = table_catalog
        self.tables = []


class DatabaseFields(BaseModel):
    field_name: str = "field_name"
    display_name: str = "display_name"
    description: str = None
    type: str = "str"
    required: bool = True
    default: str = None

    def to_dict(self) -> dict:
        "Function which converts the DataFields base details to dict"
        return {
            "field_name": self.field_name,
            "display_name": self.display_name,
            "description": self.description,
            "type": self.type,
            "required": self.required,
            "default": self.default,
        }


class Database(BaseModel):
    connection_type: str = "database"
    display_name: str = "str"
    description: str = "str"

    @property
    def field_config(self) -> list[DatabaseFields]:
        raise NotImplementedError("This property is not implemented yet.")

    @property
    def has_valid_credentials(self) -> bool:
        raise NotImplementedError("This property is not implemented yet.")

    @property
    def database_schema(self):
        raise NotImplementedError("This property is not implemented yet.")

    def to_dict(self) -> dict:
        "Function which converts the Data base details to dict"
        return {
            "display_name": self.display_name,
            "description": self.description,
            "field_config": [field.to_dict() for field in self.field_config],
        }

    def get_structured_schema(self, table_schema: list[tuple]):
        table_catalogs = []

        for row in table_schema:
            if (not table_catalogs) or (table_catalogs[-1].table_catalog != row[0]):
                table_catalogs.append(TableCatalog(row[0]))
            if (not table_catalogs[-1].tables) or (
                table_catalogs[-1].tables[-1].table_name != row[1]
            ):
                table_catalogs[-1].tables.append(Table(row[1]))
            table_catalogs[-1].tables[-1].columns.append(TableColumn(*row[2:]))

        schema_format = """"""
        for table_catalog in table_catalogs:
            schema_format += f"table_catalog: {table_catalog.table_catalog}\n"
            for table in table_catalog.tables:
                schema_format += f"\ttable_name: {table.table_name}\n"
                for column in table.columns:
                    schema_format += f"\t\tcolumn_name: {column.column_name}, column_default: {column.column_default}, data_type: {column.data_type}\n"

        return schema_format

    def get_structured_schema_from_description_objects(
        self, unstructured_schema: tuple[list]
    ):
        """Create structured schema for FetchQueryContext used with vectordb"""
        tables, columns, queries = unstructured_schema

        schema = """"""

        for table, column in zip(tables, columns):
            schema += f"table_name: {table[0].get('name')}, table_description: {table[0].get('description')}\n"

            for col in column:
                schema += f"\t\tcolumn_name: {col.get('name')}, column_description: {col.get('description')}, column_sample_values: {col.get('values_sample')}\n"

            schema += "\n"

        if queries:
            schema += f"\nSample Queries from this database:\n"
            for q in queries:
                schema += f"\t\tsample_question: {q.get('question')}, response: {q.get('response')}, description: {q.get('description')}\n"

        return schema.strip()

    def _validate_query(self, query: str):
        """Return true when we have only select query.
        else return false
        """
        if query.lower().startswith("select"):
            return True
        elif re.sub(
            r"^(with (.+) as (\(select .*\),?)+) select",
            query.lower().replace("\n", ""),
            "select",
        ).startswith("select"):
            return True
        else:
            return False

    @abstractmethod
    def get_engine(self):
        "get engine for the database"
        raise NotImplementedError("This property is not implemented yet.")

    @abstractmethod
    def execute_query(self, query: str, validate: bool = True):
        """execute database queries"""
        raise NotImplementedError("This property is not implemented yet.")

    @abstractmethod
    def get_all_table_names(self):
        """execute database queries to get all the tables"""
        raise NotImplementedError("This property is not implemented yet.")

    @abstractmethod
    def get_all_columns_from_table(self, table_name: str):
        """execute database queries to all columns in a table"""
        raise NotImplementedError("This property is not implemented yet.")

    @abstractmethod
    def get_column_data_types_with_sample_value(self, query, validate: bool = True):
        """get column datatypes with sample values"""
        raise NotImplementedError("This property is not implemented yet.")

    @abstractmethod
    def execute_query_with_limit(self, query, limit):
        """execute the given query with a limit"""
        raise NotImplementedError("This property is not implemented yet.")

    @abstractmethod
    def execute_query_with_time_filter(self, query, column_name, from_date, to_date):
        """execute the query with time filter"""
        raise NotImplementedError("This property is not implemented yet.")

    @abstractmethod
    def fetch_results_and_save_in_a_file(self, query, data_model_id):
        """fetch the results from the db based on the query and then store the data in a csv"""
        raise NotImplementedError("This property is not implemented yet.")

    def explain_query(self, query: str):
        """add explain in final sql query to check if the the SQL query has proper table and coloumn names"""
        _explain_query = f"EXPLAIN {query}"
        result, message = self.execute_query(_explain_query, validate=False)
        logger.info("Result of Explain Query: %s", result)
        if result:
            return result
        else:
            return f"ERROR: {message}"
