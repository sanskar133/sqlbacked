import logging

from engine.llms.openai_response_analysis_v0 import OpenAIResponseAnalyzer
from steps.base import Step

logger = logging.getLogger(__name__)


class ResponseAnalyzer(Step):
    START_MESSAGE = "Analyzing Retrieved data based User Question"
    END_MESSAGE = "Retrieved data analyzed based on User Query"
    ERROR_MESSAGE = f"Error: {START_MESSAGE}"

    def __init__(self, *args, **kwargs):
        logging.info(f"Initializing step {self}")
        super().__init__(*args, **kwargs)
        self.llm_response_analysis = OpenAIResponseAnalyzer()

    def input_keys(self):
        return ["user_query", "retrieved_data"]

    def output_keys(self):
        return ["analysis"]

    def __repr__(self):
        return "QueryHistResponseAnalyzer"

    def __call__(self, query, retrieved_data):

        analysis = self.llm_response_analysis.generate(
            query=query,
            retrieved_data=retrieved_data,
            query_id=self.query_id,
        )

        analysis = analysis["choices"][0]["message"]["content"]
    

        logger.info(analysis)

        return {"analysis": analysis}
