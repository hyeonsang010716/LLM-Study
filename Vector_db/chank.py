from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

import os


# 주소 설정
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
data_path = os.path.join(parent_dir, "Sample")
assets_path = os.path.join(parent_dir, "assets")
text_path = os.path.join(assets_path, "total_text.txt")

print("text file 읽는 중")

# Load text file
with open(text_path, encoding="UTF-8") as f:
    my_txt_file = f.read()

print("text file 읽기 완료")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400, # 담을 문장 크기
    chunk_overlap=20, # 얼마나 문장끼리 겹치게 할 것인가
    length_function=len, # 전체 길이를 기준으로 청크를 나눔
    is_separator_regex=False,  # 일반 문자열을 구분자로 사용
)

print("text split 중")
text_document = text_splitter.create_documents([my_txt_file]) # list 형태로 text를 나누어서 전달해줌
length = len(text_document)
print("text split 완료")


print("embedding 모델 불러오는 중")
# embedding = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
embedding =  OllamaEmbeddings(model="nomic-embed-text") # 임베딩 모델
print("embedding 모델 불러오기 완료")

print(("vecotor 저장소 생성중"))
vector_store = Chroma(
    embedding_function=embedding,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

for i in range(10, length, 10):
    vector_store.add_documents(text_document[i-10:i])
    print(f"{i}/{length} 완료") 
print(("vecotor 저장소 생성 완료"))