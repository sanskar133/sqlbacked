"""OpenAI and Azure GPT SQL Generator"""

from engine.llms import base
from engine.prompts import sql_prompt
from engine.utils import prompts, validators


class OpenAISQLGenerator(base.BaseGenerator):
    """NLP-SQL generator using OpenAI and AzureGPT"""

    def __init__(self) -> None:
        self.base_prompt = sql_prompt.SQL_WITH_REMARK_PROMPT_V3

    def generate(
        self,
        query: str,
        database_type: str = None,
        database_schema: str = None,
        query_schema_feasibility_remark: str = None,
        query_id: str = None,
    ):
        """Generate SQL code for user query

        Args:
            query (str): User query
            database_type (str): database type e.g. Postgres, Snowflake
            database_schema (str): schema of relevant table
            query_schema_feasibility_remark (str): feedback on wheather the query can be written or not

        Returns:
            (json): result from the database
        """
        validators.validate_database_type(database_type=database_type)

        prompt = prompts.prepare_sql_prompt_v2(
            base_prompt=self.base_prompt,
            query=query,
            database_type=database_type,
            database_schema=database_schema,
            query_schema_feasibility_remark=query_schema_feasibility_remark,
        )

        prompts.check_prompt_attack(prompt=prompt)
        llm_result = self._get_result_json(prompt=prompt)

        if query_id is not None:
            self._save_llm_result(
                prompt,
                llm_result,
                query_id,
            )

        return llm_result
