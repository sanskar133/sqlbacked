"""OpenAI and Azure GPT SQL Generator"""

import json

from engine.llms import base
from engine.prompts import query_data_feasibility
from engine.utils import prompts


class OpenAIQueryDataFeasibility(base.BaseGenerator):
    """Check if query can be answered from the database, based on database schema."""

    def __init__(self) -> None:
        self.base_prompt = query_data_feasibility.VALIDATION_PROMPT_V2

    def proceed(self, llm_result: list[dict]):
        """Check if we should move to the next step or end the pipeline"""
        content = llm_result["choices"][0]["message"]["content"]
        print(content)
        try:
            content = json.loads(content)
            if content.get("ANSWERABLE", "NO").lower() == "yes":
                return True
            else:
                return False

        except:
            if content.replace("ANSWERABLE:", "").strip().lower().startswith("yes"):
                return True
            else:
                return False

    def generate(
        self,
        query: str,
        database_schema: str = None,
        chat_history: str = None,
        query_id: str = None,
    ):
        """Generate validation remarks regarding queries compatibility with database

        Args:
            query (str): User query
            database_type (str): database type e.g. Postgres, Snowflakes
            database_schema (str): schema of relevant table

        Returns:
            (json): result from the database
        """

        prompt = prompts.prepare_query_schema_match_prompt_v1(
            base_prompt=self.base_prompt,
            query=query,
            chat_history=chat_history,
            database_schema=database_schema,
        )

        prompts.check_prompt_attack(prompt=prompt)
        llm_result = self._get_result(prompt=prompt)

        if query_id is not None:
            self._save_llm_result(
                prompt,
                llm_result,
                query_id,
            )

        return llm_result
