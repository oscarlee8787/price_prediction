import pandas as pd
import requests
from datetime import datetime
from datetime import timedelta
from google.cloud import storage
from io import StringIO
from pei



def download_data(endtime:str, symbol:str, interval:str, limit=5):
    '''
    Takes a date as an input,
    converts to millisecond,
    calls 5 days of historic data from Binance API
    creates a dataframe with 'Date', 'Open','High','Low','Close','Volume' as columns
    saves the dataframe to Google Cloud Storage under 'data-wrangling'
    endtime: str in "%Y-%m-%d %H:%M:%S" format
    symbol examples: BTCUSDT, ETHUSDT
    interval examples: 1d, 1h, 1m
    '''

    root_url = 'https://api.binance.com/api/v3/'

    check_url = root_url + 'ping'

    if requests.get(check_url).ok != True: #calls the ping endpoint of Binance to check if the api is working
        print('Issue with Binance API general connectivity, did not fetch data')
        return 1

    dt_obj = datetime.strptime(endtime,'%Y-%m-%d')
    next_day = dt_obj + timedelta(days=1) #adds one day so we get 5 days from Binance API, with input day as the last day
    millisec = int(next_day.timestamp() * 1000) #converts the date/time from string to milliseconds that the api requires

    params = {'endTime':millisec,
              'interval':interval,
              'symbol':symbol,
              'limit':limit
              }
    kline_url = root_url + 'klines'

    if requests.get(url=kline_url, params=params).ok != True:
        print('Issue with Binance API kline connectivity, did not fetch data')
        return 1

    data = requests.get(url=kline_url, params=params).json()

    df = pd.DataFrame(data)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume',
              'k_close_time', 'quote_asset_volume', 'num_trades',
              'taker_base_vol', 'taker_quote_vol', 'ignore']
    for col in ['Open', 'High', 'Low', 'Close', 'Volume',
                'quote_asset_volume', 'num_trades',
                'taker_base_vol', 'taker_quote_vol', 'ignore']:
        df[col] = df[col].astype(float)

    client = storage.Client()
    bucket = client.bucket('data-wrangling')
    blob = bucket.blob(f'BTC-USD_{endtime}.csv')
    blob.upload_from_string(df.to_csv(index=False), content_type='text/csv')

    return 0


def load_data(filepath: str):
    '''
    THIS FUNCTION IS WORKING WITH CSV DOWNLOADED FROM YAHOO FINANCE
    Read data from the CSV file into a DataFrame
    Select specific columns from the DataFrame
    Set the 'Date' column as the index of the DataFrame
    Convert the index to datetime format
    '''
    data = pd.read_csv(filepath)
    data = data.loc[:,['Date','Open','High','Low','Close','Volume']]
    data = data.set_index('Date')
    data.index = pd.to_datetime(data.index,unit='ns')

    return data


def load_binance_data_from_gcloud(coin, endtime):
    '''
    Goes to google cloud storage data-wrangling bucket
    Reads data from the DataFrame downloaded with Binance api
    Select specific columns from the DataFrame
    Set the 'Date' column as the index of the DataFrame
    Convert the index to datetime format
    '''
    client = storage.Client()
    bucket = client.bucket('data-wrangling')
    blob = bucket.blob(f'BTC-USD_{endtime}.csv')
    content = blob.download_as_text()
    # Convert CSV content to a pandas DataFrame
    df = pd.read_csv(StringIO(content))

    df = df.loc[:,['Date','Open','High','Low','Close','Volume']]
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index,unit='ms')
    #something to commit
    return df
