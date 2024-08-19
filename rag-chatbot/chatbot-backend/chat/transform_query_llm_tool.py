from openai import OpenAI
from typing import List
from chat.prompts import transform_query_system_message
from jinja2 import Template

def transform_query_llm(query: str, prev_history_documents: List[dict]):
    
    chat_history = "\n".join(document["content"] for document in prev_history_documents if 'content' in document)
    client = OpenAI()
    completion=client.chat.completions.create(
        messages=[
            {"role": "system", "content": transform_query_system_message },
            {"role": "user", "content": "Conversation: "+"\n"+chat_history + "\n"+ "Follow-up Question: "+ query}
        ],
        model="gpt-3.5-turbo"
    )


    return completion.choices[0].message.content