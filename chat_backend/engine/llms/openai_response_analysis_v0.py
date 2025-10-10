import json
from typing import Any
from engine.llms import base
from engine.prompts.retrieved_data_analysis import retrieved_data_anlsysis_prompt
from engine.utils import prompts


class OpenAIResponseAnalyzer(base.BaseGenerator):
    """Use ChatGPT to analyze retrieved data with current user question."""

    def __init__(self) -> None:
        self.base_prompt = retrieved_data_anlsysis_prompt

    def generate(
        self,
        query: str,
        retrieved_data: Any,
        query_id=None,
    ):
        prompt = retrieved_data_anlsysis_prompt.format(
            query=query,
            retrieved_data=json.dumps(retrieved_data),
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
