FIX_SQL_QUERY_ERROR_PROMPT = """As a data analyst with expertise in {database_type} SQL, review the following SQL query and the associated error. Please provide the corrected version of the SQL query. If the query is already correct, return it without modifications.

Question:
{question}

SQL Query with Error:
{sql_query}

Error Message:
{error}

##TIPS:

1. If the query contains any other type of error, rewrite the query to answer the question correctly.

Format your responses as JSON, including the SQL query and the following associated fields. Use this format:

{{"sql_query": "Your SQL Query Here"}}
"""
