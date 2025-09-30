############ use pickle data base to get top 5 questions
# import pickle
# import pandas as pd
# import torch
# from sentence_transformers import SentenceTransformer, util

# df = pd.read_csv("cover/sample_queries.csv")

############ get response and chart for data
# import json

# import openai

# OPENAI_LLM_API_KEY = "ADD OPENAI KEY"  # ADD KEY HERE

# cl = openai.OpenAI(api_key=OPENAI_LLM_API_KEY)
# chatgpt = lambda func: (
#     cl.chat.completions.create(
#         model="gpt-4o",
#         temperature=0.7,
#         max_tokens=1024,
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are end-user response generator to help give relevant information to user.",
#             },
#             {
#                 "role": "assistant",
#                 "content": f"""Simlar examples:
#      {{
#         "question": "sales trend for last 6 months",
#         "query": "SELECT CONCAT(order_year, '-', LPAD(order_month, 2, '0')) AS order_date, SUM(COALESCE(net_sales_before_tax, 0)) AS net_sales FROM order_values WHERE TO_DATE(CONCAT(order_year, '-', LPAD(order_month, 2, '0')), 'yyyy-MM') >= DATE_TRUNC('month', ADD_MONTHS(CURRENT_DATE, -6)) AND TO_DATE(CONCAT(order_year, '-', LPAD(order_month, 2, '0')), 'yyyy-MM') < DATE_TRUNC('month', CURRENT_DATE) GROUP BY order_year, order_month ORDER BY order_year, order_month;",
#         "logic": "This query calculates monthly sales for the last 6 months. Note that last 6 months does NOT mean last 180 days. If we're on May 15 2024,to get the last 6 full months excluding the current month (May 2024), we need the following: Start date: First day of the month six months ago. End date: Last day of the previous month. Finally we are concatenating the Order Year and Order Month because they are separate columns in the table and we only want 2 columns in the output for ease of plotting. As the net_sales_before_tax column might contain null values, we use coalesce.",
#         "response": "Sure, here is a trend of net sales for the last 6 months. I have not included the numbers of the current month since you asked for the last 6 months.",
#         "chart": {{"type": "line", "x_axis": ["order_date"], "y_axis": ["net_sales"], "logic": "Since it is a trend, we'll use a line chart."}}
#     }},
#     {{
#         "question": "What are my sales for the last quarter?",
#         "query": "WITH last_completed_quarter AS (SELECT CASE WHEN order_quarter = 1 THEN order_year - 1 ELSE order_year END AS last_quarter_year, CASE WHEN order_quarter = 1 THEN 4 ELSE order_quarter - 1 END AS last_quarter FROM order_values GROUP BY order_year,order_quarter ORDER BY order_year DESC, order_quarter DESC LIMIT 1) SELECT SUM(COALESCE(net_sales_before_tax, 0)) AS total_sales_last_quarter FROM order_values o JOIN last_completed_quarter lq ON o.order_year = lq.last_quarter_year AND o.order_quarter = lq.last_quarter;",
#         "logic": "This query calculates the sales for the last quarter in the data. Note that the query dynamically calculates the last completed quarter using a series of CASE WHEN statements instead of hardcoding a value. We use coalesce as the net_sales_before_tax_column might contain null values.",
#         "response": "Certainly, your net sales for last quarter are below.",
#         "chart": {{"type": "null", "x_axis": ["null"], "y_axis": ["null"], "logic": "The question asks for a single value. So no chart is needed."}}
#     }},
#     {{
#         "question": "net revenue for the last 180 days",
#         "query": "SELECT SUM(net_sales_before_tax) AS total_sales_last_180_days FROM order_values WHERE order_date >= DATE_ADD(CURRENT_DATE, -180);",
#         "logic": "This query calculates the net sales for the 180 days. Net revenue and net sales are the same thing. For this query, since the data for last 180 days is needed, the DATE_ADD function is used with the syntax DATE_ADD(date, numDays).",
#         "response": "Certainly, your net revenue for the last 180 days are below.",
#         "chart": {{"type": "null", "x_axis": ["null"], "y_axis": ["null"], "logic": "The question asks for a single value. So no chart is needed."}}
#     }},
#     {{
#         "question": "What is the average order value of first time customers?",
#         "query": "WITH order_totals AS (SELECT order_id, SUM(net_sales_before_tax) AS total_net_sales_before_tax FROM order_values GROUP BY order_id), first_orders AS (SELECT customer_id, MIN(order_date) AS first_order_date FROM order_values GROUP BY customer_id) SELECT AVG(ot.total_net_sales_before_tax) AS avg_net_sales_aov_first_time_customers FROM order_totals ot JOIN order_values o ON ot.order_id = o.order_id JOIN first_orders f ON o.customer_id = f.customer_id AND o.order_date = f.first_order_date;",
#         "logic": "Since the table order_values is at an Order ID - SKU ID level, the order_totals CTE calculates the total sales at an Order ID level. Then the first order date for customers is calculated in the first_orders CTE. Finally in the main query everything is merged to get the average order value for first time customers. Note that net_sales_before_tax is used for average order value calculation. The question asks for a single value. So no chart is needed.",
#         "response": "Sure, the Average Order Value for first time customers, i.e. orders for which the first order date = order date is below. I have used net sales to calculate AOV.",
#         "chart": {{"type": "null", "x_axis": ["null"], "y_axis": ["null"], "logic": "The question asks for a single value. So no chart is needed."}}
#     }},
#     {{
#         "question": "What is the quarterly trend of orders for the last 4 quarters?",
#         "query": "SELECT CONCAT(order_year, '-Q', order_quarter) AS year_quarter, COUNT(DISTINCT order_id) AS total_orders FROM order_values WHERE (order_year, order_quarter) IN (SELECT order_year, order_quarter FROM order_values GROUP BY order_year, order_quarter ORDER BY order_year DESC, order_quarter DESC LIMIT 4) GROUP BY order_year, order_quarter ORDER BY order_year DESC, order_quarter DESC;",
#         "logic": "This query aggregates net sales for the last 4 quarters, including the ongoing one. Since the trend of orders is requested, the distinct count of order_id is taken as the table is unique at an Order ID - SKU ID level. We'll plot it in a line chart since it is a trend.",
#         "response": "Here you go! Here's the trend of orders for the last 4 quarters. I have also included the current quarter.",
#         "chart": {{"type": "bar", "x_axis": ["year_quarter"], "y_axis": ["total_orders"], "logic": "Since it is a trend, we'll use a line chart."}}
#     }},
#     {{
#         "question": "Give me the revenue split for the last month by channel.",
#         "query": "SELECT source, SUM(net_sales_before_tax) AS net_sales FROM order_values WHERE order_year = YEAR(DATE_SUB(CURRENT_DATE, DAY(CURRENT_DATE))) AND order_month = MONTH(DATE_SUB(CURRENT_DATE, DAY(CURRENT_DATE))) GROUP BY source;",
#         "logic": "This query retrieves the revenue split for the last month, comparing the channels, e.g. Amazon and Shopify.",
#         "response": "Here you go! Here's the trend of orders for the last 4 quarters. I have also included the current quarter.",
#         "chart": {{"type": "pie", "x_axis": ["source"], "y_axis": ["net_sales"], "logic": "Since we're showing a distribution over a small number of values, we will use a pie chart."}}
#     }}""",
#             },  # RAG
#             {
#                 "role": "user",
#                 "content": f"""
#         For following record, generate relevant 'response' and 'chart' in JSON format like {{"response": answer, "chart": answer}}.
#         {{"question":{func.question},
#         "query":{func.query},
#         "logic":{func.logic}}}""",
#             },
#         ],
#     )
# )

