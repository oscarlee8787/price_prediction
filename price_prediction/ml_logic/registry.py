import os
import glob
from colorama import Fore, Style
import tensorflow as tf

def load_model(stage="Production"):
    """
    Return a saved model:
    locally for now


    - locally (latest one in alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'  --> for unit 02 only
    - or from MLFLOW (by "stage") if MODEL_TARGET=='mlflow' --> for unit 03 only

    Return None (but do not Raise) if no model is found

    """

    file_path = os.path.join(os.path.dirname(__file__), "..", "models", "btc_model_2", "btc_model_3.h5")

    print(Fore.BLUE + f"\nLoad latest model from local registry..." + Style.RESET_ALL)

    # Get the latest model version name by the timestamp on disk
#    local_model_directory = os.path.join(file_path, "btc_model")
 #   local_model_paths = glob.glob(f"{local_model_directory}/*")

  #  if not local_model_paths:
   #         return None

    most_recent_model_path_on_disk = sorted(local_model_paths)[-1]

    print(Fore.BLUE + f"\nLoad latest model from disk..." + Style.RESET_ALL)

    latest_model = tf.saved_model.load(most_recent_model_path_on_disk)

    print("✅ Model loaded from local disk")

    return latest_model
