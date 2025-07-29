from state_of_the_art.paper.arxiv_paper import ArxivPaper
from state_of_the_art.paper.paper_downloader import PaperDownloader
from state_of_the_art.paper.paper_entity import Paper
from state_of_the_art.register_papers.register_paper import PaperCreator
from state_of_the_art.register_papers.website_content_extractor import WebsiteContentExtractor
from state_of_the_art.utils import pdf
import os


def is_pdf_url(url) -> bool:
    return url.endswith(".pdf") or ArxivPaper.is_arxiv_url(url)


def get_content_from_url(url):
    if os.environ.get("SOTA_TEST"):
        return "Test content", "Test title", "test.pdf"

    if is_pdf_url(url):
        return get_pdf_content(url)

    return WebsiteContentExtractor().get_website_content_as_pdf(url)


def get_pdf_content(url):
    if ArxivPaper.is_arxiv_url(url):
        paper = ArxivPaper(abstract_url=url)
        PaperCreator().register_if_not_found(url)
        paper = ArxivPaper.load_paper_from_url(paper.abstract_url)
        paper_title = paper.title
    else:
        paper = Paper(pdf_url=url)
        paper_title = url.split("/")[-1].replace(".pdf", "")
    print("Paper title: ", paper_title)

    local_location = PaperDownloader().download(paper.pdf_url, given_title=paper_title)
    paper_content = pdf.read_content(local_location)

    return paper_content, paper_title, local_location
