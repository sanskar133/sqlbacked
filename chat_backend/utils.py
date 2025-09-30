import importlib.util
import logging

logger = logging.getLogger(__name__)


def import_class_by_file_and_class_name(file, class_name):
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


def get_past_conversation_pair_from_query_response_data(query_responses) -> list[tuple]:
    """
    1. Takes a list of query responses dict.
    2. Get the key from specific step data.
    3. Build pairs and return
    """

    past_conversation_pairs = []

    for query_response in query_responses:
        try:
            query_meta_data = (
                query_response["query_meta_data"]
                if "query_meta_data" in query_response
                else None
            )
            if query_meta_data is None:
                continue

            query_step_data = (
                query_meta_data["step_data"] if "step_data" in query_meta_data else None
            )

            if query_step_data is None or query_step_data == {}:
                continue

            response = get_step_output_given_query_response_rows(
                query_step_data,
                step_name="ValidateGeneratedSqlQuery",
                key_name="final_updated_query",
            )

            user_query, response = query_response["user_query"], response

            if response is None:
                continue

            past_conversation_pairs.append((user_query, response))

        except Exception as exc:
            logger.error(exc, exc_info=True)

    return past_conversation_pairs


def get_step_output_given_query_response_rows(step_data, step_name: str, key_name: str):
    """
    Functional logic for extracting output of given step name and key name
    """

    try:
        for step in step_data:
            if step["display_name"] == step_name:
                _step_data = step["data"] if "data" in step else None

                if _step_data is None:
                    return None

                if key_name in _step_data:
                    return _step_data[key_name]

        return None
    except Exception as exc:
        logger.error(exc, exc_info=True)
        return None
