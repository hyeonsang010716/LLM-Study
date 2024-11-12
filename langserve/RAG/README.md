# RAG: 데이터를 더욱 똑똑하게 활용하는 생성형 AI

## 개요

최근 AI의 발전으로 대화형 모델들이 폭넓게 사용되고 있지만, 이 모델들은 최신 정보에 접근하기 어렵다는 한계를 갖고 있습니다. RAG(검색 기반 생성)는 이러한 문제를 해결하기 위해 고안된 방법론입니다. 이번 블로그에서는 RAG가 무엇인지, 그 원리와 장점을 설명하고, 실제 구현 방법을 예시로 보여드리겠습니다.

## RAG란 무엇인가?

RAG는 대규모 언어 모델(LLM)이 특정한 질문에 답할 때 필요한 관련 데이터를 실시간으로 검색하여 생성 결과의 정확성을 높이는 방법입니다. 일반적인 언어 모델은 훈련 데이터에 포함된 정보에 의존하여 응답을 생성하지만, RAG는 외부 데이터베이스나 문서에서 필요한 정보를 가져와 답변의 신뢰도를 높이는 것이 특징입니다.

## RAG의 원리

RAG의 작동 방식은 크게 두 단계로 나뉩니다:

- 검색 단계: 사용자가 입력한 질문과 관련된 정보를 데이터베이스에서 검색합니다. 이때 BM25나 Ensemble 같은 Retriever를 사용해서 관련성이 높은 문서를 찾아냅니다.
- 생성 단계: 검색된 문서를 기반으로 언어 모델이 최종 답변을 생성합니다. 이 과정에서는 검색된 문서의 내용을 요약하거나 특정 정보를 추출하여 답변의 질을 높입니다.
## RAG 구현
RAG 구현은 Text 등의 데이터를 document 객체로 변환하고 이를 Embedding해서 Vector Store에 저장하게 됩니다. 여기에 Chain을 연결하여 활용하게 됩니다.
### Text 등의 데이터 변환
이 포스트에서는 Text 형식 변환만 다룹니다.
- 아래 텍스트는 Wikipedia에서 발췌한 일리아스의 요약 일부분입니다.
``` python
text = """
아가멤논은 제우스가 보낸 꿈에서 트로이아가 함락되는 것을 본다. 이 꿈이 무엇을 뜻하는지 아가멤논은 장군들과 토론 끝에, 전체 군사회의를 소집한다. 네스토르와 오디세우스는 열띤 논쟁을 벌이며, 아카이아군은 트로이 정복을 포기하고 귀향하자는 의견에 마음이 솔깃해지지만, 신들의 영향하에 있는 오뒷세우스의 강한 반대와 건의에 따라 트로이군과 빨리 결전을 치르자는 데에 합의를 본다. 시의 후반(484-877 이른바 전함 카탈로그)은 전쟁에 참가한 아카이아군과 트로이아군의 지방, 도시 그리고 지휘관들을 노래하고 있다."""
 ```
- 이렇게 Text 형식의 데이터를 청크(Chunk) 단위로 나누어 저장합니다.
``` python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
chunk_size=300,# 청크 사이즈를 조절
chunk_overlap=50, # 청크 사이의 겹치는 부분의 크기를 조절
)
# document객체로 변환: create_documents는 List[str]의 형태를 요구함
text_document = text_splitter.create_documents([text])
``` 
> 청크 사이즈를 조절하며 ```print(text_documents[0])```를 이용하여 청크의 의미를 확인하셔도 좋습니다.
## Embedding 모델 호출
Embedding 모델은 여러 종류가 존재하는데 여기서는 Upstage의 solar-embedding-1-large-passage 모델을 사용합니다.
> Embedding 모델을 사용하기 위해서 API KEY가 필요합니다. 다음 링크에 들어가 회원가입 후 가져오시면 됩니다. https://console.upstage.ai/docs/getting-started/quick-start
```python
from langchain_upstage import UpstageEmbeddings

# 임베딩 모델 호출
passge_embedding = UpstageEmbeddings(model="solar-embedding-1-large-passage")
# documents 임베딩
embed_texts = passge_embedding.embed_documents([text])
embed_texts[0] # Text를 임베딩 한 결과값
```
## Vector Store 생성
Vector Store는 Chroma를 사용합니다.
- Vector Store는 documents 객체와 embedding 모듈을 arguments로 요구합니다.
 - 위의 코드를 이용하여 전달합니다.
```python
from langchain_chroma import Chroma

db = Chroma.from_documents(
    documents=text_documents, embedding=passge_embedding, collection_name="my_db"
)

db.get()
```
## Retriever
Retriever는 Vector Store에서 효과적인 검색을 지원하는 도구입니다.
```python
# DB 자체 리트리버 확인
db_retriever = db.as_retriever()

docs = db_retriever.invoke("아가멤논이 꾼 꿈은?")
docs
```
- Ensemble Retriever를 사용하여 Chroma 자체 Retriever와 BM25 Retriever를 결합하여 이용합니다.
```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

bm25_retriever = BM25Retriever.from_texts(text) # BM25 리트리버
bm25_retriever.k = 2 # 검색은 2개 까지 확인

ensemble_retriever = EnsembleRetriever(
    retrievers=[db_retriever, bm25_retriever], weights=[0.5, 0.5] # 각 리트리버의 가중치를 설정

docs = ensemble_retriever.invoke("아가멤논이 꾼 꿈은?")
docs
```
## RAG 체인 생성
retriever와 RunablePassthrough를 사용하여 Rag Chain을 구성합니다
- RunablePassthrough는 입력을 그대로 전달하는 역할을 수행합니다.
- context는 LLM이 답변을 잘 할 수 있도록 도우는 문맥 정보입니다.
```python
from langchain_core.runnables import RunnablePassthrough

rag_prompt = ChatPromptTemplate.from_template(
    """
    Answer the question based only on the following context:
{context}

Question: {question}
    """
)
rag_chain = (
    {"context": ensemble_retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

rag_chain.invoke("아가멤논이 꾼 꿈은?")
```
| 최종 결과를 확인하면 답변이 잘 나오는 것을 알 수 있습니다.