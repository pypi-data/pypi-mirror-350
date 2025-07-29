from state_of_the_art.paper.arxiv_paper import ArxivPaper
from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.paper.url_sanitizer import UrlSanitizer
from state_of_the_art.register_papers.arxiv_miner import ArxivMiner


class PaperCreator:
    def __init__(self):
        self.papers = []

    def is_paper_registered(self, url):
        return PapersLoader().is_paper_url_registered(url)

    def register_if_not_found(self, url: str):
        if self.is_paper_registered(url):
            return

        self.register_arxiv_paper_by_url(url)

    def register_arxiv_paper_by_url(self, url: str):
        """
        Register an arxiv paper by its url.
        use CustomArticleCreator to register a custom paper.
        """
        url = UrlSanitizer().sanitize(url)
        ArxivMiner().register_by_id(ArxivPaper.id_from_url(url))
        if url.endswith("v1"):
            url = url[:-2]
        
        if "/pdf/" in url:
            url = url.replace("/pdf/", "/abs/")

        return url
