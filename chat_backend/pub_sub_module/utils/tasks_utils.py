from datetime import datetime, timedelta
import traceback
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pub_sub_module.cloud_storage.base_uploader_factory import (
    CloudStorageUploaderFactory,
)

from kpi_analytics.base.data_models import BaseDataModel
from io import BytesIO
from database_connection_management.databases import utils as database_utils
import os
import json


def get_sample_value_of_time_columns(columns, time_column):
    for column in columns:
        if column["key"] == time_column:
            return column["sample_value"]


def check_date_format(date_string):
    print(date_string)
    date_formats = [
        "%d-%m-%y",
        "%d-%m-%Y",
        "%d/%m/%y",
        "%d/%m/%Y",
        "%m-%d-%y",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%y-%m-%d",
        "%y/%m/%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %I:%M %p",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d %I:%M %p",
        "%d-%b-%Y",
        "%d-%b-%y",
        "%d %b %Y",
        "%d %b %y",
        "%d %B %Y",
        "%d %B %y",
    ]

    for date_format in date_formats:
        try:
            datetime.strptime(date_string, date_format)
            return date_format
        except ValueError:
            print("error")

    return None


def get_last_sync_date_for_last_2_months_or_last_day(date_format, last_sync_date):
    """
    Calculate the start and end dates based on the last synchronization date.

    Args:
    - date_format (str): The format for the date strings.
    - last_sync_date (str or None): The last synchronization date in the format specified by date_format.
                                    If None, default to 2 months ago.

    Returns:
    - tuple: A tuple containing the start and end dates in the specified date_format.
    """

    if last_sync_date is None:
        last_sync_date = datetime.now() - timedelta(days=60)
        time_filter_start = (datetime.now() - timedelta(days=1)).strftime(date_format)
        time_filter_end = last_sync_date.strftime(date_format)
        print(time_filter_start, time_filter_end)
        return time_filter_start, time_filter_end
    else:
        last_sync_date = datetime.strptime(last_sync_date, "%d-%m-%y")
        time_filter_start = (datetime.now() - timedelta(days=1)).strftime(date_format)
        time_filter_end = last_sync_date.strftime(date_format)
        return time_filter_end, time_filter_start


def get_data_bricks_connection_object():
    database_object = database_utils.get_database_object(
        "DataBricks",
        {
            "server_hostname": os.getenv("DATABRICKS_SERVER_HOST"),
            "http_path": os.getenv("DATABRICKS_HTTP_PATH"),
            "access_token": os.getenv("DATABRICKS_ACCESS_TOKEN"),
        },
    )
    return database_object


def create_master_databricks_table_if_not_exists(
    table_name, columns, cloud_provider="s3"
):
    cloud_uploader = CloudStorageUploaderFactory.create_uploader(cloud_provider)
    cloud_uploader.create_folder(table_name)
    cloud_credentials = cloud_uploader.get_client_object()
    database_object = get_data_bricks_connection_object()
    table_nm = database_object.create_external_master_table(
        table_name, columns, cloud_credentials.get("bucket_name")
    )
    return table_nm


def process_csv_chunks_and_save_to_cloud(
    file_name, table_name, chunk_size=10000, cloud_provider="s3"
):
    cloud_uploader = CloudStorageUploaderFactory.create_uploader(cloud_provider)
    try:
        while True:
            df_chunk = pd.read_csv(file_name, chunksize=(chunk_size))
            chunk = df_chunk.get_chunk()
            if chunk.empty or chunk is None:
                if os.path.exists(file_name):
                    os.remove(file_name)
                break

            chunk["created_at_ref"] = datetime.now().strftime("%Y-%m-%d")

            csv_string = chunk.to_csv(index=False)
            csv_bytes = csv_string.encode()
            csv_path = cloud_uploader.upload_file(csv_bytes, table_name)
            if csv_path:
                remove_processed_chunk_from_csv(file_name, chunk)
                # time.sleep(2)

    except Exception as e:
        print(f"Error processing CSV file: {e}")


def remove_processed_chunk_from_csv(file_name, chunk):
    df = pd.read_csv(file_name)
    chunk_indices = chunk.index.tolist()
    df.drop(chunk_indices, inplace=True)
    df.to_csv(file_name, index=False)
    print("Processed chunk removed from CSV file successfully.")


