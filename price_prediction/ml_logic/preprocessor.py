import numpy as np

def split_data(data, target_column='Close', split_ratio=0.8):
    """
    Split the given data into training and testing sets based on the specified split ratio.

    Parameters:
    - data (pandas.DataFrame): The input data.
    - target_column (str): The name of the target column. Default is 'Close'.
    - split_ratio (float): The ratio for the train-test split. Default is 0.8.

    Returns:
    - train_data (pandas.DataFrame): Training data.
    - test_data (pandas.DataFrame): Testing data.
    """

    # Set the Target column
    aim = target_column

    # Determine the index for the split
    split_index = int(len(data) * split_ratio)

    # Split the data into training and testing sets
    train_data = data.iloc[:split_index]
    test_data = data.iloc[split_index:]

    return train_data, test_data


# Function to normalize a continuous variable to a zero-base scale
def normalise_zero_base(continuous):
    """
    Normalize a continuous variable to a zero-base scale.
    Parameters:
    - continuous (pandas.Series): The continuous variable to be normalized.
    Returns:
    - pandas.Series: The normalized continuous variable.
    """
    # Normalize by dividing each value by the first value and subtracting 1
    return continuous / continuous.iloc[0] - 1


# Function to turn the normalized number back to an actual value
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


# Function to extract windowed data from a continuous variable
def extract_window_data(continuous, window_len=5, zero_base=True):
    """
    Extract windowed data from a continuous variable.
    Parameters:
    - continuous (pandas.Series): The continuous variable to extract windows from.
    - window_len (int, optional): The length of each window (default is 5).
    - zero_base (bool, optional): Whether to normalize each window to a zero-base scale (default is True).
    Returns:
    - numpy.ndarray: Array of windowed data.
    Example:
    >>> windowed_data = extract_window_data(data['Close'], window_len=10, zero_base=True)
    """
    # Initialize an empty list to store windowed data
    window_data = []

    # Iterate over the continuous variable to extract windows
    for idx in range(len(continuous) - window_len):
        # Extract a window of data
        tmp = continuous[idx: (idx + window_len)].copy()

        # Normalize the window to a zero-base scale if specified
        if zero_base:
            tmp = normalise_zero_base(tmp)

        # Append the window data to the list
        window_data.append(tmp.values)

    # Convert the list of windowed data to a numpy array
    return np.array(window_data)


def prepare_data(train_data, test_data, continuous, aim, window_len=10, zero_base=True, test_size=0.2):
    """
    Prepare data for time series analysis.
    Parameters:
    - continuous (pandas.Series): The continuous variable for time series analysis.
    - aim (str): The target variable to predict.
    - window_len (int, optional): The length of each window (default is 10).
    - zero_base (bool, optional): Whether to normalize each window to a zero-base scale (default is True).
    - test_size (float, optional): The proportion of data to be used as the test set (default is 0.2).
    Returns:
    - tuple: A tuple containing train_data, test_data, X_train, X_test, y_train, y_test.
    """
    # Extract windowed data for training and testing sets
    X_train = extract_window_data(train_data, window_len, zero_base)
    X_test = extract_window_data(test_data, window_len, zero_base)

    # Extract target variable for training and testing sets
    y_train = train_data[aim][window_len:].values
    y_test = test_data[aim][window_len:].values

    # Normalize the target variable to a zero-base scale if specified
    if zero_base:
        y_train = y_train / train_data[aim][:-window_len].values - 1
        y_test = y_test / test_data[aim][:-window_len].values - 1

    # Return the prepared data
    return train_data, test_data, X_train, X_test, y_train, y_test
