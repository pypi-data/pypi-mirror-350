from state_of_the_art.paper.arxiv_paper import ArxivPaper
from state_of_the_art.paper.paper_downloader import PaperDownloader
from state_of_the_art.paper.paper_entity import Paper
from state_of_the_art.utils.mail import EmailService


class EmailAPaper:
    KINDE_EMAIL = 'machado.jean.kindle_new@kindle.com'

    def __init__(self):
        self.downloader = PaperDownloader()

    def send(self, paper: Paper) -> str:

        # test if instance is ArxivPaper
        if isinstance(paper, ArxivPaper):
            destination = self.downloader.download_from_arxiv(paper)
        else:
            destination = self.downloader.download(paper.abstract_url)


        result = EmailService().send(
            content=None,
            subject=paper.title,
            attachment=destination,
            recepient=self.get_destination_email(),
        )

        EmailService().send(
            content=None,
            subject=paper.title,
            attachment=destination,
            recepient=self.KINDE_EMAIL,
        )

        return result
