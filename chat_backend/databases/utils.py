import importlib.util
import logging
import os

from databases.base import Database

logger = logging.getLogger(__name__)
DATABASE_FILES_DIRECTORY = os.path.dirname(__file__)


def list_all_database_options() -> dict:
    """
    Retrieves options for all database classes in the specified directory.

    Returns:
    dict: A dictionary containing class names as keys and their corresponding options
          obtained by calling the 'to_dict()' method of each class instance.
          The structure of the dictionary is {class_name: options}.
    """

    try:
        database_options_dict = {}

        database_files = get_all_files_from_databases_folder()

        for file in database_files:
            try:
                databae_class_name = os.path.splitext(file)[0]
                database_class = import_class_by_file_and_class_name(
                    os.path.join(DATABASE_FILES_DIRECTORY, file), databae_class_name
                )
                database_options_dict[databae_class_name] = database_class().to_dict()
            except Exception as exc:
                logger.error(
                    f"Erro importing class {databae_class_name}", exc_info=True
                )
        logger.info(database_options_dict)
    except Exception as exc:
        logger.error(str(exc), exc_info=True)

        return {}

    return database_options_dict


def get_all_files_from_databases_folder() -> list:
    """
    Get a list of all files from the database folder, excluding specific files.

    Returns:
    list: A list of file names in the database folder, excluding files specified
          in the 'FILES_TO_EXCLUDE' constant.
    """

    FILES_TO_EXCLUDE = ["utils", "base"]
    all_files = [
        file
        for file in os.listdir(DATABASE_FILES_DIRECTORY)
        if os.path.isfile(os.path.join(DATABASE_FILES_DIRECTORY, file))
    ]
    filtered_files = [
        file
        for file in all_files
        if all(substring not in file for substring in FILES_TO_EXCLUDE)
    ]
    logger.info(filtered_files)

    return filtered_files


def import_class_by_file_and_class_name(file, class_name) -> Database:
    """
    Dynamically Imports The Class Given the file and class name

    Args:
    - file (str): The file path (including the file name) without the '.py' extension.
    - class_name (str): The name of the class to be imported.

    Returns:
    - class: The imported class.
    """
    module = load_module_given_file_path(file)
    if module:
        try:
            imported_class = getattr(module, class_name)
            return imported_class
        except AttributeError:
            raise ImportError(f"Class '{class_name}' not found in module '{file}'")
    else:
        raise ImportError(f"Module '{file}' not found")


def load_module_given_file_path(file):
    """
    Load the module given the file path

    Args:
    - file (str): The file path (including the file name) without the '.py' extension.

    Returns:
    - module: The loaded module.
    """
    spec = importlib.util.spec_from_file_location(file, f"{file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_if_database_credentials_are_valid(database_name, connection_details):
    try:
        logger.info(
            f"Checking if database credentials are valid for Database {database_name}"
        )
        database_class = import_class_by_file_and_class_name(
            os.path.join(DATABASE_FILES_DIRECTORY, f"{database_name.capitalize()}.py"),
            database_name.capitalize(),
        )
        return database_class(
            connection_details=connection_details
        ).has_valid_credentials
    except Exception as exc:
        logger.error(exc, exc_info=True)
        raise Exception(exc)


def get_database_object(database_name, connection_details, connection_type="STANDARD"):
    try:
        logger.info(f"Checking Get Database Object {database_name}")
        database_class = import_class_by_file_and_class_name(
            os.path.join(DATABASE_FILES_DIRECTORY, f"{database_name.capitalize()}.py"),
            database_name.capitalize(),
        )
        if connection_type == "STANDARD":
            return database_class(connection_details=connection_details)
        else:
            return database_class(
                connection_details=connection_details, connection_type=connection_type
            )
    except Exception as exc:
        logger.error(exc, exc_info=True)
        raise Exception(exc)


def get_database_tables(database_name, connection_details):
    try:
        logger.info(f"Fetching all table names for Database {database_name}")
        database_class = import_class_by_file_and_class_name(
            os.path.join(DATABASE_FILES_DIRECTORY, f"{database_name.capitalize()}.py"),
            database_name.capitalize(),
        )
        database_instance = database_class(connection_details=connection_details)
        return database_instance.get_all_table_names()

    except Exception as exc:
        logger.error(exc, exc_info=True)
        raise Exception(exc)


def get_columns_from_table(database_name, connection_details, table_name):
    try:
        logger.info(f"Fetching all table names for Database {database_name}")
        database_class = import_class_by_file_and_class_name(
            os.path.join(DATABASE_FILES_DIRECTORY, f"{database_name.capitalize()}.py"),
            database_name.capitalize(),
        )
        database_instance = database_class(connection_details=connection_details)
        return database_instance.get_all_columns_from_table(table_name)
    except Exception as exc:
        logger.error(exc, exc_info=True)
        raise Exception(exc)
