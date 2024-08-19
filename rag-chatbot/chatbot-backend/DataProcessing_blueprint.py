# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(DataProcessing_blueprint) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import azure.functions as func
import logging
import io
import PyPDF2
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from text_embedder.text_embed import TextEmbedder
text_embedder = TextEmbedder()
from Indexing.index_documents import index_documents
from chunking.chunk import text_chunker

DataProcessing_blueprint = func.Blueprint()


@DataProcessing_blueprint.route(route="DataProcessing", auth_level=func.AuthLevel.ANONYMOUS)
def DataProcessing(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    response = ""
    file = req.files.get('file')
    if file:
        # Read the file content
        file_content = file.stream.read()  # file_content is now a byte string
        
        # Convert byte string to a readable PDF file object using io.BytesIO
        pdf_file = io.BytesIO(file_content)
        
        # Use PyPDF2 to read the PDF file object
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            logging.info(f"the number of pages is {num_pages}")
            logging.info(f"the first page is {pdf_reader.pages[0].extract_text()}")
            # pdf_df = pd.DataFrame(columns = ['pageContent','pageNumber'])
            all_rows = []
            for index, page in enumerate(pdf_reader.pages):
                
                all_rows.append({
                "pageContent" : page.extract_text(),
                "pageNumber" : index + 1
                })
        except Exception as e:
            logging.info(f"Failed to read PDF file. Error: {str(e)}", status_code=500)
            # pdf_df = pd.concat([pdf_df, pd.DataFrame(all_rows)],ignore_index=True)

            # pdf_dict = pdf_df.to_dict()


        chunked_rows = text_chunker(all_rows=all_rows)

        doc = text_embedder.embed_content(chunked_rows)

        #doc is [{pageContent :, pageNumber: , embedding:},{},{}]
        if doc:
            response = index_documents(doc)
            logging.info(f" the response is {response}")
        else:
            logging.info(f"the doc is empty")

                            
        return func.HttpResponse(f"{response}")
    else:
        return func.HttpResponse(f"the file not received correctly")




