from langchain_core.tools import tool
from langchain.tools.retriever import create_retriever_tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_upstage import UpstageEmbeddings, ChatUpstage
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os
load_dotenv()

dir_path = os.path.dirname(os.path.abspath(__file__))
text_path = os.path.join(dir_path, "assets")

text = []
with open(text_path+"/total_text.txt", "r", encoding="utf-8") as f:
    text.append(f.read())

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=50,
)

text_documents = text_splitter.create_documents(text)

embeddings = UpstageEmbeddings(model="solar-embedding-1-large-passage")

db = Chroma.from_documents(
    documents=text_documents, embedding=embeddings
)
db_retriever = db.as_retriever()

retriever_tool = create_retriever_tool(
    db_retriever,
    name="text_search",
    description="to use this tool to search information from the text"
)

search_tool = TavilySearchResults(k=5)

tools = [retriever_tool, search_tool]

llm = ChatUpstage()

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant."
        "Make sure to use the `retriever_tool` tool for searching information from the text."
        "If you can't find the information from the text, use the `search_tool` tool for searching information from the web.",
    ),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
