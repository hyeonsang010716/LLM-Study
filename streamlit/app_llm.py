import Vector_DB 
import streamlit as st
import time
import os
from openai import OpenAI
import random
from dotenv import load_dotenv
import embedding


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

    answer = embedding.get_answer(prompt)

    print(answer)

    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(answer))
    
    # 메시지 기록에 담기
    st.session_state.messages.append({"role": "assistant", "content": response})


