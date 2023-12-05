import os
import pandas as pd
import numpy as np
from tensorflow import keras
from price_prediction.ml_logic.preprocessor import normalise_zero_base, denormalize_zero_base
from price_prediction.ml_logic.data import download_data, load_data_from_binance


#from price_prediction.ml_logic.registry import load_model #LOAD PRICE MODEL
#from price_prediction.ml_logic.preprocessor import preprocess_features #PREPROCESS INSERTED DATA

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# 💡 Preload the model to accelerate the predictions

app.state.model = keras.models.load_model(os.path.join(os.path.dirname(__file__), "..", "models", "btc_model_2", "btc_model_3.h5"))

@app.get("/predict")
def predict(X):
    """
    X is provided as a string by the user in "%Y-%m-%d" format from the streamlit frontend.

    Takes a date as an input
    calls 5 days of historic data before the input date from Binance API
    uses that as the input for the prediction function
    makes a prediction for the day after the input.

    Date sample: 2023-11-07
    """
    model = app.state.model
    assert model is not None

    #api_data = download_data(endtime=X, symbol='BTCUSDT', interval='1d')
    #      sample date: '2023-11-07 08:00:00'
    download_data(endtime=X, symbol='BTCUSDT', interval='1d')


    data = load_data_from_binance()

    df_normed = normalise_zero_base(data)
    df_array = np.array(df_normed)
    # becuz the model takes an array as an input
    df_array = np.expand_dims(df_array, axis=0)
    # and the array needs to have a shape of (1,5,5)

    preds = model.predict(df_array)[0][0]
    # the model outputs a normalized number

    diff_pred = denormalize_zero_base(preds,data['Close'][0])
    # which needs to be denormalized by this function

    y_pred = data['Close'][0] + diff_pred
    # the number we got is the price difference from the first of the 5-day window, so we add it back to the first day

    return dict(price_prediction = float(y_pred)) #HERE WE NEED DO SEE WHAT OUR MODEL PREDICTS: Price or Logistic??


@app.get("/")
def root():

    return dict(greeting="Hello Crypto Price Prediction")
