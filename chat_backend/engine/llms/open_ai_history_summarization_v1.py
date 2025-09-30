from engine.llms import base
from engine.prompts import summarize_query_for_memory
from engine.utils import prompts


class OpenAIHistorySummarization(base.BaseGenerator):
    """Use ChatGPT to summarize the history and current user question into a single query."""

    def __init__(self) -> None:
        self.base_prompt = summarize_query_for_memory.SUMMARIZATION_PROMPT

    def generate(
        self,
        query: str,
        chat_history: str,
        query_id=None,
    ):
        prompt = prompts.prepare_query_for_history_summarization(
            base_prompt=self.base_prompt,
            query=query,
            history=chat_history,
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
