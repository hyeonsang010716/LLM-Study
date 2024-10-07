from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings


def get_answer(query):
    embedding =  OllamaEmbeddings(model="nomic-embed-text") # 임베딩 모델

    print(("vecotor 저장소 연결중"))
    vector_store = Chroma(
        embedding_function=embedding,
        persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
    )
    print(("vecotor 저장소 생성 완료"))

    ollama = Ollama(
        base_url="http://localhost:11434",
        model="llama3.2"
    )

    qachain = RetrievalQA.from_chain_type(ollama, retriever=vector_store.as_retriever())

    res = qachain.invoke({"query": query})

    return res['result']