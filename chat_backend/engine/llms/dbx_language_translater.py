from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
import json


class DBXLanguageTranslater:
    """Class to interact with Databricks LLM serving endpoint for language translation."""

    def __init__(self):

        self.client = WorkspaceClient()
        self.endpoint_name = (
            "databricks-meta-llama-3-3-70b-instruct"  # Example endpoint name
        )
        self.system_prompt = (
            "You are a helpful assistant that translates the given text into english"
            "You will be given a dictionary with keys in english and values in another language. Your task is to translate the values into english while keeping the keys unchanged."
            "Return the output in the same dictionary format."
        )
        self.max_tokens = 512
        self.temperature = 0.7

    def __call__(self, text: str) -> str:
        """Translate the given text to the target language using the LLM endpoint."""
        user_prompt = f"Translate the following text to english:\n\n{text}"

        messages = [
            ChatMessage(role=ChatMessageRole.SYSTEM, content=self.system_prompt),
            ChatMessage(role=ChatMessageRole.USER, content=user_prompt),
        ]

        response = self.client.serving_endpoints.query(
            name=self.endpoint_name,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        data = response.choices[0].message.content
        try:
            return json.loads(data)
        except:
            start_index = data.find("{")
            end_index = data.rfind("}") + 1
            json_data = data[start_index:end_index]
            return json.loads(json_data)
