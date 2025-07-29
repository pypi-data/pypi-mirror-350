from state_of_the_art.container_startup import ContainerStartup
from state_of_the_art.infrastructure.s3 import S3
from state_of_the_art.paper.paper_downloader import PaperDownloader
from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.insight_extractor.insight_extractor import AIInsightsExtractor
from state_of_the_art.register_papers.arxiv_miner import ArxivMiner
from state_of_the_art.ci_cd import Cli
from state_of_the_art.relevance_model.model_cli import ModelsCLI
from state_of_the_art.tables.tables import Table
from state_of_the_art.recommenders.recommender_pipeline import MainRecommenderPipeline


class Sota:
    """
    State of the art via ai main entry script
    """

    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()

        self.papers = PapersLoader()
        self.InsightExtractor = AIInsightsExtractor
        self.downloader = PaperDownloader
        self.ArxivMiner = ArxivMiner
        self.cicd = Cli
        self.s3 = S3
        self.modelscli = ModelsCLI
        self.container_startup = ContainerStartup
        self.table = Table
        self.MainRecommenderPipeline = MainRecommenderPipeline


def main():
    import fire

    fire.Fire(Sota)


if __name__ == "__main__":
    main()
