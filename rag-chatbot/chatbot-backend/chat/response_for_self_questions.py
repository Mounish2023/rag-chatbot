from openai import OpenAI
from typing import List
from chat.prompts import response_for_self_questions_system_prompt
from jinja2 import Template

def self_response_from_llm(query: str):
    
    client = OpenAI()
    completion=client.chat.completions.create(
        messages=[
            {"role": "system", "content": response_for_self_questions_system_prompt },
            {"role": "user", "content": query},
        ],
        model="gpt-3.5-turbo"
    )


    return completion.choices[0].message.content