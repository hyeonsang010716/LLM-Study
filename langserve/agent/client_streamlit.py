import asyncio
import streamlit as st
from langserve import RemoteRunnable

async def main():
    remote_runnable = RemoteRunnable("https://progressive-fionna-uh3135-d5472958.koyeb.app/")

    st.title("Chat Bot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    if prompt := st.chat_input("Input user query"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            ai = await remote_runnable.ainvoke({
                "input": prompt,
                "chat_history": st.session_state.messages[:-1]
            })
            response = ai["output"]
            st.markdown(response)
            
        st.session_state.messages.append({"role": "assistant", "content": response})
asyncio.run(main())
