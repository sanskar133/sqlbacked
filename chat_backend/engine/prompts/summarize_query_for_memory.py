SUMMARIZATION_PROMPT = """You are given the chat history, which contains human queries with AI responses.
Your job is to alter the Current User Question below, in such a way that the New Question is a natural language question which will be resolved into an SQL statement using an LLM, but the New Question is resolved based on the Chat History. No relative words like 'less', 'more', 'previous', 'next', etc. or placeholder words like 'this' or 'that' can be in the output, always resolve in some quantitative form using the chat history as context.
Note that its possible that some questions will contain entirely new context, and not be related to the chat history. In such cases, just output the user question as is. Only manipulate the question if its context matches that of the chat history. Usually, these kind of questions will contain a table name.

Example History and expected behavior:
# example with follow up question
History:
User: What is revenue of conglomerate inc.?
AI: For which time period are you looking it for?

Current User Question: 2020
New User Question: What is revenue of conglomerate inc. for year 2020?

# example with related context
History:
User: What is revenue of conglomerate inc. for year 2020?
AI: Here is the revenue of conglomerate inc. for year 2020:

Current User Question: now tell me the gross margin
New User Question: What is gross margin of conglomerate inc. for year 2020?

# example with un-related context
History:
User: What is revenue of conglomerate inc. for year 2020?
AI: Here is the revenue of conglomerate inc. for year 2020:

Current User Question: What is the revenue of Apple inc.?
New User Question: What is the revenue of Apple inc.?

Use the given examples as reference and do the similar thing for the following:
Chat History:
```
{chat_history}
```

Current User Question: {user_question}
New User Question:
"""
