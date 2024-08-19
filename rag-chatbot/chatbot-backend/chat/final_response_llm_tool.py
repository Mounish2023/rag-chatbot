from openai import OpenAI
from typing import List
from chat.prompts import final_response_system_prompt, final_response_user_message
from jinja2 import Template

def final_response_from_llm(query: str, documents: List[dict], prev_history_documents: List[dict]):
    
    source_knowledge = "\n".join(document["content"] for document in documents if 'content' in document)
    prev_history = "\n".join(document["content"] for document in prev_history_documents if 'content' in document)
    user_template=Template(final_response_user_message)
    rendered_user_template=user_template.render( source_knowledge = source_knowledge,prev_history=prev_history)
    client = OpenAI()
    completion=client.chat.completions.create(
        messages=[
            {"role": "system", "content": final_response_system_prompt },
            {"role": "system", "content": rendered_user_template},
            {"role": "user", "content": query},
        ],
        model="gpt-3.5-turbo"
    )


    return completion.choices[0].message.content

    
