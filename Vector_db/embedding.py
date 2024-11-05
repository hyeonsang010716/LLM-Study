# DB 경로를 받고 접근해서 임베딩 후 키워드와 유사한 값 리스트로 리턴
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('paraphrase-MiniLM-L12-v2') # Sentence-BERT 모델 로드

def get_embedding(questions):# 질문 전부를 임베딩하기
    print("질문 임베딩 중..")
    qustion_vectors = model.encode(questions)

    # 질문 벡터의 차원 확인
    vector_dimension = len(qustion_vectors[0])
    #Faiss index 생성
    index = faiss.IndexFlatL2(vector_dimension)
    # 인덱스에 벡터 추가
    index.add(np.array(qustion_vectors).astype('float32'))
    print("질문 임베딩 완료")

    return index


def search_qa(query, index, k=5):
    print("질문 검색 중..")
    # 질문(query)를 vector로 변환
    query_vector = model.encode([query])

    # distances는 query와 가장 가까운 값의 유사도
    # indices는 query와 가장 가까운 값의 인덱스 값
    distances, indices = index.search(np.array(query_vector).astype('float32'), k)
    print("답변 5개 생성")
    return indices
