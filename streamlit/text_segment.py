import streamlit as st

# 아래처럼 streamlit은 마크다운으로 사용이 가능
# 각각 타이틀 헤더 캡션 코드 보이기 등등으로 표현
st.title("Title")
st.header("Header")
st.caption("caption")

sample_code = '''
def function():
    print(hello)
'''
st.code(sample_code, language="Python")

