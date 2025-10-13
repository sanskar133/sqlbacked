from databases.dbx.embeddings.base import BaseVectorizer
import requests
import pandas as pd
import os


class DBXEmbeddingModel(BaseVectorizer):

    def __init__(self):

        self.endpoint = os.getenv("EMBEDDING_ENDPOINT")
        token = os.getenv("DATABRICKS_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def get_embedding(self, text):

        input_data = pd.DataFrame({"sentences": text})
        records = input_data.to_dict("records")
        payload = {"dataframe_records": records}

        response = requests.post(
            self.endpoint, headers=self.headers, json=payload
        ).json()
        if "predictions" not in response:
            raise ValueError(f"Error in embedding text: {response}")
        # subject to change based on model response structure
        result = response["predictions"]["embeddings"]

        return result

    def generator(self):
        return super().generator()

    def storage(self):
        return super().storage()

    def similarity(self):
        return super().similarity()
