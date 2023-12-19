# Crypto Price Pattern Prediction
Crypto Price Pattern Prediction is a deep learning algorithm that recognizes recurring price movement patterns in crypto trading history and makes a prediction of the most likely price movements in a future period.

Original feature and model exploration are done in Jupyter notebook in notebooks folder.



## Model
#### _Current:_
LSTM

#### _Future:_
- 1D-Convolution
- LLM
- HiSTGNN



## Feature engineering
Features include daily Open, Close, High, Low, and Volume of a specific coin. The time series of data from 2015-2023 is split into multiple periods that are 5 days long. Then, each 5-day window is normalized individually, as change relative to the first day, the first day always being 0. Target variables are the sixth day. Prediction is made by inputing a five-day long series and the output target is the sixth day. The target is then unnormalized to return the actual number instead of relative change to the first day.



## Front- and backend
Interface built with streamlit (https://magicrypto.streamlit.app/). Image environment built with Docker and deployed on Google Cloud Platform.



#### Website

<img width="1463" alt="Screen Shot 2023-12-16 at 10 26 21 PM" src="https://github.com/oscarlee8787/price_prediction/assets/73566517/ed85bb41-e149-4282-b38f-8269358c712b">

<img width="1451" alt="Screen Shot 2023-12-16 at 10 27 58 PM" src="https://github.com/oscarlee8787/price_prediction/assets/73566517/e3969664-44ed-434d-9a16-4fc143b352f1">



## Training data source
BTCUSD daily k-line data from Yahoo Finance. Dates: 2015-2023



## Known issues
1. Model trained on BTCUSD daily k-line from _Yahoo_, but prediction on frontend is based on BTCUSD daily k-line from _Kraken's api_
2. Package used to call current data from Binance api. However, api stopped working when deployed to GCP. Workaround calls data from Kraken's api directly through the Streamlit interface. Hence:
    - our api doesn't work without the frontend
    - predictions might be unprecise because of different data sources
