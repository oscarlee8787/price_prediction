import os
import requests
from colorama import Fore, Style

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


from tensorflow import keras

from price_prediction.ml_logic.params import *
from price_prediction.ml_logic.data import  load_data_from_binance ,download_data
from price_prediction.ml_logic.preprocessor import split_data, normalise_zero_base, denormalize_zero_base, extract_window_data, prepare_data
from price_prediction.ml_logic.model import build_lstm_model, compile_model, train_model, evaluate_model
from price_prediction.ml_logic.registry import load_model




def load_or_download_data(path):
    if not os.path.exists(path):
        download_data(path)
    return load_data_from_binance(path)


def predict_data(data, model_name, model_path, future_predictions=5):
    split_ratio = 0.8
    time_steps = 5
    X_train, y_train, X_test, y_test = split_data(data, split_ratio)

    train_data = prepare_data(X_train, y_train, time_steps)
    test_data = prepare_data(X_test, y_test, time_steps)

    trainX, trainY = extract_window_data(train_data, time_steps)
    testX, testY = extract_window_data(test_data, time_steps)

    normalise_zero_base(trainX, trainY, testX, testY)

    trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
    testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))

    if not os.path.exists(model_path):
        model = build_lstm_model(model_name)
        compile_model(model)
        train_model(model, trainX, trainY)
        model.save(model_path)
    else:
        model = load_model(model_path)

    evaluate_model(model, testX, testY)

    predictions = []
    for _ in range(future_predictions):
        x = np.zeros((1, time_steps, 1))
        x[0, :, 0] = testX[-1]
        prediction = model.predict(x)[0]
        predictions.append(prediction)
        testX = np.vstack((testX, x))

    denormalize_zero_base(testY, predictions)

    return predictions  # Return the denormalized predictions

def main():
    data_path = "data/crypto_data.csv"
    model_name = "LSTM"
    model_path = "saved_models/lstm_model.h5"

    data = load_or_download_data(data_path)
    predicted_sequence = predict_data(data, model_name, model_path)
    print(predicted_sequence)

if __name__ == "__main__":
    main()
