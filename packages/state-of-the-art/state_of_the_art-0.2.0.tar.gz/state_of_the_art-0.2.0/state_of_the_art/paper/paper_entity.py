import datetime
from typing import Optional
from state_of_the_art.config import config
import pandas as pd


class Paper:
    """
    Base paper abstration
    """

    def __init__(self, *, pdf_url: Optional[str] = None, abstract_url: Optional[str] = None, title: Optional[str] = None, id: Optional[str] = None, published: Optional[datetime.date] = None, abstract: Optional[str] = None):
        self.pdf_url = pdf_url
        self.abstract_url = pdf_url if pdf_url else abstract_url
        self.title = title if title else ""
        self.abstract = abstract if abstract else ""
        self.published = published
        self.id = id
        if pdf_url and not pdf_url.endswith(".pdf"):
            self.pdf_url += ".pdf"

    def exists_in_db(self, url):
        print(f"Checking if paper {url} exists in db")
        from state_of_the_art.paper.papers_data_loader import PapersLoader

        result = PapersLoader().load_from_url(url)
        if result.empty:
            return False
        return True

    def get_destination(self):
        file_name = self.get_filename()
        return f"{config.NEW_PAPERS_FOLDER}/{file_name}"

    def get_filename(self):
        return self.pdf_url.split("/")[-1]

    def published_date_str(self):
        return ""


    def has_published_date(self):
        # test if is a pandas timestamp date
        return type(self.published) == pd.Timestamp or type(self.published) == datetime.date
    
    def get_published_date(self):
        if type(self.published) == pd.Timestamp:
            return self.published.date()
        return self.published

    @classmethod
    def load_from_dict(cls, data: dict) -> "Paper":
        if "abstract_url" not in data:
            raise Exception(f"Abstract url not found in {data}")
        if "published" not in data:
            raise Exception(f"Published date not found in {data}")
        if "title" not in data:
            raise Exception(f"Title not found in {data}")

        return cls(
            abstract_url=data["abstract_url"],
            published=data["published"],
            title=data["title"],
            abstract=data.get("abstract", ""),
            id=data.get("tdw_uuid", None),
        )
