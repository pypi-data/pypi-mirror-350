
from typing import List, Optional, Union

import numpy as np
import pandas as pd

from state_of_the_art.paper.arxiv_paper import ArxivPaper
from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.search.bm25_search import Bm25Search
from sentence_transformers import SentenceTransformer


class InterestRecommender():
    CUT_THRESHOLD = 0.4

    def __init__(self, days_to_lookback=15, papers_df: Optional[pd.DataFrame] = None):
        self.number_of_papers = 0
        self.days_to_lookback = days_to_lookback
        self.loader = PapersLoader()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        if papers_df is None:
            self.papers_df = self.loader.load_last_n_days(days=days_to_lookback)
        else:
            self.papers_df = papers_df
        
        if len(self.papers_df) == 0:
            raise Exception("No papers found to recommend")

        self.set_new_papers(self.papers_df)

    def set_new_papers(self, papers_df: pd.DataFrame):
        self.papers_df = papers_df
        self.papers = self.loader.from_pandas_to_paper_list(self.papers_df)
        print(f"Found {len(self.papers)} papers")
        print('setting up bm25...')
        self.bm25_search = Bm25Search(self.papers) 
        print('setting up sentence transformers...')
        self.papers_embeddings = self.model.encode(self.papers_df["title"].tolist()) 
        self.number_of_papers = len(self.papers)
    
    def recommend(self, topic_name: str, n_papers: int = 7, return_papers=False) -> Union[List[ArxivPaper], pd.DataFrame]:
        if not topic_name:
            raise ValueError("Topic name is required")
        result = self.recommend_via_embeddings(topic_name)

        if return_papers:
            return self.loader.load_papers_from_urls(result['abstract_url'].to_list()[0:n_papers])

        return result

    def recommend_via_embeddings(self, topic_name: str) -> List[ArxivPaper]:
        topic_embeddings = self.model.encode(topic_name) 
        cosine_similarities = np.dot(self.papers_embeddings, topic_embeddings)
        
        data = []
        for i in range(0, len(self.papers)):
            data.append([cosine_similarities[i], self.papers[i].title, self.papers[i].abstract_url])

        df = pd.DataFrame(data, columns=['similarity_score', 'title', 'abstract_url'])
        # sort by 
        df = df.sort_values(by='similarity_score', ascending=False)
        result = df[df['similarity_score']>=self.CUT_THRESHOLD]
        return result

        

    def recommend_via_bm25(self, topic_name: str, n_papers: int = 7, return_all_papers: bool = False) -> List[ArxivPaper]:
        papers, scores = self.bm25_search.search_returning_paper_and_score(topic_name)[0:n_papers]

        results = list(zip(papers, scores))

        if return_all_papers:
            return results

        return results[0:n_papers]
