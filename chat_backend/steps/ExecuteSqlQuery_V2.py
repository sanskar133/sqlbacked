import logging

from steps.base import Step

logger = logging.getLogger(__name__)


class ExecuteSqlQuery(Step):
    START_MESSAGE = "Executing Sql Query"
    END_MESSAGE = "SQL Query Executed"
    ERROR_MESSAGE = "Error: Executing Sql Query"

    def __init__(self, *args, **kwargs):
        logging.info(f"Initializing step {self}")
        super().__init__(*args, **kwargs)

    def input_keys(self):
        return ["updated_query"]

    def output_keys(self):
        return ["data", "message"]

    def __repr__(self):
        return "ExecuteSqlQuery_V2"

    def __call__(self, updated_queries):
        queries = []
        for updated_query in updated_queries:
            if isinstance(updated_query.get("query_validation_remark"), list):
                queries.append(updated_query)
            elif isinstance(updated_query.get("query_validation_remark"), str):
                if (
                    not updated_query.get("query_validation_remark").startswith(
                        "ERROR: "
                    )
                    or updated_query.get("query_validation_remark") == "COMPLETED"
                ):
                    queries.append(updated_query)
        updated_queries = queries
        del queries

        data_list = []
        message_list = []
        if updated_queries:
            for query in updated_queries:
                try:
                    if query.get("data"):
                        data = query.get("data")
                        message = query.get("query_validation_remark")
                    else:
                        data, message = self.chat_manager.database_object.execute_query(
                            query.get("query_after_regex_match", "")
                        )
                    data_list.append({"data": data})
                    message_list.append(message)
                except Exception as exc:
                    logger.error("Error executing query %s", exc)
                    return {"data": [], "message": [str(exc)]}
        return {"data": data_list, "message": message_list}
