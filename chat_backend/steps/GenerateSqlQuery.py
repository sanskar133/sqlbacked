import json
import logging

from engine.llms.open_ai_sql_gpt_v2 import OpenAISQLGenerator
from steps.base import Step

logger = logging.getLogger(__name__)


class GenerateSqlQuery(Step):
    START_MESSAGE = "Generating Sql Query"
    END_MESSAGE = "SQL Query Generated"
    ERROR_MESSAGE = "Error: Generating SQL Query"

    def __init__(self, *args, **kwargs):
        logging.info(f"Initializing step {self}")
        super().__init__(*args, **kwargs)
        self.llm_interface = OpenAISQLGenerator()

    def input_keys(self):
        ["processed_question", "schema", "query_schema_feasibility_remark"]

    def output_keys(self):
        return ["generated_query"]

    def __repr__(self):
        return "GenerateQuery"

    def __call__(self, processed_question, schema, query_schema_feasibility_remark):
        if schema:
            generated_query_data = self.llm_interface.generate(
                processed_question,
                self.chat_manager.database_object.display_name,
                schema,
                query_schema_feasibility_remark,
                query_id=self.query_id,
            )
            logger.info(
                f"########Generate SQL Query Output OpenAI###########: {generated_query_data}\n"
            )
        else:
            logger.error(f"########Generate SQL Query###########: Schema Not Found!\n")
            generated_query = None

        try:
            generated_query = generated_query_data["choices"][0]["message"]["content"]
        except:
            generated_query = None
        

        return json.loads(generated_query)
