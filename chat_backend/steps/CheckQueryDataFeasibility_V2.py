import json
import logging

from engine.llms.open_ai_query_data_feasibility_v2 import OpenAIQueryDataFeasibility
from steps.base import Step

logger = logging.getLogger(__name__)


class CheckQueryDataFeasibility(Step):
    START_MESSAGE = "Checking Query Data Feasibility"
    END_MESSAGE = "Query Data Feasibility Check Completed"
    ERROR_MESSAGE = "Error: Checking Query Data Feasibility"

    def __init__(self, *args, **kwargs):
        logging.info(f"Initializing step {self}")
        super().__init__(*args, **kwargs)
        self.llm_query_data_feasibility = OpenAIQueryDataFeasibility()

    def input_keys(self):
        return ["processed_question", "schema"]

    def output_keys(self):
        return ["query_schema_feasibility_remark", "proceed"]

    def __repr__(self):
        return "CheckQueryDataFeasibility_V2"

    def __call__(self, processed_question, schema, chat_history):
        query_schema_feasibility_remark_data = self.llm_query_data_feasibility.generate(
            processed_question,
            schema,
            query_id=self.query_id,
            chat_history=chat_history,
        )

        proceed = self.llm_query_data_feasibility.proceed(
            query_schema_feasibility_remark_data
        )
        logger.info(f"Question Answerable: {proceed}")

        try:
            query_schema_feasibility_remark = query_schema_feasibility_remark_data[
                "choices"
            ][0]["message"]["content"]
            print(query_schema_feasibility_remark)
            try:
                query_schema_feasibility_remark = json.loads(
                    query_schema_feasibility_remark
                )
            except:
                query_schema_feasibility_remark = {
                    "COMMENTS": query_schema_feasibility_remark
                }
        except:
            query_schema_feasibility_remark = {"COMMENTS": None}
        logger.info(query_schema_feasibility_remark)
        return {
            "query_schema_feasibility_remark": query_schema_feasibility_remark.get(
                "COMMENTS"
            ),
            "follow_up_question": query_schema_feasibility_remark.get(
                "FOLLOW_UP_QUESTION", ""
            ),
            "answerable": proceed,
        }