# df["gpt_response"] = df.apply(chatgpt, axis=1)


# df = pd.concat(
#     [
#         df.drop(["sno", "gpt_response"], axis=1),
#         df["gpt_response"]
#         .apply(
#             lambda x: json.loads(
#                 x.choices[0].message.content.strip("```").strip("json").strip("\n")
#             )
#         )
#         .apply(pd.Series),
#     ],
#     axis=1,
# )
# df.to_csv("cover/sample_queries.csv", index=False)
############ get response and chart for data


############ generate embeddings for questions and save to pickle
import os
import pickle

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer

nltk.download("stopwords")

user_id = "presales_demo_loan"

model = SentenceTransformer(
    "nomic-ai/nomic-embed-text-v1.5",
    trust_remote_code=True,
    truncate_dim=256,
    device="cpu",
)
stop_words = set(stopwords.words("english"))

db_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "sample_database",
    user_id,
)

df = pd.read_csv(os.path.join(db_path, "sample_queries.csv"))

df["question_processed"] = df["question"].apply(
    lambda x: " ".join(
        [
            word_token
            for word_token in word_tokenize(x)
            if not word_token.lower() in stop_words and not word_token.isdigit()
        ]
    )
)

df["embedding"] = df["question_processed"].apply(
    lambda x: model.encode(x, convert_to_tensor=True)
)


db_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "sample_database",
)
with open(os.path.join(db_path, f"{user_id}_sample_query_vector_db.pkl"), "wb") as fp:
    pickle.dump(df, fp)
############ generate embeddings for questions and save to pickle


############ # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
# model = SentenceTransformer("all-MiniLM-L12-v2")

# query = "Get monthly trend of returns for last 12 months"

# with open("cover/sample_query_vector_db.pkl", "rb") as fp:
#     df = pickle.load(fp)

# top_k = min(5, df.shape[0])
# query_embedding = model.encode(query, convert_to_tensor=True)

# # We use cosine-similarity and torch.topk to find the highest 5 scores
# cos_scores = util.cos_sim(
#     query_embedding, torch.stack((df["embedding"].values.tolist()), dim=0)
# )[0]
# top_results = torch.topk(cos_scores, k=top_k)

# print("\n\n======================\n\n")
# print("Query:", query)
# print("\nTop 5 most similar sentences in corpus:")

# question_list = df["question"].values.tolist()
# for score, idx in zip(top_results[0], top_results[1]):
#     print(question_list[idx], "(Score: {:.4f})".format(score))


############ get final samples
# import ast

# samples = (
#     df.loc[top_results.indices.tolist()].drop(["embedding"], axis=1).to_dict("records")
# )
# for sample in samples:
#     try:
#         sample.update({"chart": ast.literal_eval(sample["chart"])})
#     except:
#         pass
# print(samples)
