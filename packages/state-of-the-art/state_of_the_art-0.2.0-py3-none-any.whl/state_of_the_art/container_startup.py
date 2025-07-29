from state_of_the_art.infrastructure.datadog_utils import send_metric, setup_datadog
from state_of_the_art.infrastructure.s3 import S3
from state_of_the_art.tables.text_feedback_table import TextFeedbackTable


class ContainerStartup:
    def __init__(self) -> None:
        setup_datadog()
        self.pull_models = S3().pull_models
        self.pull_events_data = S3().pull_data_iterator

    def run_during_startup(self):
        """
        Downloads all the necessary depenedencies for the container
        """
        print(f"Setting up container ")
        print("Downloading ntlk")
        self.download_ntlk()
        self.pull_models()

        print("Pulling data from S3")
        for log in self.pull_events_data():
            print(log)
        

    def download_ntlk(self):
        print("Downloading ntlk")
        import nltk

        nltk.download("wordnet")


if __name__ == "__main__":
    import fire

    fire.Fire()
