import logging

from engine.llms.open_ai_history_summarization_v1 import OpenAIHistorySummarization
from steps.base import Step

logger = logging.getLogger(__name__)


class QueryHistorySummarization(Step):
    START_MESSAGE = "Summarizing User Question based on History"
    END_MESSAGE = "User Question Summarized based on History"
    ERROR_MESSAGE = "Error: Summarizing User Question based on History"

    def __init__(self, *args, **kwargs):
        logging.info(f"Initializing step {self}")
        super().__init__(*args, **kwargs)
        self.llm_summarization = OpenAIHistorySummarization()
        self.history_window_size = 10

    def input_keys(self):
        return ["question"]

    def output_keys(self):
        return ["processed_question"]

    def _get_past_chat_messages(self, chat_history: list) -> str:
        """
        Get Past Chat Messages Using Chat Id
        """
        # the last 5 messages and reverse them back to the writing order
        history = ""
        for chat in chat_history:
            chat_tuple = [item for item in chat.items()][0]
            history += f"{chat_tuple[0]}: {chat_tuple[1]}\n"

        return history

    def __repr__(self):
        return "QueryHistorySummarization"

    def __call__(self, question, chat_history):

        chat_history_str = self._get_past_chat_messages(
            chat_history[-self.history_window_size :]
        )

        augmented_question = self.llm_summarization.generate(
            question,
            chat_history_str,
            self.query_id,
        )

        try:
            augmented_question = augmented_question["choices"][0]["message"]["content"]
        except Exception:
            augmented_question = question

        logger.info(augmented_question)

        return {"processed_question": augmented_question, "history": chat_history_str}
