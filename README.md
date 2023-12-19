# Crypto Price Pattern Prediction
Crypto Price Pattern Prediction is a deep learning algorithm that recognizes recurring price movement patterns in crypto trading history and makes a prediction of the most likely price movements in a future period.


## Front- and backend
Interface built with streamlit (https://magicrypto.streamlit.app/). Image environment built with Docker and deployed on Google Cloud Platform.


#### Website
![[Screen Shot 2023-12-16 at 10.26.21 PM 1.png]]

![[Screen Shot 2023-12-16 at 10.27.58 PM.png]]

## Training data sourced
BTCUSD daily k-line data from Yahoo Finance


## Model
#### _Current:_
LSTM

#### _Future:_
1D-Convolution, LLM, HiSTGNN


## Known issues
1. Model trained on BTCUSD daily k-line from _Yahoo_, but prediction on frontend is based on BTCUSD daily k-line from _Kraken's api_
2. Package used to call current data from Binance api. However, api stopped working when deployed to GCP. Workaround calls data from Kraken's api directly through the Streamlit interface. Hence:
    - our api doesn't work without the frontend
    - predictions might be unprecise because of different data sources
