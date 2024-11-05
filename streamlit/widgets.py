import streamlit as st
import pandas as pd

# make button and click event
button = st.button("click the button")

if button:
    st.write("selected btn")

# checkbox