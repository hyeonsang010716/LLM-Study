import os
import sql_db
import embedding
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(current_dir)
dir_path = os.path.join(root, "data", "Sample", "02.라벨링데이터", "국정감사", "16")  #원하는 경로 (일단 한정해 두었음)
db_path = os.path.join(root, "data", "qa_database.db") # 경로를 어디에 놓을까? (일단 data 모으는 곳에 두긴 했어)

# sql DB 생성
questions, answers = sql_db.read_json_files(dir_path) # 각각 질문 답변 데이터 수집

db = sql_db.create_db(db_path)
sql_db.insert_data(db, questions, answers)
data = sql_db.get_db_data(db)

# embedding
index = embedding.get_embedding(questions)

query = "최근에 두 지검 검사장이 이 사건의 변호인으로 선임되고 하니까 점점 부산지검은 다대ㆍ만덕사건에 관한 한 처음부터 수사를 못 하게 되어 있는 사건이다, 내가 아까 말한 대로 국정감사 때마다 요구하고 추궁하고 또 감사원 감사가 착수되고 하니까 할 수 없이 등 떠밀려서 마지못해서 하는 것 아니냐 하는 것입니다.  수사진은 왜 교체했습니까?"
indices = embedding.search_qa(query, index)

# print(type(indices)) #np.ndarray (2차원)

for i in indices[0]:
    print(f"질문 : {questions[i]}")
    print(f"답변 : {answers[i]}")
    print()
    