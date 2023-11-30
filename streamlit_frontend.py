import streamlit as st
import numpy as np
import pandas as pd
import datetime

def set_bg_color():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #ADD8E6;  # You can change this hex color as you want
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to set the background color
set_bg_color()

st.markdown("""# Crypto Price Prediction
## for Bitcoin, Ethereum & Litecoin
""")

d = st.date_input(
    "Please enter a date starting from today to 14 days into the future",
    datetime.date.today())
    #datetime.date(2023, 12, 8))
st.write('Your birthday is:', d)
