from functools import partial

VALIDATION_PROMPT = """Given the following query and sql database schema.
Help me figure out if query can be answered from the database.
Please categorize the query in YES, and NO.
DEFINITION of categories:
    YES - yes query can be answered with coloumns present in the database. Reply yes for queries which ask for database snapshots as well. e.g. get all tables from database
    NO - it should be last resort in case query can not be answered at all by any means from the database
Feel free to add you comments under comments.

SCHEMA: {database_schema}
QUERY: {user_query}
CATEGORY:
COMMENTS:
"""

VALIDATION_PROMPT_V2 = """
I want you to act as a business analyst.
You will receive questions from the business team and will be provided database schema and chat history.
For each question, identify if there is enough information in the question for it to be answered using SQL query:

ANSWERABLE DEFINITION:
- yes: If the question can be answered using a SQL query, set "ANSWERABLE" to "yes" and leave "FOLLOW_UP_QUESTION" empty.
- no: If the question cannot be answered using a SQL query, set "ANSWERABLE" to "no" and generate a follow-up question that seeks additional information to make the question answerable.

Your responses should be formatted as JSON, containing if question is 'ANSWERABLE', 'FOLLOW_UP_QUESTION' (if any)  and 'COMMENTS'. Please adhere to the following format for your responses and exclude any additional indicators like ```json{{}}```, etc.:
{{"ANSWERABLE": "yes" or "no","FOLLOW_UP_QUESTION": "" empty if "ANSWERABLE" is "no" else a follow-up question, "COMMENTS":"Your detailed analysis plan and comments here. Avoid providing SQL query examples. Don't copy content from prompt in this section."}}

Database Schema:
{database_schema}

# Example Input and Output:
Business Question: "What is the net revenue of conglomerate inc. for year 2020?"
Response:
{{
  "ANSWERABLE": "yes",
  "FOLLOW_UP_QUESTION": "",
  "COMMENTS":"as required details are present, we can answer using SQL query"
}}

Business Question: "What is the EBITDA of conglomerate inc.?"
Response:
{{
  "ANSWERABLE": "no",
  "FOLLOW_UP_QUESTION": "Can you please clarify for which time period? Do you want to see values across all years, for specific time range, or something else?",
  "COMMENTS":"The question seems ambiguous as given information is not sufficient to answer the question and identify appropriate user ASK based on database schema"
}}

Your task is to prepare an analysis plan and respond according to the aforementioned criteria.
Be accurate as you might end up declaring a question to be not answerable even if it is complete.
Refer to Sample questions and queries as well.

Do not ask follow-up questions with technical words like table name, column name, etc. User is un-aware of DB schema.

Be mindful before making decision if question is answerable.
Keep in consideration the recent chat history as well and avoid asking same question again and again:
Chat History:
```
{chat_history}
```

Business Question: {user_query}

Response:
"""
