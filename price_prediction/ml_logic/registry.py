import os
import glob
from colorama import Fore, Style
from tensorflow import keras

def load_model(stage="Production"):
    """
    Return a saved model:
    locally for now


    - locally (latest one in alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'  --> for unit 02 only
    - or from MLFLOW (by "stage") if MODEL_TARGET=='mlflow' --> for unit 03 only

    Return None (but do not Raise) if no model is found

    """

    LOCAL_REGISTRY_PATH = os.path.join(os.path.expanduser('~'), "code", "oscarlee8787", "price_prediction", "models")

    print(Fore.BLUE + f"\nLoad latest model from local registry..." + Style.RESET_ALL)

    # Get the latest model version name by the timestamp on disk
    local_model_directory = os.path.join(LOCAL_REGISTRY_PATH, "btc_model")
    local_model_paths = glob.glob(f"{local_model_directory}/*")

    if not local_model_paths:
            return None

    most_recent_model_path_on_disk = sorted(local_model_paths)[-1]

    print(Fore.BLUE + f"\nLoad latest model from disk..." + Style.RESET_ALL)

    latest_model = keras.models.load_model(most_recent_model_path_on_disk)

    print("✅ Model loaded from local disk")

    return latest_model
