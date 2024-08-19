from azure.search.documents import SearchClient
import json
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
from text_embedder.text_embed import TextEmbedder
text_embedder = TextEmbedder()
def get_relevant_memory(query: str):

    with open('config.json','r') as file:
        config = json.load(file)

    search_client = SearchClient(endpoint=config["SEARCH_ENDPOINT"],index_name=config["MEMORY_INDEX_NAME"], credential=AzureKeyCredential(config["SEARCH_ADMIN_KEY"]))
    vector_query = VectorizedQuery(
        vector=text_embedder.embed_content(query), k_nearest_neighbors=3, fields="contentVector"
    )
    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        select=['content'],
    )
    documents = []
    for result in results:
        documents.append(result)

    return documents



