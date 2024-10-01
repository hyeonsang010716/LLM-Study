import streamlit as st
import time
import os
from openai import OpenAI
import random
from dotenv import load_dotenv

# # Open ai 세팅
# load_dotenv() # .env 파일 로드
# api_key = os.getenv("API_KEY") # 환경 변수에서 API 키 불러오기

# client = OpenAI(api_key=st.secrets[api_key])  # API 키 저장
# if "openai_model" not in st.session_state: # 기본 모델 설정
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# 대답 방식
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# 채팅 서비스 이름 설정
st.title("Simple chat")

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# # 새로 고침 시 이전에 있던 채팅 기록 가져오기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 유저 입력 = 변수 prompt
if prompt := st.chat_input("What is up?"):
    # 유저 메시지 기록에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 유저 메시지를 보여주기
    with st.chat_message("user"): # user가 보낸 응답이라는 의미
        st.write(prompt)

    

    # stream = client.chat.completions.create(
    #         model=st.session_state["openai_model"],
    #         messages=[
    #             {"role": m["role"], "content": m["content"]}
    #             for m in st.session_state.messages
    #         ],
    #         stream=True,
    #     )

    answer = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(answer))
    
    # 메시지 기록에 담기
    st.session_state.messages.append({"role": "assistant", "content": response})
