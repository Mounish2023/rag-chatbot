# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(userQuery_blueprint) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import azure.functions as func
import logging
from chat.get_knowledge_from_index import get_relevant_documents
from chat.final_response_llm_tool import final_response_from_llm
from chat.get_relevant_memory import get_relevant_memory
from chat.transform_query_llm_tool import transform_query_llm
from chat.classify_self_questions_llm_tool import classify_self_questions_llm
from chat.put_memory_into_index import upload_memory_into_index
from chat.response_for_self_questions import self_response_from_llm
from chat.managing_output import final_output

userQuery_blueprint = func.Blueprint()


@userQuery_blueprint.route(route="userQuery", auth_level=func.AuthLevel.ANONYMOUS)
def userQuery(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    query = req.params.get('query')
    if not query:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            query = req_body.get('query')
    
    

    chat_history = get_relevant_memory(query=query)

    transformed_query = transform_query_llm(query=query,prev_history_documents=chat_history)

    
    query_bool = classify_self_questions_llm(query=transformed_query)
    answer = {}
    chitchat_response = {}
    if not int(query_bool):
        documents = get_relevant_documents(query=query)

        answer = final_response_from_llm(query=query,documents=documents,prev_history_documents=chat_history)

        uploaded = upload_memory_into_index(query=query, answer=answer)
        logging.info(f'{uploaded}')

    else:

        chitchat_response = self_response_from_llm(query=query)

    final_response =  final_output(answer_for_trivia=chitchat_response, answer_for_user_question=answer)

    if final_response:
        return func.HttpResponse(body=str(final_response),status_code=200, mimetype="text/plain")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a query in the query string or in the request body for a personalized response.",
             status_code=200
        )