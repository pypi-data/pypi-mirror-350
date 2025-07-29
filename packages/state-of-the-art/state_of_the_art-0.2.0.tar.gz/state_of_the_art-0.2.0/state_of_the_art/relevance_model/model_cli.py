

import os
from state_of_the_art.config import config
from state_of_the_art.relevance_model.model_utils import get_configured_mlflow

class ModelsCLI:
    def serve_mlflowui(self):
        print(f"Tracking URI: '{config.MLFLOW_TRACKING_URI}'")
        os.system(f" mlflow ui --port 8080 --backend-store-uri '{config.MLFLOW_TRACKING_URI}'")
    
    def save_for_inference(self):
        mlflow = get_configured_mlflow()
        #get Model by uuid
        run_id = "6014e6e959d448f4a30d76d8a4261f27"
        run = mlflow.get_run(run_id)
        uri = run.info.artifact_uri
        uri = uri.replace("file://", "")
        model_path = uri + "/model/data/model.pth"
        destination_path = config.TEXT_PREDICTOR_PATH_LOCALLY
        print(f"Copying {model_path} to {destination_path}")
        os.system(f"cp {model_path} {config.TEXT_PREDICTOR_PATH_LOCALLY}")

        print("Model copied successfully to local folder, to deploy it to the cloud run:  sota s3 push_model")





if __name__ == "__main__":
    import fire
    fire.Fire(ModelsCLI)
