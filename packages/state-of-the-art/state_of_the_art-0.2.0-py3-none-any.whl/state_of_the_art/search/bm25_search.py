from typing import List, Tuple
import nltk
from rank_bm25 import BM25Okapi as BM25
from state_of_the_art.paper.arxiv_paper import ArxivPaper


class Bm25Search:
    def __init__(self, papers_list: List[ArxivPaper] = None):
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.bm25 = None
        self.papers_list = papers_list
        if papers_list:
            self.set_papers_and_index(papers_list=papers_list)
        else:
            print("No papers list provided while initializing Bm25Search")

    def set_papers_and_index(self, papers_list: List[ArxivPaper]):
        self.papers_list = papers_list
        tokenized_corpus = [
            self.tokenize(paper.title + " " + paper.abstract)
            for paper in self.papers_list
        ]

        self.bm25 = BM25(tokenized_corpus)

    def search_returning_papers(self, query, n=100, get_all_papers=False) -> List[ArxivPaper]:
        if not self.bm25:
            raise ValueError("BM25 is not initialized. Please call set_papers_and_index first. Alternative maybe you initialized bm25 without a papers list?")
        
        if get_all_papers:
            n = len(self.papers_list)

        tokenized_query = self.tokenize(query)
        matches = self.bm25.get_top_n(tokenized_query, self.papers_list, n=n)

        return matches

    def search_returning_paper_and_score(
        self, query, n=100, get_all_papers=False
    ) -> Tuple[List[ArxivPaper], List[float]]:
        tokenized_query = self.tokenize(query)

        if get_all_papers:
            n = len(self.papers_list)

        matches = self.bm25.get_top_n(tokenized_query, self.papers_list, n=n)
        scores = sorted(self.bm25.get_scores(tokenized_query)[0:n], reverse=True)

        return matches, scores

    def tokenize(self, string):
        tokens = self.tokenizer.tokenize(string)
        lemmas = [self.lemmatizer.lemmatize(t) for t in tokens]
        return lemmas

if __name__ == "__main__":
    import fire

    fire.Fire()
