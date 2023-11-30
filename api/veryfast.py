import pandas as pd
from tensorflow import keras
from ml_logic.preprocessor import *


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
app.state.model = models.load_model('/Users/johannes_macbookpro/code/oscarlee8787/price_prediction/models/btc_model/saved_model.pb')

data_dummy = pd.read_csv('/Users/johannes_macbookpro/code/oscarlee8787/price_prediction/raw_data/BTC-USD_dummy.csv')

data_dummy = data_dummy.loc[:,['Date','Open','High','Low','Close','Volume']]

data_dummy = data_dummy.set_index('Date')
data_dummy.index = pd.to_datetime(data_dummy.index,unit='ns')

dummy_normed = normalise_zero_base(data_dummy)

dummy_array = np.array(dummy_normed)

dummy_array = np.expand_dims(dummy_array, axis=0)



def denormalize_zero_base(normalized, initial_value):
    """
    Denormalize a zero-base normalized continuous variable.
    Parameters:
    - normalized (pandas.Series): The normalized continuous variable to be denormalized.
    - initial_value (float): The initial value before normalization.
    Returns:
    - pandas.Series: The denormalized continuous variable.
    """
    # Denormalize by multiplying each value by the initial value + 1
    return normalized * (initial_value + 1)



@app.get("/predict")
def predict(
        X=dummy_array
    ):
    """
    Make a single price prediction.
    Assumes `prediction_date` is provided as a string by the user in "%Y-%m-%d %H:%M:%S" format

    """
    # 💡 Optional trick instead of writing each column name manually:
    # locals() gets us all of our arguments back as a dictionary
    #X_pred = pd.DataFrame(locals(), index=[0])

    # Convert to US/Eastern TZ-aware ... or EUROPE??
    #X_pred['prediction_date'] = pd.Timestamp(prediction_date, tz='US/Eastern')

    model = app.state.model
    #assert model is not None

    preds_dummy = model.predict(X)[0][0]

    diff_pred = denormalize_zero_base(preds_dummy,37796.792969)

    y_pred = data_dummy['Close'][0] + diff_pred

    return dict(price_prediction = float(y_pred)) #HERE WE NEED DO SEE WHAT OUR MODEL PREDICTS: Price or Logistic??

@app.get("/")
def root():

    return dict(greeting="Hello Crypto Price Prediction")
