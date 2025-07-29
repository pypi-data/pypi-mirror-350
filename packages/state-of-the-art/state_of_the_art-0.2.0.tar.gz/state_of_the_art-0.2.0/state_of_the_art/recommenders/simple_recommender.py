
import datetime
from typing import Dict, Generator, List, Optional, Tuple

import pandas as pd
from state_of_the_art.paper.paper_entity import Paper
from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.search.bm25_search import Bm25Search
from state_of_the_art.tables.interest_table import InterestTable
from state_of_the_art.tables.paper_table import PaperTable


class PaperRecommender:
    DEFAULT_RESULTS_PER_TOPIC = 2
    def __init__(self, topics_df: pd.DataFrame = None):
        self.topics_df = topics_df if topics_df is not None else self._load_all_topics()
        self.paper_candidates: List[Paper] = []
    
    def _load_all_topics(self):
        return InterestTable().read_sorted_by_position()

    def set_date_filters(self, date_from: datetime.date, date_to: datetime.date):
        self.date_from = date_from
        self.date_to = date_to
    

    def fetch_paper_candidates(self):
        papers_df = PaperTable().read()
        papers_df = papers_df[(papers_df["published"].dt.date >= self.date_from) & (papers_df["published"].dt.date <= self.date_to)]
        self.paper_candidates: List[Paper] = PapersLoader().from_pandas_to_paper_list(papers_df)

    def get_recommendations(self, results_per_topic: Optional[int] = None, max_results=100) -> Generator[Tuple[Paper, Dict[str, Dict[str, str]]], None, None]:
        if results_per_topic is None:
            results_per_topic = self.DEFAULT_RESULTS_PER_TOPIC

        self.fetch_paper_candidates()

        if not self.paper_candidates:
            raise Exception("No papers found")
        
        bm25_search = Bm25Search(self.paper_candidates) 

        result_papers = []
        total_papers = 0
        for topic in self.topics_df.iterrows():
            if topic[1].get('name', '') == None: 
                continue
            topic_query = topic[1].get('name', '') + " " + topic[1].get('description', '')

            top_papers = bm25_search.search_returning_papers(topic_query, n=results_per_topic)
            for paper in top_papers:
                yield (paper, {'labels': [topic[1]["name"]]})

            result_papers.extend(top_papers)
            total_papers += len(top_papers)
            if total_papers >= max_results:
                break
