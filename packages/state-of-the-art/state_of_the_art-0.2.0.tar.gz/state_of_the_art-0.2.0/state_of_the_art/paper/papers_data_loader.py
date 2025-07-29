from typing import List, Optional, Union

from state_of_the_art.paper.arxiv_paper import ArxivPaper
import pandas as pd
import datetime
from state_of_the_art.config import config
from state_of_the_art.paper.paper_entity import Paper


class PapersLoader:
    TITLE_MAX_LENGH = 80

    def load_papers_df(self) -> pd.DataFrame:
        df = config.get_datawarehouse().event("arxiv_papers")
        # @todo Fix duplicates
        df.drop_duplicates(subset=["abstract_url"], keep="first", inplace=True)

        return df

    def get_all_papers(self) -> List[ArxivPaper]:
        df = self.load_papers_df().sort_values(by="published", ascending=False)
        return self.from_pandas_to_paper_list(df)

    def from_pandas_to_paper_list(self, df) -> List[ArxivPaper]:
        papers = []
        for i in df.iterrows():
            if ArxivPaper.is_arxiv_url(i[1]["abstract_url"]):
                papers.append(ArxivPaper.load_from_dict(i[1].to_dict()))
            else:
                papers.append(Paper.load_from_dict(i[1].to_dict()))
        return papers
    
    def load_last_n_days(self, days=7) -> pd.DataFrame:
        end =  datetime.date.today()
        start = (datetime.datetime.now() - datetime.timedelta(days=days)).date()

        return self.load_between_dates(start=start, end=end)

    def load_between_dates(self, start: datetime.date, end: datetime.date) -> pd.DataFrame:
        df = self.load_papers_df()
        return df[
            (df["published"].dt.date >= start) & (df["published"].dt.date <= end)
        ].sort_values(by="published", ascending=False)

    def load_from_url(self, url) -> Optional[pd.DataFrame]:
        papers = self.load_papers_df()
        result = papers[papers["abstract_url"] == url]
        return result

    def load_from_partial_url(self, url) -> pd.DataFrame:
        papers = self.load_papers_df()
        match = papers[papers["abstract_url"].str.contains(url)]

        print(f"While searching by partial url match found {match}")

        return match

    def load_from_urls(
        self, urls: List[str], as_dict=False, fail_on_missing_ids=True
    ) -> pd.DataFrame:
        urls = list(set(urls))
        papers = self.load_papers_df()
        if as_dict:
            result = {}
            for url in urls:
                result[url] = papers[papers["abstract_url"] == url]
            result_len = len(result.keys())
        else:
            result = papers[papers["abstract_url"].isin(urls)]
            result_len = len(result)

        if result_len != len(urls):
            message = f"""
                Found {len(result)} papers but expected {len(urls)}
                Missing urls: {[i for i in urls if i not in result['abstract_url'].to_list()]}
"""
            if fail_on_missing_ids:
                raise ValueError(message)
            else:
                print(message)

        return result

    def load_papers_from_urls(self, urls: List[str]) -> List[ArxivPaper]:
        papers = self.load_from_urls(urls, as_dict=True)
        result = []
        for i in urls:
            if not papers[i].to_dict(orient="records"):
                print("No data for ", i)
                continue

            paper_dict = papers[i].to_dict(orient="records")[0]
            if ArxivPaper.is_arxiv_url(paper_dict["abstract_url"]):
                entity = ArxivPaper.load_from_dict(paper_dict)
            else:
                entity = Paper.load_from_dict(paper_dict)
            result.append(entity)
        return result

    def is_paper_url_registered(self, url: str) -> bool:
        try:
            result = self.load_from_partial_url(url)
            return True if not result.empty else False
        except BaseException as e:
            print("Could not find paper from url ", url, e)
            return False

    def load_paper_from_url(self, url: str) -> ArxivPaper:
        if not url:
            raise Exception("Url not defined to load any paper")

        result = self.load_from_partial_url(url)
        if result.empty:
            raise Exception(f"Could not find paper from url {url}")

        arxiv_data = result.to_dict(orient="records")[0]
        print("Arxiv data ", arxiv_data)
        if not ArxivPaper.is_arxiv_url(url):
            return Paper(pdf_url=arxiv_data["abstract_url"], title=arxiv_data["title"])

        result = ArxivPaper.load_from_dict(arxiv_data)
        if not result:
            raise Exception(f"Could not find paper from url {url}")

        return result

    def load_paper_from_id(self, id: str) -> Optional[Paper]:
        df = self.load_papers_df()
        result = df[df["tdw_uuid"] == id]
        if result.empty:
            return None

        if ArxivPaper.is_arxiv_url(result.to_dict(orient="records")[0]["abstract_url"]):    
            return ArxivPaper.load_from_dict(result.to_dict(orient="records")[0])
        else:
            return Paper.load_from_dict(result.to_dict(orient="records")[0])

    def df_to_papers(self, papers_df) -> List[ArxivPaper]:
        """
        Converts a dataframe to papers
        """
        papers_dict = papers_df.to_dict(orient="records")
        result = []
        for i in papers_dict:
            try:
                paper = ArxivPaper.from_dict(i)
                result.append(paper)
            except Exception as e:
                print("Error converting to paper ", i, e)

        return result
