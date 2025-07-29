
from state_of_the_art.config import config

def get_configured_mlflow():
    import mlflow
    mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
    mlflow.set_experiment("relevance_model")
    return mlflow
