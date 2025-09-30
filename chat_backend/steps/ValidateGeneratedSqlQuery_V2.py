import json
import logging
import re

from engine.llms.opena_ai_fix_sql_query_error import OpenAIFixSQLQueryError
from steps.base import Step

logger = logging.getLogger(__name__)


class ValidateGeneratedSqlQuery(Step):
    START_MESSAGE = "Validating Generated SQL Query"
    END_MESSAGE = "Generated SQL Query Validated"
    ERROR_MESSAGE = "Error: Validating Generated SQL Query"

    def __init__(self, *args, **kwargs):
        logging.info(f"Initializing step {self}")
        super().__init__(*args, **kwargs)

        self.llm_sql_query_fixer = OpenAIFixSQLQueryError()

    def input_keys(self):
        return ["updated_query"]

    def output_keys(self):
        return ["query_validation_remark", "proceed"]

    def __repr__(self):
        return "ValidateGeneratedSqlQuery_V2"

    def extract_sql_using_regex(self, text):
        regex = r"SELECT.*?;"
        match = re.search(regex, text, re.DOTALL)
        if match:
            return match.group()
        else:
            return text

    def __call__(self, question, database_schema, updated_queries):
        validated_queries = []
        for updated_query in updated_queries:
            data = []
            fixed_query = updated_query.get("sql_query")
            # query_after_regex_match = self.extract_sql_using_regex(fixed_query)
            query_after_regex_match = fixed_query

            # TODO: add explain query for Mssql
            if self.chat_manager.database_object.display_name in ["Ibm_i_db2", "Sqlite3"]:
                (
                    data,
                    query_validation_remark,
                ) = self.chat_manager.database_object.execute_query(
                    query_after_regex_match
                )
            elif self.chat_manager.database_object.display_name not in ["Mssql"]:
                query_validation_remark = (
                    self.chat_manager.database_object.explain_query(
                        query_after_regex_match
                    )
                )
            else:
                query_validation_remark = [{"plan": "go ahead"}]

            logger.info(
                "\n\n##################query_validation_remark: %s###############\n\n",
                query_validation_remark,
            )
            # logger.info("\n\ntype: %s###############\n\n", type(query_validation_remark))
            n_attempt = 0
            total_attempts = 4

            while (
                (
                    isinstance(query_validation_remark, list)
                    and query_validation_remark[0]["plan"].startswith("Error")
                )
                or (
                    isinstance(query_validation_remark, str)
                    and query_validation_remark.startswith("ERROR: ")
                )
                and n_attempt < total_attempts
            ):
                n_attempt += 1

                logger.info(
                    "\n\n##################loop_query_validation_remark: %s###############\n\n",
                    query_validation_remark,
                )

                fixed_query_llm_result = self.llm_sql_query_fixer.generate(
                    question,
                    database_schema,
                    query_after_regex_match,
                    (
                        query_validation_remark[1]["plan"]
                        if not isinstance(query_validation_remark, str)
                        else query_validation_remark
                    ),
                    query_id=self.query_id,
                    database_type=self.chat_manager.database_object.display_name,
                )
                fixed_query = fixed_query_llm_result["choices"][0]["message"]["content"]
                fixed_query = json.loads(fixed_query).get("sql_query")
                query_after_regex_match = fixed_query
                if self.chat_manager.database_object.display_name in ["Ibm_i_db2", "Sqlite3"]:
                    (
                        data,
                        query_validation_remark,
                    ) = self.chat_manager.database_object.execute_query(
                        query_after_regex_match
                    )
                else:
                    query_validation_remark = (
                        self.chat_manager.database_object.explain_query(
                            query_after_regex_match
                        )
                    )
            validated_queries.append(
                {
                    "data": data,
                    "fixed_query": fixed_query,
                    "query_after_regex_match": query_after_regex_match,
                    "query_validation_remark": (
                        query_validation_remark[0]["plan"]
                        if not isinstance(query_validation_remark, str)
                        else query_validation_remark
                    ),
                    "no_attempts": n_attempt,
                }
            )
        # print(validated_queries)
        if all(
            [
                (
                    validated_query.get("query_validation_remark").startswith("Error")
                    if isinstance(validated_query.get("query_validation_remark"), str)
                    else False
                )
                for validated_query in validated_queries
            ]
        ):
            proceed = False
        else:
            proceed = True

        return {
            "proceed": proceed,
            "validated_queries": validated_queries,
        }
