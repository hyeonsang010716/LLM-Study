# DB 생성 (경로는 main에서 전달 받음)
import os
import pandas as pd
import sqlite3
import json
import faiss
import numpy as np


# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(current_dir)
DATA_PATH = os.path.join(root, "data", "Sample", "02.라벨링데이터")  #원하는 경로 (일단 한정해 두었음)
DB_PATH = os.path.join(root, "data", "qa_database.db") # 경로를 어디에 놓을까? (일단 data 모으는 곳에 두긴 했어)

max_length = 0


def load_json(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            data = json.load(file) # 전체 내용
    except FileNotFoundError:
        data = "파일을 찾을 수 없습니다."
    except json.JSONDecodeError:
        data = "유효하지 않은 JSON 형식입니다."
    return data


def get_keyword(data):
    global max_length

    key1 = set(data['question']['keyword'].split(","))
    key2 = set(data['answer']['keyword'].split(","))
    temp = set()
    for x in key1:
        temp.add(x.strip())
    for x in key1:
        temp.add(x.strip())
    keywords = ",".join(list(temp))

    # print(len(temp))

    if len(temp) > max_length:
        
        max_length = len(temp)
    
    return keywords


def read_json_files():
    question = []
    answer = []
    keywords = []

    # 디렉토리와 하위 디렉토리를 탐색
    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            # 파일 확장자가 .json인지 확인
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                print(f"{file_path} 읽는 중..")
                # JSON 파일 읽기
                data = load_json(file_path)
                # json파일에서 question / answer 쌍으로 추출
                keywords.append(get_keyword(data))
                question.append(data['context_summary']["summary_q"])
                answer.append(data['context_summary']["summary_a"])
                print(f"{file_path}읽기 완료")
                
    return keywords, question, answer


def create_db():
    print("Database 생성 중..")
    # 데이터베이스 연결 (이 객체를 이용해서 데이터베이스 접근이 가능)
    conn = sqlite3.connect(DB_PATH)
    if not os.path.isfile(DB_PATH):
        # 커서 생성 (커서는 DB 명령어를 사용할 때 필요)
        cursor = conn.cursor()

        # 테이블 생성 
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_pairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT,
            question TEXT,
            answer TEXT
        )
        ''')
    print("Database 생성 완료")

    return conn


def insert_data(conn, keywords, questions, answers):
    if not (len(questions) == len(questions) == len(answers)):
        print("The number of questions and the number of answers are different.")
        return 
    
    cursor = conn.cursor()

    for k, q, a in zip(keywords, questions, answers):  # 질문과 답변을 쌍으로 해서 추가
        cursor.execute('''
                       INSERT INTO qa_pairs (keyword, question, answer)
                       VALUES (?, ?, ?)
                       ''', (k, q, a))
        
    conn.commit()


def get_db_data():
    keywords, questions, answers = read_json_files() # 각각 질문 답변 데이터 수집
    db = create_db()
    insert_data(db, keywords, questions, answers)
    

    query = "SELECT keyword, question, answer FROM qa_pairs"
    df = pd.read_sql_query(query, db)

    return questions, answers, df
    
    # 전체 데이터가 적으면 더 빠른 방법
    # cursor = conn.cursor()
    # cursor.execute("SELECT question, answer FROM qa_pairs")
    # qa_pairs = cursor.fetchall() 
 

def search_db_data(text):
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT * FROM qa_pairs WHERE keyword LIKE '%{text}%';"
    df = pd.read_sql_query(query, conn)
    
    return df


def get_questions():
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT question FROM qa_pairs;"
    df = pd.read_sql_query(query, conn)
    result = df['question'].tolist()
    
    return result


def get_answers():
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT answer FROM qa_pairs;"
    df = pd.read_sql_query(query, conn)
    result = df['answer'].tolist()
    
    return result


if __name__ == "__main__":
    # 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(current_dir)
    dir_path = os.path.join(root, "data", "Sample", "02.라벨링데이터")  #원하는 경로 (일단 한정해 두었음)
    db_path = os.path.join(root, "data", "qa_database.db") # 경로를 어디에 놓을까? (일단 data 모으는 곳에 두긴 했어)

    data = get_db_data()
    print(data)

    print(get_questions())
#    print(len(data)) # 35200 총 데이터의 양 (dataframe)
#    print(data.iloc[0])

    #keyword_search = search_db_data("향상", db)
    #print(keyword_search)