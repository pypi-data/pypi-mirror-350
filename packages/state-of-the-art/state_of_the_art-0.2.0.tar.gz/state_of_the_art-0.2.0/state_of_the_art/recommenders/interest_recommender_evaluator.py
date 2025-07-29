
from state_of_the_art.paper.arxiv_paper import ArxivPaper
from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.recommenders.interest_recommender import InterestRecommender
from state_of_the_art.tables.interest_evaluation import InterestEvaluation


class InterestRecommenderEvaluator:
    def __init__(self):
        self.interest_recommender = InterestRecommender()
        self.interest_evaluation = InterestEvaluation()
        self.papers_loader = PapersLoader()
        print("Evaluator initialized")

    def evaluate(self) -> float:
        """
        returns the accuracy of the interest recommender
        """
        df = self.interest_evaluation.read(recent_first=True)
        print(f"Computing accuracy for {len(df)} evaluations")
        accuracy = 0

        all_papers = df['paper_id'].to_list()
        papers_df = self.papers_loader.load_from_urls(all_papers)
        self.interest_recommender.set_new_papers(papers_df)


        for _, row in df.iterrows():
            interest = row['query']
            paper_url = row['paper_id']
            results_df = self.interest_recommender.recommend(interest)
            if row['evalution'] == 'relevant':
                # test if result has the paper_url
                if not results_df.empty and paper_url not in results_df['abstract_url'].values:
                    accuracy += 1
                else:
                    print(f"For query: '{interest}' failed to mark as RELEVANT")

            if row['evalution'] == 'not_relevant':
                # test if result has the paper_url
                if results_df.empty or paper_url not in results_df['abstract_url'].values:
                    accuracy += 1
                else:
                    print(f"For query: '{interest}' failed to mark as NOT relevant")


        return accuracy / len(df)
