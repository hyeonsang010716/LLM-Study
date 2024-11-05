import streamlit as st
import pandas as pd
import numpy as np
import os


title = st.text_input(
    label="질문을 입력해주세요",
    placeholder=""
)
st.write(f"당신이 입력한 질문: :violet[{title}]")  # violet은 색상 지정