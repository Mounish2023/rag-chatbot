import azure.functions as func
import logging
import io
import PyPDF2
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from text_embedder.text_embed import TextEmbedder
text_embedder = TextEmbedder()
from Indexing.index_documents import index_documents
from userQuery_blueprint import userQuery_blueprint
from DataProcessing_blueprint import DataProcessing_blueprint


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

app.register_functions(DataProcessing_blueprint)

app.register_functions(userQuery_blueprint)





