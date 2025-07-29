
from state_of_the_art.paper.arxiv_paper import ArxivPaper
from state_of_the_art.paper.paper_entity import Paper
import os
from state_of_the_art.utils import pdf
import requests
from state_of_the_art.config import config
from requests.adapters import HTTPAdapter, Retry


class PaperDownloader:
    def download_from_arxiv(self, paper: ArxivPaper, force_download=False) -> str:
        """
        Downloads a paper from arxiv
        """
        return self.download(
            paper.pdf_url, given_title=paper.title, force_download=force_download
        )

    def open_from_arxiv(self, paper: ArxivPaper):
        self.open(paper.pdf_url, title=paper.title)

    def download(self, pdf_url: str, force_download=False, given_title=None) -> str:
        """
        Downloads a paper from a given url
        :param url:
        :return:
        """

        if not pdf_url.startswith("http"):
            print("Not an http url spkipping download")
            return pdf_url
        
        if '/abs/' in pdf_url:
            raise Exception('Arxiv abstract url detected. YOu should use the pdf url instead')

        paper = Paper(pdf_url=pdf_url)
        print(f"Downloading paper from {paper.pdf_url}")
        destination = self._get_destination(pdf_url, title=given_title)

        if os.path.exists(destination):
            if "FORCE_DOWNLOAD" in os.environ or force_download:
                print("Force download is enabled so will download the file again")
                self.remove(destination)
            else:
                print(f"File {destination} already exists so wont download it again")
                return destination

        print(f"Downloading file {paper.pdf_url} to {destination}")

        self._download(pdf_url, destination)

        print("Downloaded file to ", destination)
        return destination

    def _get_destination(self, pdf_url, title=None):
        if title is None:
            title = pdf_url.split("/")[-1].replace(".pdf", "")
        return pdf.create_pdf_path("paper" + title, disable_timestamp=True)

    def remove(self, pdf_url):
        path = self._get_destination(pdf_url)
        if os.path.exists(path):
            os.remove(path)
            print(f"Removed file {path}")

    def open(self, pdf_url, title=None):
        path = self._get_destination(pdf_url, title=title)
        pdf.open_pdf(path)
        print(f"Opened file {path}")

    def _download(self, url, destination):
        session = requests.Session()
        USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
        session.headers['User-Agent'] = USER_AGENT
        retries = Retry(total=1, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
       
        http_adapter = HTTPAdapter(max_retries=retries)

        session.mount('http://', http_adapter)
        session.mount('https://', http_adapter)

        with session.get(url,stream=True, timeout=config.ARXIV_PAPER_DOWNLOAD_TIMEOUT) as r:
            r.raise_for_status()
            with open(destination, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        return destination



if __name__ == "__main__":
    import fire
    fire.Fire(PaperDownloader)
