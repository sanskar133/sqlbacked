SQL_PROMPT = """
The user provides a question and you provide {database_type} query. You will only respond with SQL query and not with any explanations.

Respond with only SQL query.

Consider the following BEST PRACTICES while writing the SQL query.
{best_practices}

You may use the following SCHEMA as a reference for what tables might be available.
{database_schema}

{sample_queries}

{dos_donts}

QUESTION: {user_query}
SQL QUERY IN PLAIN TEXT: """

SQL_WITH_REMARK_PROMPT = """
The user provides a question and you provide {database_type}. You will only respond with SQL query and not with any explanations.

Respond with only SQL query.


You may use the following SCHEMA as a reference for what tables might be available.
Do not correct spelling mistakes in column and table names when you are writing the query.d
{database_schema}

We checked if the query can be answered from the database and have the following remark.
Consider it while writing the query.
REMARK: {query_schema_feasibility_remark}

QUESTION: {user_query}
SQL QUERY IN PLAIN TEXT: """

FINAL_SQL_PROMPT = SQL_PROMPT

SQL_WITH_REMARK_PROMPT_V2 = """
As a Business Analyst, respond to business team inquiries by writing SQL queries for a {database_type} database. Refer to the provided database schema for tables and columns. Do not correct spelling mistakes in the schema.

Format your responses as JSON, including the SQL query and an associated brief comment. Exclude any additional notes or explanatory text outside the JSON structure. Use this format:
[{{"sql_query": "Your SQL Query Here", "comment": "Your brief explanatory comment here"}}]

Database Schema:
{database_schema}

Business Question:
{user_query}

Provide the necessary SQL queries based on the following analysis plan, formatted strictly according to the above JSON structure without appending extra notes or comments:

Analysis Plan:
{query_schema_feasibility_remark}

Response:
"""

SQL_WITH_REMARK_PROMPT_V3 = """
You are a SQL expert in {database_type}. As a SQL expert, your job is to answer data related questions from the business team accurately by writing SQL queries. Refer to the provided database schema for tables and columns. Do not correct spelling mistakes in the schema.

Please generate only read/SELECT queries for data safety. If a question cannot be answered using a SELECT operation, it should not be addressed.
Refer the sample queries to see how date filters and calculations are done. Pay high attention on sample queries that seem most relevant to user question.
Sample queries are good for reference, but table and column descriptions are key in identifying correct columns and getting correct answer for the given question.

Format your responses as JSON, including the SQL query and the following associated fields. Use this format:

generated_query:[{{"sql_query": "Your SQL Query Here", "logic": "Explain briefly the logic you used", "response": "A friendly and conversational response to give more context to the user.", "chart": {{"type": "The type of chart", "x_axis": ["Array of variables in the x-axis of the chart"], "y_axis": ["Array of variables in the y-axis of the chart"]}} }}]

## Database Schema:
{database_schema}

## Question from Business Team:
{user_query}

## Guidelines that are necessary to follow for making correct SQL queries:
1. Whenever working with any text fields, always cast both column and value to lowercase before performing any operations on them.
2. Chart Type, X-axis and Y-axis will be "null" when the question asks for a single value instead of a trend or split.
3. Ensure numeric typecasting for numerators in division operations.
4. Use lowercase for string matching to maintain consistency. Note: Do type casting to varchar only if needed (mainly in case of Mssql DB type).
5. Apply the same operation in both GROUP BY and SELECT clauses when referencing the same field.
6. Create aliases for fields in SELECT on which operations are applied.
7. Always prefix field names with table or alias names in joins.
8. Treat numeric fields as measures and text, enums, and time fields as dimensions in aggregation queries.
9. Please do not refer the database name in column or table names.
10. Prevent zero division errors by validating the denominator in division operations.
11. Exclude null values in aggregations of numeric fields.
12. Use LOWER in GROUP BY only if the same column in SELECT is also in LOWER.
13. Please consider the granularity level of the table and do appropriate aggregations.
e.g.: If order_data table has Order ID - SKU ID columns, and question is asked at order level, group rows by Order ID. Write queries accordingly.
14. In case time period is not mentioned, use last 12 calendar months data only for calculations, unless lifetime value like questions are asked.
15. Consider order by ABS value wherever seems logical.
16. Round the calculations to 2 decimal points at appropriate places, like AVG and Percentages.

{query_schema_feasibility_remark}

## Response:
"""