def map_source_data_types_to_databricks_data_types(columns):
    """
    Map PostgreSQL data types to Databricks data types.

    Args:
        columns (list): List of dictionaries representing columns, where each dictionary contains a 'data_type' key.

    Returns:
        list: List of dictionaries with updated 'data_type' values mapped to Databricks data types.
    """

    data_type_mapping = {
        "bigint": "LONG",
        "bigserial": "LONG",
        "bit": "BOOLEAN",
        "bit varying": "STRING",
        "boolean": "BOOLEAN",
        "box": "STRING",
        "bytea": "BINARY",
        "character": "STRING",
        "character varying": "STRING",
        "cidr": "STRING",
        "circle": "STRING",
        "date": "DATE",
        "double precision": "DOUBLE",
        "inet": "STRING",
        "integer": "INTEGER",
        "interval": "STRING",
        "json": "STRING",
        "jsonb": "STRING",
        "line": "STRING",
        "lseg": "STRING",
        "macaddr": "STRING",
        "money": "DOUBLE",
        "numeric": "DECIMAL",
        "path": "STRING",
        "pg_lsn": "STRING",
        "point": "STRING",
        "polygon": "STRING",
        "real": "FLOAT",
        "smallint": "INTEGER",
        "smallserial": "INTEGER",
        "serial": "INTEGER",
        "text": "STRING",
        "time": "STRING",
        "time with time zone": "TIMESTAMP",
        "timestamp": "TIMESTAMP",
        "timestamp with time zone": "TIMESTAMP",
        "tsquery": "STRING",
        "tsvector": "STRING",
        "txid_snapshot": "STRING",
        "uuid": "STRING",
        "xml": "STRING",
        16: "BOOLEAN",
        23: "INTEGER",
        1082: "DATE",
        1114: "TIMESTAMP",
        1043: "STRING",
        700: "FLOAT",
        701: "DOUBLE",
    }

    for column in columns:
        if isinstance(column["data_type"], int):
            column["data_type"] = data_type_mapping.get(
                column["data_type"], column["data_type"]
            )
        else:
            column["data_type"] = data_type_mapping.get(
                column["data_type"].lower(), column["data_type"]
            )

    return columns


def extract_data_model_values(data_model):
    """
    Extracts values from the data_model dictionary.

    Args:
    - data_model (dict): The data_model dictionary.

    Returns:
    - tuple: A tuple containing the extracted values.
    """

    meta_data = data_model.get("meta", {})
    query = data_model.get("sql_query", "")
    time_column = meta_data.get("time_column", None)
    time_format = meta_data.get("time_format", None)
    primary_key_column = meta_data.get("primary_key_column", None)
    columns_with_data_type_and_sample_values = meta_data.get("columns", None)
    last_sync_date = meta_data.get("last_sync_date", None)

    return (
        query,
        time_column,
        time_format,
        last_sync_date,
        primary_key_column,
        columns_with_data_type_and_sample_values,
    )


def map_parquet_data_types_to_databricks(parquet_column_data_types):
    """
    Map Parquet data types to Databricks data types.

    Args:
        existing_columns_with_data_type (list of dict): List of dictionaries containing existing column names, data types, and sample values.
        parquet_column_data_types (list of dict): List of dictionaries containing Parquet column names and their corresponding data types.

    Returns:
        list of dict: List of dictionaries with updated data type mappings to Databricks data types.
    """

    parquet_databricks_mapping = {
        "string": "STRING",
        "int8": "TINYINT",
        "int16": "SMALLINT",
        "int32": "INT",
        "int64": "BIGINT",
        "uint8": "BYTE",
        "uint16": "SHORT",
        "uint32": "INT",
        "uint64": "LONG",
        "float16": "FLOAT",
        "float32": "FLOAT",
        "float64": "DOUBLE",
        "binary": "BINARY",
        "bool": "BOOLEAN",
        "double": "DOUBLE",
        "date32": "DATE",
        "date64": "TIMESTAMP",
        "timestamp": "TIMESTAMP",
        "UNKNOWN": "STRING",
    }

    for parquet_column in parquet_column_data_types:
        databricks_type = parquet_databricks_mapping.get(
            parquet_column.get("data_type"), "STRING"
        )
        parquet_column["data_type"] = databricks_type

    return parquet_column_data_types


