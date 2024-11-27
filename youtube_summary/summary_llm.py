from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_upstage import ChatUpstage
from typing import List, Dict, Annotated
from dotenv import load_dotenv

from get_news import get_news_context
load_dotenv()


llm = ChatUpstage()

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant specialized in summarizing news articles."
        "Please provide a concise summary of the given news article."
        "Make sure to include the main points and key information."
        "답변은 한국어로 해줘",
    ),
    ("human", "다음 뉴스 기사를 요약해줘:\n\n{context}"),
])

chain = prompt | llm | StrOutputParser()


def search_news_keyword(keyword: str):
    text = get_news_context(keyword)
    return chain.invoke({"context": text})

if __name__ == "__main__":
    keyword="폭설"
    print(search_news_keyword(keyword))