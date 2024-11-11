from langchain_core.prompts import ChatPromptTemplate
from langchain_upstage import ChatUpstage, UpstageEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers import EnsembleRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_community.retrievers import BM25Retriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from text import illad_text
from dotenv import load_dotenv

load_dotenv()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 150,
    chunk_overlap = 50,
)

text_documents = text_splitter.create_documents([illad_text])

vector_store = Chroma.from_documents(
    documents=text_documents ,embedding=UpstageEmbeddings(model="solar-embedding-1-large-passage")
)

db_retriever = vector_store.as_retriever()

bm25_retriever = BM25Retriever.from_texts(
    [doc.page_content for doc in text_documents]
)

ensemble_retriever = EnsembleRetriever(
    retrievers=[db_retriever, bm25_retriever], weights=[0.5, 0.5]
)

rag_prompt = ChatPromptTemplate.from_template(
    """
    Answer the question based only on the following context:
    {context}

Question: {question}
    """
)

llm = ChatUpstage()

rag_chain = (
    {"context": ensemble_retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

print(rag_chain.invoke("아가멤논이 꾼 꿈은?"))
