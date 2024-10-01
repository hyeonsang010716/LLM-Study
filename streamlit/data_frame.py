import streamlit as st
import pandas as pd
import numpy as np
import os
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(current_dir)
path = os.path.join(root, "data", "Sample", "01.원천데이터", "국정감사", "16", "SRC_16대_2000_2000년10월20일_국정감사_교육위원회_0001(030043)")  #원하는 경로 (일단 한정해 두었음)

df = pd.read_excel(path + ".xlsx")
print(df.shape[1])

# dataframe 호출
# use_container_width == width를 넓히는 방법 (streamlit) 
st.dataframe(df, use_container_width=False)

# csv 다운로드도 가능하게
st.download_button(
    label="csv로 다운로드",
    data=df.to_csv(),
    file_name="SRC_16대_2000_2000년10월20일_국정감사_교육위원회_0001",
    mime='text/csv'
)

# 파일 업로드 버튼 (업로드 기능)
file = st.file_uploader("파일 선택(csv or excel)", type=['csv', 'xls', 'xlsx'])

# if Path(file).suffix == '.xlsx':
#     # csv 파일로 저장합니다
#     csv_file = 'output_file.csv'
#     file.to_csv(csv_file, index=False)


# 파일이 정상 업로드 된 경우
if file is not None:
    # 파일 읽기
    up_df = pd.read_csv(file)
    # 출력
    st.dataframe(up_df)