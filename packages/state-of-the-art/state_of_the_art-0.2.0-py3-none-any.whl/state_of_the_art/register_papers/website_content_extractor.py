from typing import Tuple
from state_of_the_art.utils import pdf

class WebsiteContentExtractor:
    def get_website_title(self, url: str) -> str:
        from urllib.request import urlopen, Request
        from bs4 import BeautifulSoup

        req = Request(url=url, headers={"User-Agent": "Mozilla/5.0"})
        html = urlopen(req).read()

        soup = BeautifulSoup(html, features="html.parser")

        return soup.title.string if soup.title else url
    
    def get_website_content(self, url: str, cookies_string: str = None) -> Tuple[str, str]:
        from urllib.request import urlopen, Request
        from bs4 import BeautifulSoup

        req = Request(url=url, headers={"User-Agent": "Mozilla/5.0"})
        if cookies_string:
            req.add_header('Cookie', cookies_string)
        html = urlopen(req).read()

        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # get teh page title
        title = soup.title.string if soup.title else url

        return text, title

    def get_website_content_as_pdf(self, url: str) -> Tuple[str, str, str]:

        text, title = self.get_website_content(url)

        location = pdf.create_pdf(
            data=text, output_path_description="webpage " + title, disable_open=True
        )

        return text, title, location
