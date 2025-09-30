import gc
import json
import logging

from chat_manager.base import ChatManager
from custom_exceptions.ProceedFalseException import ProceedFalseException
from steps.CheckQueryDataFeasibility_V2 import CheckQueryDataFeasibility
from steps.ExecuteSqlQuery_V2 import ExecuteSqlQuery
from steps.FetchQueryContext_V3 import FetchQueryContext
from steps.GenerateSqlQuery import GenerateSqlQuery
from steps.QueryHistorySummarization_V1 import QueryHistorySummarization
from steps.ValidateGeneratedSqlQuery_V2 import ValidateGeneratedSqlQuery

logger = logging.getLogger(__name__)
"""
TODO
1. Gracefully del connection engines
"""


class ChatManagerV5(ChatManager):
    def __init__(
        self,
        database_object,
        websocket_object,
        socket_id,
        benchmark=False,
    ):
        logger.info("Initializing base chat manager v2")
        self.benchmark = benchmark

        self.query_history_summarization_object = QueryHistorySummarization(1, self)
        self.fetch_query_context_object = FetchQueryContext(2, self)
        self.check_query_data_feasibility_object = CheckQueryDataFeasibility(3, self)
        self.generate_sql_query_object = GenerateSqlQuery(4, self)
        self.validate_generated_sql_query_object = ValidateGeneratedSqlQuery(5, self)
        self.execute_sql_query_object = ExecuteSqlQuery(6, self)

        super().__init__(database_object, websocket_object, socket_id)

    def run(self, websocket_request, query_id):
        step_data = []

        try:

            # Process Chat Session History
            (
                query_history_summarization_output,
                query_history_summarization_step_data,
            ) = self.query_history_summarization_object.run(
                query_id=query_id,
                question=websocket_request.message,
                chat_history=websocket_request.history,
                benchmark=self.benchmark,
            )

            step_data.append(query_history_summarization_step_data)

            # FetchQueryContext step For Normal and For Ecommerce
            (
                fetch_query_context_output,
                fetch_query_context_step_data,
            ) = self.fetch_query_context_object.run(
                query_id,
                question=query_history_summarization_output.get(
                    "processed_question", websocket_request.message
                ),
                user_id=websocket_request.user_id,
                benchmark=self.benchmark,
            )
            step_data.append(fetch_query_context_step_data)

            # CheckQueryDataFeasibility step
            (
                check_query_data_feasibility_output,
                check_query_data_feasibility_step_data,
            ) = self.check_query_data_feasibility_object.run(
                query_id=query_id,
                processed_question=query_history_summarization_output.get(
                    "processed_question", websocket_request.message
                ),
                schema=fetch_query_context_output.get("feasibility_schema"),
                chat_history=query_history_summarization_output.get(
                    "history", websocket_request.message
                ),
                benchmark=self.benchmark,
            )
            step_data.append(check_query_data_feasibility_step_data)

            # if not check_query_data_feasibility_output.get("answerable", False):
            if False:
                if self.benchmark:
                    return [{"data": [{"answerable": False}]}], step_data
                else:
                    self.send_message(
                        _type="FINAL",
                        message=check_query_data_feasibility_output.get(
                            "query_schema_feasibility_remark"
                        ),
                        data={},
                        query_id=query_id,
                        step_data=step_data,
                    )
                return

            # Generate SQL query step
            (
                generate_sql_query_output,
                generate_sql_query_step_data,
            ) = self.generate_sql_query_object.run(
                query_id,
                processed_question=query_history_summarization_output.get(
                    "processed_question", websocket_request.message
                ),
                schema=fetch_query_context_output["schema"],
                query_schema_feasibility_remark="",
                benchmark=self.benchmark,
            )

            step_data.append(generate_sql_query_step_data)

            # Post process query step, only if ecommerce
            # logger.info(f"########Generate SQL Query Output###########: {generate_sql_query_output}\n")

            # ValidateGeneratedSqlQuery step
            (
                validate_generated_sql_query_output,
                validate_generated_sql_query_step_data,
            ) = self.validate_generated_sql_query_object.run(
                query_id,
                question=query_history_summarization_output.get(
                    "processed_question", websocket_request.message
                ),
                updated_queries=(generate_sql_query_output["generated_query"]),
                database_schema=fetch_query_context_output["schema"],
                benchmark=self.benchmark,
            )
            step_data.append(validate_generated_sql_query_step_data)

            # ExecuteSqlQuery step
            logger.info(
                f"validate_generated_sql_query_output: {validate_generated_sql_query_output}"
            )
            (
                execute_sql_query_output,
                execute_sql_query_step_data,
            ) = self.execute_sql_query_object.run(
                query_id,
                updated_queries=validate_generated_sql_query_output[
                    "validated_queries"
                ],
                benchmark=self.benchmark,
            )

            # removing data from validation step data
            for query_idx in range(len(step_data[-1].data["validated_queries"])):
                step_data[-1].data["validated_queries"][query_idx]["data"] = []

            step_data.append(execute_sql_query_step_data)

            # print("===========>", execute_sql_query_output)
            if len(execute_sql_query_output["data"]) == 1 and not self.benchmark:
                self.send_message(
                    _type="FINAL",
                    message=execute_sql_query_output["message"][0],
                    data=execute_sql_query_output["data"][0],
                    query_id=query_id,
                    step_data=step_data,
                )
                return
            elif len(execute_sql_query_output["data"]) > 1 and not self.benchmark:
                self.send_message(
                    _type="FINAL",
                    message=execute_sql_query_output["message"],
                    data=execute_sql_query_output["data"],
                    query_id=query_id,
                    step_data=step_data,
                )
                return
            elif not self.benchmark:
                self.send_message(
                    _type="FINAL",
                    query_id=query_id,
                    step_data=step_data,
                    error_message=str(execute_sql_query_output["message"][0]),
                    data={},
                    status_code=400,
                )

            if self.benchmark:
                return execute_sql_query_output["data"], step_data

        except ProceedFalseException as exc:
            step_data.append(exc.step_data)
            if not self.benchmark:
                self.send_message(
                    _type="FINAL",
                    query_id=query_id,
                    step_data=step_data,
                    error_message=str("Cannot Execute Query"),
                    status_code=400,
                )

        except Exception as exc:
            logger.error(
                f"Error in processing user query: {query_id} {str(exc)}",
                exc_info=True,
            )
            if not self.benchmark:
                self.send_message(
                    _type="FINAL",
                    query_id=query_id,
                    step_data=step_data,
                    error_message=str(exc),
                    status_code=400,
                )

        # Garbage collection
        finally:
            # Check if variables exist in scope, otherwise referencing them while deleting them will cause a NameError
            # Alternate would be to create a contextmanager class

            # FetchQueryContext step
            if "fetch_query_context_output" in locals():
                del fetch_query_context_output
            if "fetch_query_context_step_data" in locals():
                del fetch_query_context_step_data

            # GenerateSqlQuery step
            if "generate_sql_query_output" in locals():
                del generate_sql_query_output
            if "generate_sql_query_step_data" in locals():
                del generate_sql_query_step_data

            # ValidateGeneratedSqlQuery step
            if "validate_generated_sql_query_output" in locals():
                del validate_generated_sql_query_output
            if "validate_generated_sql_query_step_data" in locals():
                del validate_generated_sql_query_step_data

            # ExecuteSqlQuery step
            if "execute_sql_query_output" in locals():
                del execute_sql_query_output
            if "execute_sql_query_step_data" in locals():
                del execute_sql_query_step_data

            # PredictChartType
            if "predicted_chart_output" in locals():
                del predicted_chart_output
            if "predicted_chart_step_data" in locals():
                del predicted_chart_step_data

            # Any more steps in the future
            ...

            # Run the garbage collector
            gc.collect()
