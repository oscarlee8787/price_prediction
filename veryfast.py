import pandas as pd

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
# app.state.model = load_model()

# http://127.0.0.1:8000/predict?prediction_date=2023-11-05
@app.get("/predict")

def predict(
        prediction_date: str,  # 2023-11-05
    ):
    """
    Make a single price prediction.
    Assumes `prediction_date` is provided as a string by the user in "%Y-%m-%d %H:%M:%S" format

    """

    # 💡 Optional trick instead of writing each column name manually:
    # locals() gets us all of our arguments back as a dictionary
    X_pred = pd.DataFrame(locals(), index=[0])

    # Convert to US/Eastern TZ-aware ... or EUROPE??
    X_pred['prediction_date'] = pd.Timestamp(prediction_date, tz='US/Eastern')

    model = app.state.model
    assert model is not None

    X_processed = preprocess_features(X_pred)
    y_pred = model.predict(X_processed)

    return dict(price_prediction = float(y_pred)) #HERE WE NEED DO SEE WHAT OUR MODEL PREDICTS: Price or Logistic??

@app.get("/")
def root():

    return dict(greeting="Hello Crypto Price Prediction")
