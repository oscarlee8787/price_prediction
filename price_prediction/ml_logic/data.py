import pandas as pd

def download_data():
    '''
    Takes a date (string in "%Y-%m-%d %H:%M:%S" format) as an input, calls 5 days of historic data from Binance API
    Outputs a dataframe
    '''


def load_data(filepath: str):
    '''
    Read data from the CSV file into a DataFrame
    Select specific columns from the DataFrame
    Set the 'Date' column as the index of the DataFrame
    Convert the index to datetime format
    '''
    data = pd.read_csv(filepath)
    data = data.loc[:,['Date','Open','High','Low','Close','Volume']]
    data = data.set_index('Date')
    data.index = pd.to_datetime(data.index,unit='ns')
    # something

    return data
