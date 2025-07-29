from typing import Iterator
from state_of_the_art.infrastructure.datadog_utils import send_metric, setup_datadog
from state_of_the_art.infrastructure.shell import ShellRunner
from state_of_the_art.tables.changelog_table import Changelog
from state_of_the_art.tables.data_sync_table import PushHistory
from state_of_the_art.config import config
import os

class S3:
    def __init__(self):
        setup_datadog(disable_exception=True)
        
    def list_buckets(self) -> None:
        os.system("aws s3api list-buckets")

    def list_content(self) -> None:
        os.system(f"aws s3 ls s3://{config.data_bucket}")

    def validate_credentials(self) -> None:
        if os.path.exists(f"{config.HOME}/.aws/credentials"):
            print("Using credentials from ~/.aws/credentials")
            return

        if os.environ.get("SOTA_TEST"):
            print("Test mode, not validating credentials")
            return
        else:
            print("Using credentials from env variables")

        if not os.environ.get("AWS_ACCESS_KEY_ID"):
            raise Exception("AWS_ACCESS_KEY_ID not set")
        if not os.environ.get("AWS_SECRET_ACCESS_KEY"):
            raise Exception("AWS_SECRET_ACCESS_KEY not set")
        if not os.environ.get("AWS_DEFAULT_REGION"):
            raise Exception("AWS_DEFAULT_REGION not set")

    def sync_local_to_s3(self) -> None:
        """
        Syncronizes the data from the local tinydatawerehouse_events folder to the s3 bucket
        """
        Changelog().add_log("Start pushing data to s3")

        self.validate_credentials()
        cmd = f"aws s3 sync {config.TINY_DATA_WAREHOUSE_EVENTS} s3://{config.data_bucket}/tinydatawerehouse_events"
        if os.environ.get("SOTA_TEST"):
            print(f"Test mode, not pushing to s3 cmd {cmd}")
            return
        else:
            print(f"Actual mode, s3 with command {cmd}")

        result = ShellRunner().run_waiting(cmd)
        print(result)
        PushHistory().add()
        print("Pushed to s3")
        send_metric(metric="sota.push_data_to_s3.success", value=1)
        Changelog().add_log("Pushed data to s3")


    def pull_data(self) -> None:
        """
        Pulls data from s3 to local tinydatawerehouse_events folder using the sync command 
        """
        for i in self.pull_data_iterator():
            print(i)

    def pull_data_iterator(self) -> Iterator[str]:
        self.validate_credentials()
        DESTINATION = config.TINY_DATA_WAREHOUSE_EVENTS

        yield "Using destination: " + DESTINATION

        if os.environ.get("SOTA_TEST"):
            print(f"Test mode, not pulling from s3 cmd {shell_cmd}")
            return

        if os.path.exists(DESTINATION):
            yield f"Path {DESTINATION} already exists so removing it"
            yield ShellRunner().run_waiting(f"rm -rf {DESTINATION}/")

        yield ShellRunner().run_waiting(f"mkdir -p {DESTINATION}")

        shell_cmd = f"aws s3 sync s3://{config.data_bucket}/tinydatawerehouse_events {DESTINATION}"
        yield ShellRunner().run_waiting(shell_cmd)

    def push_model(self) -> None:
        """ 
        Pushes our single model to s3
        """
        shell_cmd = f"aws s3 cp {config.TEXT_PREDICTOR_PATH_LOCALLY} s3://{config.data_bucket}/models/ "
        result = ShellRunner().run_waiting(shell_cmd)
        print("Model pushed to s3")
        return result

    def pull_models(self) -> str:
        if not os.path.exists(config.MODELS_PATH_LOCALLY):
            os.system("mkdir -p " + config.MODELS_PATH_LOCALLY)

        shell_cmd = f"aws s3 cp {config.MODEL_FOLDER_IN_CLOUD} {config.MODELS_PATH_LOCALLY} --recursive"
        result = ShellRunner().run_waiting(shell_cmd)
        assert os.path.exists(config.MODELS_PATH_LOCALLY), "Models folder not found"
        print("Model pulled from s3")
        return result

    def copy_article_to_s3(self, file_path: str) -> None:
        shell_cmd = f"aws s3 cp {file_path} s3://{config.ARTICLES_BUCKET}/"
        result = ShellRunner().run_waiting(shell_cmd)
        print("Article copied to s3")
        return result
