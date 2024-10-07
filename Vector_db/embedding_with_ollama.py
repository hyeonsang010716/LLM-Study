from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os

# 주소 설정
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 
data_path = os.path.join(parent_dir, "Sample")
assets_path = os.path.join(parent_dir, "assets")
text_path = os.path.join(assets_path, "total_text.txt")

print(parent_dir)

# Load text file
with open(text_path, encoding="UTF-8") as f:
    my_txt_file = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400, # 담을 문장 크기
    chunk_overlap=20, # 얼마나 문장끼리 겹치게 할 것인가
    length_function=len, # 전체 길이를 기준으로 청크를 나눔
    is_separator_regex=False,  # 일반 문자열을 구분자로 사용
)

text_document = text_splitter.create_documents([my_txt_file]) # list 형태로 text를 나누어서 전달해줌

embedding =  OllamaEmbeddings(model="nomic-embed-text")# 임베딩 모델
vectorstores = Chroma.from_documents(documents=text_document, embedding=embedding)

query = "선거구별 단속실적과 선거구별 형사입건대상 분류에 대한 자료를 요청하였습니다. 이 자료를 전남도청 국감이 끝나기 전까지 제출 가능한지 확인하고, 또 경찰청과 지방 경찰청의 정원과 현원 차이에 대한 이유를 설명해주십시오."
docs = vectorstores.similarity_search(query)
print(docs)