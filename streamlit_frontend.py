import streamlit as st
import numpy as np
import pandas as pd
import datetime
import yfinance as yf
import matplotlib
matplotlib.use("Agg")  # Agg is a non-interactive backend that should work with Streamlit
import matplotlib.pyplot as plt
# import plotly.graph_objs as go
import requests
from price_prediction.ml_logic.data import download_data


# BACKGROUND COLOR --------------------------------------------------------------------
#def set_bg_color():
#    st.markdown(
#        f"""
 #       <style>
#        .stApp {{
#            background-color: #ADD8E6;  # You can change this hex color as you want
 #       }}
#        </style>
#        """,
 #       unsafe_allow_html=True
 #   )

def set_bg_from_url(url):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url({url});
            background-size: cover;
        }}
        </style>
        """, unsafe_allow_html=True)

set_bg_from_url("https://elements-video-cover-images-0.imgix.net/files/9ae69261-0ac4-43b2-9f39-7ecc51579ade/inlin[…]in&h=394&w=700&s=9c4ce31d5ac33b74260261ea42407aa3")





# Call the function to set the background color
#set_bg_color()

# HEADERS ------------------------------------------------------------------------------
st.markdown("""# Crypto Price Prediction
## for Bitcoin, Ethereum & Litecoin
""")

d = st.date_input(
    "Please enter a date",
    datetime.date.today())
    #datetime.date(2023, 12, 8))

d_str = str(d)
j = download_data(endtime=d_str, symbol='BTCUSDT', interval='1d')
st.write(j)
# DROP DOWN MENU -----------------------------------------------------------------------

# List of options for the dropdown
options = ["please select", "Bitcoin"]
#, "Ethereum", "Litecoin"]

# Creating the dropdown menu
selected_option = st.selectbox("Please choose a curreny to get your prediction:", options)

coin = None

if selected_option == "Bitcoin":
    coin = 'BTC-USD'

#if selected_option == "Ethereum":
 #   coin = 'ETH-USD'

#if selected_option == "Litecoin":
   # coin = 'LTC-USD'

# Fetching the current price

def get_current_price(coin):
    stock = yf.Ticker(coin)
    todays_data = stock.history(period='1d')
    return todays_data['Close'][0]

if coin != None:

    current_price = get_current_price(coin)
    st.write(f'Current price of {selected_option} ({coin}): ${current_price:.2f}')


# SHOW THE CHART! ----------------------------------------------------------------------

# Function to fetch and plot stock data


# def plot_stock(coin):
#     # Load stock data
#     data = yf.download(coin, start=datetime.date.today()-datetime.timedelta(days=90), end=datetime.date.today())

#     # Plotting
#     fig = go.Figure()
#     fig.add_trace(go.Candlestick(x=data.index,
#                 open=data['Open'],
#                 high=data['High'],
#                 low=data['Low'],
#                 close=data['Close'],
#                 name='market data'))

#     fig.update_layout(title=f'{coin}',
#                       xaxis_rangeslider_visible=False)
#     st.plotly_chart(fig, use_container_width=True)

# if coin != None:
#     plot_stock(coin)

# converting DATE to UNIX milliseconds ------------------------------------------------------

#def convert_date_to_unix_milliseconds(date_str):
    # Parse the date string to datetime object
    # Assuming the date string format is yyyy%mm%dd
 #   date_obj = datetime.strptime(date_str, '%Y%%m%%d')

    # Convert the datetime object to Unix timestamp in seconds
  #  unix_timestamp = datetime.timestamp(date_obj)

    # Convert Unix timestamp to milliseconds
   # unix_milliseconds = int(unix_timestamp * 1000)

    #return unix_milliseconds

#convert_date_to_unix_milliseconds(d)

#st.write(d_milli)

# Example usage
#date_string = "2023%11%30"
#unix_milliseconds = convert_date_to_unix_milliseconds(date_string)
#print(f"Unix Time in milliseconds: {unix_milliseconds}")

# Adding one day to the current date
next_day = d + datetime.timedelta(days=1)

# SENDING REQUEST TO OUR FAST API ------------------------------------
params = dict(
    X=d)

if coin != None:
    url = 'https://wednesday-wgsxngkdcq-oe.a.run.app/predict'  # FastAPI server URL
    response = requests.get(url, params=params).json()
    st.write(f''' ## The Bitcoin price prediction for {next_day} is: {response["price_prediction"]}''')
