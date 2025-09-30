"""base class for llm-sql generators"""

import os
import time
from abc import ABC, abstractmethod

import pandas as pd
from settings import env
from utils import commons


class BaseGenerator(ABC):
    """Base llm generator for nlp-sql and memory augmentation"""

    if env.LLM_PROVIDER == "AZURE":
        from openai import AzureOpenAI

        client = AzureOpenAI(
            api_key=env.LLM_API_KEY,
            api_version=env.LLM_API_VERSION,
            azure_endpoint=env.LLM_API_ENDPOINT,
        )
    elif env.LLM_PROVIDER == "OPENAI":
        from openai import OpenAI

        client = OpenAI(api_key=env.LLM_API_KEY)
    else:
        raise ImportError("LLM provider should be either AZURE or OPENAI.")

    temperature = 0.2
    top_p = 0

    @abstractmethod
    async def generate(
        self, query: str, database_type: str = None, database_schema: str = None
    ):
        """all generators must define generate method"""

    @commons.error_decorator(error_type=Exception, raise_exc=False)
    def _get_result(self, prompt: str) -> dict:
        t_0 = time.perf_counter()
        llm_result = self.client.chat.completions.create(
            model=env.LLM_MODEL_NAME,
            temperature=self.temperature,
            top_p=self.top_p,
            messages=[{"role": "user", "content": prompt}],
        )
        t_final = time.perf_counter()

        llm_result = llm_result.model_dump()
        llm_result["time_taken_secs"] = round(t_final - t_0, 2)

        return llm_result

    @commons.error_decorator(error_type=Exception, raise_exc=False)
    def _get_result_json(self, prompt: str) -> dict:
        t_0 = time.perf_counter()
        llm_result = self.client.chat.completions.create(
            model=env.LLM_MODEL_NAME,
            response_format={"type": "json_object"},
            temperature=self.temperature,
            top_p=self.top_p,
            messages=[{"role": "user", "content": prompt}],
        )
        t_final = time.perf_counter()

        llm_result = llm_result.model_dump()
        llm_result["time_taken_secs"] = round(t_final - t_0, 2)

        return llm_result

    def proceed(self, *args, **kwargs):
        return True

    def _save_llm_result(self, question, result, query_id, **kwargs):
        """helper method to log all llm generated reponses"""
        model_name = result["model"]
        input_token_count = result["usage"]["prompt_tokens"]
        output_token_count = result["usage"]["completion_tokens"]

        # save LLM RESULT
        file_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "sample_database",
            "llm_response.csv",
        )

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame(
                columns=[
                    "query_id",
                    "user_query",
                    "response",
                    "response_time",
                    "model_name",
                    "input_token_count",
                    "output_token_count",
                ]
            )

        # New data to append (example data, you should replace this with actual data)
        new_data = pd.DataFrame(
            [
                {
                    "query_id": query_id,
                    "user_query": question[:9990],
                    "response": result,
                    "response_time": result["time_taken_secs"],
                    "model_name": model_name,
                    "input_token_count": input_token_count,
                    "output_token_count": output_token_count,
                }
            ]
        )

        # Append the new data to the DataFrame
        df = pd.concat([df, new_data], ignore_index=True)

        # Save the updated DataFrame back to the CSV file
        df.to_csv(file_path, index=False)
