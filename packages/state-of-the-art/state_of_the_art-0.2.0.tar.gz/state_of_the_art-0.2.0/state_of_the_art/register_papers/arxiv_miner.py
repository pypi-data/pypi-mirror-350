from typing import Iterator, List, Literal
from state_of_the_art.config import config
from state_of_the_art.infrastructure.datadog_utils import send_metric, setup_datadog
from state_of_the_art.paper.arxiv_paper import ArxivPaper
from tqdm import tqdm
import datetime
import logging

from state_of_the_art.register_papers.arxiv_gateway import ArxivGateway, SORT_TYPE_ANNOTATION
from state_of_the_art.tables.changelog_table import Changelog
from state_of_the_art.tables.mine_history import ArxivMiningHistory
from state_of_the_art.utils.internet import has_internet


class ArxivMiner:
    """
    Looks at arxiv api for papers
    """

    SORT_COLUMN: SORT_TYPE_ANNOTATION = "submitted"

    def __init__(self):
        self.config = config
        tdw = config.get_datawarehouse()
        arxiv_papers = tdw.event("arxiv_papers")
        self.existing_papers_urls = (
            arxiv_papers["abstract_url"].values if not arxiv_papers.empty else []
        )
        self.tdw = config.get_datawarehouse()
        self.existing_papers_urls = self._load_existing_papers_urls()
        self.arxiv_gateway = ArxivGateway()
        self.KEYWORDS_TO_MINE = config.QUERIES_TO_MINE
        setup_datadog(disable_exception=True)

    def mine_all_keywords(self, dry_run=False, keyword=None, number_of_papers_per_keyword=100) -> Iterator[str]:
        """
        Register all papers by looking in arxiv api with the keywords of the audience configuration

        Its an iterator, so it will yield one by one, you need to iterate over it to get all the papers
        :param dry_run:
        :param disable_relevance_miner:
        :return:
        """
        print(f"Mining {number_of_papers_per_keyword} papers for each keyword")
        if dry_run:
            yield "Dry run, just printing, not registering them"
        send_metric(metric="scheduler.mine_all_keywords.started", value=1)
        Changelog().add_log(message="Starting to mine all keywords")

        yield f"Mining the following keywords: " + str(self.KEYWORDS_TO_MINE)

        total_new_papers_found = []
        for keyword in tqdm(self.KEYWORDS_TO_MINE):
            yield "Mining papers for topic: " + keyword
            candidate_papers = self.arxiv_gateway.find_by_query(
                query=keyword, sort_by=self.SORT_COLUMN, number_of_papers=number_of_papers_per_keyword
            )
            real_new_papers = [
                p
                for p in candidate_papers
                if p.abstract_url not in self.existing_papers_urls
            ]
            yield "Unique new papers found: " + str(len(real_new_papers)) + " for topic: " + keyword
            total_new_papers_found = total_new_papers_found + real_new_papers

        yield "Found " + str(len(total_new_papers_found)) + " new papers"

        if dry_run:
            return len(total_new_papers_found), 0

        total_registered, total_skipped = self._register_given_papers(
            total_new_papers_found
        )
        ArxivMiningHistory().add(
            keywords=",".join(self.KEYWORDS_TO_MINE),
            total_new_papers_found=len(total_new_papers_found),
        )
        yield "New papers " + str(total_registered) + " papers"
        yield "Skipped " + str(total_skipped) + " papers"
        yield "Done"
        print("Done")
        send_metric(metric="scheduler.mine_all_keywords.success", value=1)
        Changelog().add_log(message="Mined all keywords")
    
    def mine_a_keyword(self, keyword: str, sort_column: SORT_TYPE_ANNOTATION='submitted', number_of_papers=30, dry_run=False) -> List[ArxivPaper]:
        """
        Register all papers by looking in arxiv api with the keyworkds of the audience configuration
        :param dry_run:
        :param disable_relevance_miner:
        :return:
        """
        print(f"Mining {number_of_papers} papers for keyword: {keyword}")
        if dry_run:
            print("Dry run, just printing, not registering them")
        send_metric(metric="scheduler.mine_a_keyword.started", value=1)
        yield f"Registering papers for the following keyword: " + keyword

        candidate_papers = self.arxiv_gateway.find_by_query(
            query=keyword, sort_by=sort_column, number_of_papers=number_of_papers
        )
        print("Sample titles: ")
        for index, p in enumerate(candidate_papers[:10]):
            print(f" {index}. " + p.title, f" {p.abstract_url}")


        real_new_papers = [
            p
            for p in candidate_papers
            if p.abstract_url not in self.existing_papers_urls
        ]
        yield "Unique new papers found: " + str(len(real_new_papers)) + " for topic: " + keyword
        yield "Found " + str(len(real_new_papers)) + " new papers"

        if dry_run:
            return real_new_papers

        total_registered, total_skipped = self._register_given_papers(
            real_new_papers
        )
        ArxivMiningHistory().add(
            keywords=keyword,
            total_new_papers_found=len(real_new_papers),
        )
        yield "New papers " + str(total_registered) + " papers"
        yield "Skipped " + str(total_skipped) + " papers"
        yield "Done"
        send_metric(metric="scheduler.mine_a_keyword.success", value=1)
        Changelog().add_log(message=f"Mined keyword: '{keyword}'")
        return real_new_papers

    def register_by_id(self, id: str):
        """
        Register new paper by id
        """
        print("Registering paper in db by id: ", id)
        papers = self.arxiv_gateway.find_by_id([id])
        print("Found papers: ", str(papers))
        return self._register_given_papers(papers)

    def latest_date_with_papers(self) -> datetime.date:
        """
        Return the latest date with papers in arxiv with the Query AI
        So i assume it should always return something recent
        """
        if not has_internet():
            raise Exception("No internet connection found")

        query = "cat:cs.AI"

        result = self.arxiv_gateway.find_by_query(
            query=query, number_of_papers=3, sort_by="submitted"
        )
        if not result:
            raise Exception(f"Did not find any paper with Query {query}")
        date_str = result[0].updated.date().isoformat()
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


    def _load_existing_papers_urls(self):
        arxiv_papers = self.tdw.event("arxiv_papers")
        if arxiv_papers.empty:
            return []
        return arxiv_papers["abstract_url"].values

    def _register_given_papers(self, papers: List[ArxivPaper]):
        counter = 0
        skipped = 0
        registered = 0
        self.existing_papers_urls = self._load_existing_papers_urls()

        registered_now = []
        for paper in tqdm(papers):
            counter = counter + 1
            if (
                paper.abstract_url in self.existing_papers_urls
                or paper.abstract_url in registered_now
            ):
                skipped += 1
                logging.info("Skipping already registered paper: ", paper.abstract_url)
                continue

            registered += 1
            self.tdw.write_event("arxiv_papers", paper.to_dict())
            registered_now.append(paper.abstract_url)

        print("Registered ", registered, " papers", "Skipped ", skipped, " papers")
        return registered, skipped


if __name__ == "__main__":
    import fire

    fire.Fire()
