from openai import OpenAI
import logging
import json
from typing import List

class TextEmbedder():
    
    def clean_text(self,text:str):
        text = text.replace("\n","")
        return text
    
    def embed_content(self,text: List[dict] | str):
        # [{},{}]
        with open('config.json','r') as file:
            config = json.load(file)
        logging.info(f" config file is {config}")
        client = OpenAI()

        logging.info(f" the client is {client}")
        logging.info(f"the text is {text}")
        if isinstance(text, str):
            page_content = self.clean_text(text)
            # logging.info(f"the content is {page_content}")
            response = client.embeddings.create(input=[page_content], model="text-embedding-3-small")
            # logging.info(f"the response is {response}")
            embedding = response.data[0].embedding
            return embedding
        else:
            for doc in text:
                # logging.info(f"the pageContent before sending {doc}")
                page_content = self.clean_text(doc["pageContent"])
                # logging.info(f"the content is {page_content}")
                response = client.embeddings.create(input=[page_content], model="text-embedding-3-small")
                # logging.info(f"the response is {response}")
                embedding = response.data[0].embedding
                doc["embedding"] = embedding

        return text



