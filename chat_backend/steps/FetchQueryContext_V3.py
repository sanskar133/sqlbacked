import ast
import logging
import os
import pickle

import nltk
import torch
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer, util
from settings import env
from steps.base import Step

logger = logging.getLogger(__name__)
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

emb_model = SentenceTransformer(
    "nomic-ai/nomic-embed-text-v1.5",
    trust_remote_code=True,
    truncate_dim=256,
    device="cpu",
)

# nltk.download("punkt")
# nltk.download("stopwords")


class FetchQueryContext(Step):
    START_MESSAGE = "Fetching Query Context"
    END_MESSAGE = "Context Fetched for Query"
    ERROR_MESSAGE = "Error: Fetching Query Context"

    def __init__(self, *args, **kwargs):
        logging.info(f"Initializing step {self}")
        self.model = emb_model

        super().__init__(*args, **kwargs)

    def input_keys(self):
        return ["question"]

    def output_keys(self):
        return ["schema"]

    def __repr__(self):
        return "FetchQueryContext"

    def _get_relevant_tables(self, question: str, user_id: str, k: int = 15):
        stop_words = set(stopwords.words("english"))
        word_tokens = word_tokenize(question)

        filtered_question = " ".join(
            [
                word_token
                for word_token in word_tokens
                if not word_token.lower() in stop_words
            ]
        )

        # load local database
        db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "sample_database",
            f"{user_id}_embedding.pkl",
        )

        if not os.path.exists(db_path):
            return []

        with open(db_path, "rb") as fp:
            df = pickle.load(fp)

        # generate embedding of question
        top_k = min(k, df.shape[0])
        question_embedding = self.model.encode(
            filtered_question, convert_to_tensor=True
        )

        cos_scores = util.cos_sim(
            question_embedding, torch.stack((df["embedding"].values.tolist()), dim=0)
        )[0]
        top_results = torch.topk(cos_scores, k=top_k)

        # get top k results in desired format
        return df.loc[top_results.indices.tolist()]["table_name"].unique().tolist()

    def _get_k_most_relevant_queries_from_local_db(
        self, question: str, user_id: str, k: int = 5
    ):
        stop_words = set(stopwords.words("english"))

        word_tokens = word_tokenize(question)

        filtered_question = " ".join(
            [
                word_token
                for word_token in word_tokens
                if not word_token.lower() in stop_words
            ]
        )

        # load local database
        db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "sample_database",
            f"{user_id}_sample_query_vector_db.pkl",
        )

        if not os.path.exists(db_path):
            return []

        with open(db_path, "rb") as fp:
            df = pickle.load(fp)

        # generate embedding of question
        top_k = min(k, df.shape[0])
        question_embedding = self.model.encode(
            filtered_question, convert_to_tensor=True
        )

        cos_scores = util.cos_sim(
            question_embedding, torch.stack((df["embedding"].values.tolist()), dim=0)
        )[0]
        top_results = torch.topk(cos_scores, k=top_k)

        # get top k results in desired format
        samples = (
            df.loc[top_results.indices.tolist()]
            .drop(["embedding", "question_processed"], axis=1)
            .to_dict("records")
        )

        # load chart strings as dict
        for sample in samples:
            try:
                sample.update({"chart": ast.literal_eval(sample["chart"])})
            except:
                pass
        return samples

    def _process_unstructured_schema(self, question: str, user_id: str):
        # TODO: get top 10 relevant column embeddings -> corresponding unique tables names
        if user_id == "presales_demo_ecom":
            from sample_database.presales_demo_ecom_schema import (
                table_and_descriptions,
                table_to_column_mapping,
            )
            table_names = list(table_and_descriptions.keys())
            database_sample_queries = {}
        
        elif user_id == "presales_demo_loan":
            from sample_database.presales_demo_loan_schema import (
                table_and_descriptions,
                table_to_column_mapping,
            )
            table_names = list(table_and_descriptions.keys())
            database_sample_queries = {}

        else:
            table_names = self._get_relevant_tables(question, user_id)
            print("TABLE_NAMES:", table_names)

            # load local database
            db_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "sample_database",
                f"{user_id}_schema.pkl",
            )

            with open(db_path, "rb") as fp:
                (
                    table_and_descriptions,
                    table_to_column_mapping,
                    database_sample_queries,
                ) = pickle.load(fp)

        schema = """"""

        for t_name, t_desc in table_and_descriptions.items():
            # if table names is non-empty check if t_name is there, else True for all t_name
            if (table_names and t_name in table_names) or (len(table_names) == 0):
                column_name_and_description = table_to_column_mapping[t_name]

                schema += f"table_name: {t_name}, table_description: {t_desc}\n"

                for col, desc_and_samplevalues in column_name_and_description.items():
                    desc = desc_and_samplevalues["description"]
                    values_sample = desc_and_samplevalues.get("values_sample", [])

                    schema += f"\t\tcolumn_name: {col}, column_description: {desc}"

                    if values_sample:
                        schema += f", values_sample: {values_sample}"

                    schema += "\n"

                schema += "\n"

        feasibility_schema = schema

        if database_sample_queries:
            sample_queries_to_use = self._get_k_most_relevant_queries_from_local_db(
                question, user_id, k=5
            )
            if not sample_queries_to_use:
                sample_queries_to_use.extend(database_sample_queries)
            # following the format outlined in datamodels_config.pyc
            schema += f"\nSample Queries from database:\n"
            for q in sample_queries_to_use:
                schema += f"\tsample_question: {q.get('question')}\n"
                schema += f"\texpected_query: {q.get('query')}\n"
                schema += f"\tlogic: {q.get('logic')}\n"
                schema += f"\tresponse: {q.get('response')}\n"
                schema += f"\tchart: {q.get('chart')}\n"

                schema += "\n"

        return schema.strip(), feasibility_schema.strip()

    def __call__(self, question: str, user_id: str, *args, **kwargs):
        """
        Get schema from datamodels_config_new
        """

        user_schema_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "sample_database",
            f"{user_id}_schema.pkl",
        )
        if user_id in ["presales_demo_ecom", "presales_demo_loan"] or os.path.exists(user_schema_path):
            # LOAD COLUMNS, DATABASE_SAMPLE_QUERIES, TABLE_DESCRIPTIONS from pkl
            schema, feasibility_schema = self._process_unstructured_schema(
                question, user_id
            )
            # including sample queries as well for now
            feasibility_schema = schema
        else:  # fallback
            schema = self.chat_manager.database_object.database_schema
            feasibility_schema = schema

        logger.info(schema)

        return {"schema": schema, "feasibility_schema": feasibility_schema}
