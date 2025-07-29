import datetime
from typing import Optional

from state_of_the_art.paper.arxiv_paper import ArxivPaper
from state_of_the_art.register_papers.website_content_extractor import WebsiteContentExtractor

class CustomArticleCreator:
    def __init__(self, disable_tags: bool = False):
        self.disable_tags = disable_tags

    def create(self, paper_url: str, title: Optional[str] = None) -> str:
        """
        Creates a new paper and returns the paper id
        """
        if ArxivPaper.is_arxiv_url(paper_url):
            raise ValueError("Arxiv paper not supported")

        if not title:
            title = WebsiteContentExtractor().get_website_title(paper_url)

        from state_of_the_art.tables.paper_table import PaperTable

        paper_table = PaperTable()
        papers_df = paper_table.read()
        if paper_url in papers_df["abstract_url"].values:
            raise ValueError(f"Article url {paper_url} already exists")
        if title in papers_df["title"].values:
            raise ValueError(f"Article title {title} already exists")

        today = datetime.datetime.now()
        paper_id = paper_table.add(
            abstract_url=paper_url, title=title, published=today, institution=""
        )
        if not self.disable_tags:
            from state_of_the_art.tables.tags_table import TagsTable
            tags_table = TagsTable()
            tags_table.add_tag_to_paper(paper_url, "Manually Created")
        return paper_id
    

if __name__ == "__main__":
    import fire
    fire.Fire(CustomArticleCreator(disable_tags=True))
