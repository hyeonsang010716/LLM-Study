from langchain_upstage import ChatUpstage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, smart, kind, and efficient AI assistant. You always fulfill the user's requests to the best of your ability. You always answer succinctly. You must answer in Korean."),
    ("user", "{user_input}"),
    MessagesPlaceholder(variable_name="messages")
])

llm = ChatUpstage()

chain = prompt | llm | StrOutputParser()

if __name__ == "__main__":
    question = "한국의 수도는?"
    print(chain.invoke({"user_input": question, "messages": []}))
