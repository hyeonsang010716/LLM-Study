import os
from .sql_db import *
from .embedding import *


def get_answer(query):
    # sql DB 생성
    questions, answers, data = get_db_data() # 각각 질문 답변 데이터 수집

    # embedding
    index = get_embedding(questions)

    indices = search_qa(query, index)

    result = []

    for i in indices[0]:
        result.append((questions[i], answers[i]))

    return result
    
        