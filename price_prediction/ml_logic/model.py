from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Dropout, LSTM
import numpy as np
from colorama import Fore, Style

'''
# Define parameters for data preparation and LSTM model
Needs to be stored somewhere else, just saving it here for now

window_len = 5
test_size = 0.2
zero_base = True
lstm_neurons = 50
epochs = 20
batch_size = 32
loss = 'mse'
dropout = 0.24
optimizer = 'adam'
output_size = 1
'''

# Function to build an LSTM (Long Short-Term Memory) model
def build_lstm_model(input_data, output_size, neurons, activ_func='linear',
                     dropout=0.2):
    """
    Build an LSTM (Long Short-Term Memory) model.
    Parameters:
    - input_data (numpy.ndarray): The input data for the model.
    - output_size (int): The size of the output layer.
    - neurons (int): The number of neurons in the LSTM layer.
    - activ_func (str, optional): Activation function for the output layer (default is 'linear').
    - dropout (float, optional): Dropout rate to prevent overfitting (default is 0.2).

    Returns:
    - tensorflow.keras.models.Sequential: The constructed LSTM model.
    """
    # Create a Sequential model
    model = Sequential()

    # Add an LSTM layer with the specified number of neurons and input shape
    model.add(LSTM(neurons, input_shape=(input_data.shape[1], input_data.shape[2])))

    # Add a Dropout layer to prevent overfitting
    model.add(Dropout(dropout))

    # Add a Dense layer with the specified number of units
    model.add(Dense(units=output_size))

    # Add an Activation layer with the specified activation function
    model.add(Activation(activ_func))

    print("✅ Model compiled")

    # Return the constructed LSTM model
    return model


def compile_model(model, loss='mse', optimizer='adam'):
    '''
    Compile the model with the specified loss function and optimizer
    - loss (str, optional): Loss function for model training (default is 'mse' - Mean Squared Error).
    - optimizer (str, optional): Optimization algorithm for model training (default is 'adam').
    '''

    model.compile(loss=loss, optimizer=optimizer)

    print("✅ Model compiled")

    return model


def train_model(model, X, y, validation_data: tuple, epochs=20, batch_size=16, shuffle=False):
    """
    Fit the model and return a tuple (fitted_model, history)
    validation_data has to be a tuple as (X_val, y_val)

    """
    history = model.fit(X,
                        y,
                        validation_data=validation_data,
                        epochs=epochs,
                        batch_size=batch_size,
                        shuffle=shuffle)

    print(f"✅ Model trained on {len(X)} rows with min val loss: {round(np.min(history.history['val_loss']), 2)}")

    return model, history


def evaluate_model(model, X, y):
    """
    Evaluate trained model performance on the dataset
    """

    print(Fore.BLUE + f"\nEvaluating model on {len(X)} rows..." + Style.RESET_ALL)

    if model is None:
        print(f"\n❌ No model to evaluate")
        return None

    metrics = model.evaluate(
        x=X,
        y=y,
        return_dict=True
    )

    loss = metrics["loss"]
    mae = metrics["mae"]

    print(f"✅ Model evaluated, loss: {round(loss, 2)}")

    return metrics