def get_parquet_data_types_from_saved_csv_file(csv_file):
    df = pd.read_csv(csv_file, nrows=100000)

    for column in df.columns:
        if df[column].dtype == "object":
            df[column] = df[column].astype("string")

    sample_values = {}
    for column in df.columns:
        non_null_values = df[column].dropna().head(5).tolist()
        if len(non_null_values) == 0:
            print(f"replacing by null string for colums {column}")
            df[column].fillna("null", inplace=True)
        if len(non_null_values) < 5:
            non_null_values += ["null"] * (5 - len(non_null_values))

        sample_values[column] = non_null_values

    table = pa.Table.from_pandas(df)
    schema = table.schema
    parquet_column_data_types = []
    for field in schema:
        key = field.name
        _sample_values = sample_values[field.name]
        data_type = str(field.type)
        if "phone" in key.lower():
            data_type = "string"

        if len(_sample_values) == 0:
            data_type = "string"

        print(f"Sample valyes for field {key} and datatype {data_type}", _sample_values)
        parquet_column_data_types.append(
            {
                "key": key,
                "data_type": data_type,
                "sample_values": _sample_values,
            }
        )

    print("parquet columns data types", parquet_column_data_types)
    databricks_data_types = map_parquet_data_types_to_databricks(
        parquet_column_data_types
    )

    return databricks_data_types


# Need to extract the repeated code
def process_parquet_chunks_and_save_to_cloud(
    file_name,
    table_name,
    parquet_column_data_types,
    chunk_size=50000,
    cloud_provider="s3",
):
    cloud_uploader = CloudStorageUploaderFactory.create_uploader(cloud_provider)
    try:

        if not os.path.exists(file_name):
            raise FileNotFoundError(f"File not found: {file_name}")

        while True:
            df_chunk = pd.read_csv(file_name, chunksize=(chunk_size))
            chunk = df_chunk.get_chunk()
            if chunk.empty or chunk is None:
                if os.path.exists(file_name):
                    os.remove(file_name)
                break

            chunk["created_at_ref"] = str(datetime.now().strftime("%Y-%m-%d"))

            chunk = cast_columns_to_correct_datatype(chunk, parquet_column_data_types)

            buffer = BytesIO()
            chunk.to_parquet(buffer, compression="snappy", index=False)

            parquet_bytes = buffer.getvalue()
            parquet_path = cloud_uploader.upload_file(parquet_bytes, table_name)

            if parquet_path:
                remove_processed_chunk_from_csv(file_name, chunk)
                # time.sleep(2)

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise Exception(e)

        print(f"Error processing CSV file: {e}")


def process_parquet_chunks_and_save_to_cloud_v2(
    file_name,
    table_name,
    parquet_column_data_types,
    chunk_size=50000,
    cloud_provider="s3",
):
    cloud_uploader = CloudStorageUploaderFactory.create_uploader(cloud_provider)
    try:

        if not os.path.exists(file_name):
            raise FileNotFoundError(f"File not found: {file_name}")

        while True:
            df_chunk = pd.read_csv(file_name, chunksize=(chunk_size), dtype=str)
            chunk = df_chunk.get_chunk()
            if chunk.empty or chunk is None:
                if os.path.exists(file_name):
                    os.remove(file_name)
                break

            chunk["created_at_ref"] = str(datetime.now().strftime("%Y-%m-%d"))

            chunk = cast_columns_to_correct_datatype(chunk, parquet_column_data_types)

            buffer = BytesIO()
            chunk.to_parquet(buffer, compression="snappy", index=False)

            parquet_bytes = buffer.getvalue()
            parquet_path = cloud_uploader.upload_file(parquet_bytes, table_name)

            if parquet_path:
                remove_processed_chunk_from_csv(file_name, chunk)
                # time.sleep(2)

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise Exception(e)

        print(f"Error processing CSV file: {e}")


