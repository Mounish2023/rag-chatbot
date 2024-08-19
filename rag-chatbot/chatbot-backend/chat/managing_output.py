import json

def final_output(answer_for_trivia: dict, answer_for_user_question:dict):
    if answer_for_trivia:
        return answer_for_trivia
    else:
        return answer_for_user_question
    