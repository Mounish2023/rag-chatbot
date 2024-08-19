from azure.search.documents import SearchIndexingBufferedSender
import json
from azure.core.credentials import AzureKeyCredential
import uuid
from text_embedder.text_embed import TextEmbedder
text_embedder = TextEmbedder()

def upload_memory_into_index(query: str, answer: str):
    with open('config.json','r') as file:
        config = json.load(file)
    unique_id = uuid.uuid4()
    Q_and_A = "user: "+ query + "\n" + "Assistant: "+ answer
    doc = {
        "id": str(unique_id),
        "content": Q_and_A,
        "contentVector": text_embedder.embed_content(Q_and_A)
    }
    with SearchIndexingBufferedSender(endpoint=config["SEARCH_ENDPOINT"],index_name=config["MEMORY_INDEX_NAME"],credential=AzureKeyCredential(config["SEARCH_ADMIN_KEY"])) as batch_client:
        batch_client.upload_documents(documents=[doc])

        return f"Conversation uploaded to memory index"