def cast_columns_to_correct_datatype(chunk, parquet_column_data_types):
    """
    Create a dynamic PyArrow schema based on column information.

    Args:
        parquet_column_data_types (list of dict): List of dictionaries containing Parquet column names and their corresponding data types.

    Returns:
        pyarrow.Schema: A PyArrow schema object based on the provided column information.
    """

    fields = []
    for column_info in parquet_column_data_types:
        # print(column_info, " INFO")
        column_name = column_info["key"]
        databricks_data_type = column_info["data_type"]

        arrow_data_type = None
        if databricks_data_type == "STRING":
            arrow_data_type = "string"
        elif databricks_data_type == "TINYINT":
            arrow_data_type = "Int8"
        elif databricks_data_type == "SMALLINT":
            arrow_data_type = "Int16"
        elif databricks_data_type == "INT":
            arrow_data_type = "Int32"
        elif databricks_data_type == "BIGINT":
            arrow_data_type = "Int64"
        elif databricks_data_type == "BYTE":
            arrow_data_type = "UInt8"
        elif databricks_data_type == "SHORT":
            arrow_data_type = "UInt16"
        elif databricks_data_type == "LONG":
            arrow_data_type = "UInt64"
        elif databricks_data_type == "FLOAT":
            arrow_data_type = "float32"
        elif databricks_data_type == "DOUBLE":
            arrow_data_type = "float64"
        elif databricks_data_type == "BINARY":
            arrow_data_type = "boolean"
        elif databricks_data_type == "BOOLEAN":
            arrow_data_type = "boolean"
        elif databricks_data_type == "DATE":
            arrow_data_type = None
        elif databricks_data_type == "TIMESTAMP":
            arrow_data_type = None

        if arrow_data_type:
            chunk[column_name] = chunk[column_name].astype(arrow_data_type)

    return chunk


def compare_objects(dict1, dict2):
    """
    Compare two dictionaries based on the data_type of keys.

    Args:
    - dict1 (dict): First dictionary to compare.
    - dict2 (dict): Second dictionary to compare.

    Returns:
    - list: List of keys where data_types differ.
    """
    differing_keys = []

    for key in dict1:
        if key in dict2:
            data_type1 = dict1[key].get("data_type")
            data_type2 = dict2[key].get("data_type")
            if data_type1 != data_type2:
                differing_keys.append(key)

    print(differing_keys, "DLDLD\n\n" * 10)
    return differing_keys


def upload_raw_data_to_cloud(raw_data, cloud_provider="s3"):
    """Input: raw_data with key as the file name and value as dictionary"""

    cloud_uploader = CloudStorageUploaderFactory.create_uploader(cloud_provider)
    cloud_uploader.bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME_JSON")
    for file_name, data in raw_data.items():
        json_data = json.dumps(data)
        file_name = cloud_uploader.upload_file_general(
            json_data.encode(), file_name, "application/json"
        )
        print("file uploaded: ", file_name)


def create_base_data_model_instance(data_model_details, database_name):
    """
    Creates an instance of the base data model with provided details.
    Args:
    - data_model_details (dict): A dictionary containing details of the data model.
    - database_name (str): The name of the database associated with the data model.
    """
    base_data_model = BaseDataModel
    base_data_model.data_model_details = data_model_details
    base_data_model.database_name = database_name
    base_data_model = base_data_model()
    return base_data_model


def flatten_business_config_dict_to_table(data):
    """
    This function flattens the business expense meta from the local DB and will make the correct structure required for business expense master table in databricks
    Args (data): Meta of business expense model
    """
    result = []

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def flatten(data):
        for key, value in data.items():
            if isinstance(value, dict):
                if key == "online_payments":
                    for sub_key, sub_value in value.items():
                        if (
                            isinstance(sub_value, dict)
                            and "type" in sub_value
                            and sub_value["type"] == "percent"
                        ):
                            result.append(
                                {
                                    "expense_type": "transaction",
                                    "expense_source": sub_key,
                                    "is_percent": sub_value.get("type", None)
                                    == "percent",
                                    "percent_of": sub_value.get("percent_of", None),
                                    "value": sub_value.get("value", 0.0),
                                    "synced_at": current_datetime,
                                }
                            )
                elif key == "cod":
                    if "type" in value and value["type"] == "percent":
                        result.append(
                            {
                                "expense_type": "transaction",
                                "expense_source": value.get("display_name", None),
                                "is_percent": value.get("type", None) == "percent",
                                "percent_of": value.get("percent_of", None),
                                "value": value.get("value", 0.0),
                                "synced_at": current_datetime,
                            }
                        )
                elif key in ["packaging", "shipping"]:
                    result.append(
                        {
                            "expense_type": key,
                            "expense_source": None,
                            "is_percent": value.get("type", None) == "percent",
                            "percent_of": value.get("percent_of"),
                            "value": value.get("value", 0.0),
                            "synced_at": current_datetime,
                        }
                    )
                else:
                    flatten(value)
            elif isinstance(value, list):
                flatten(value, expense_type=key)

    flatten(data)
    return result
