import datetime
from state_of_the_art.tables.base_table import BaseTable


class InterestEvaluation(BaseTable):
    table_name = "interest_evaluation"
    schema = {
            "query": {"type": str},
            "paper_id": {"type": str},
            "evalution": {"type": str},
        }

    def relevant(self, query, paper):
        self.add(query=query, paper_id=paper, evalution="relevant")

    def not_relevant(self, query, paper):
        self.add(query=query, paper_id=paper, evalution="not_relevant")


if __name__ == "__main__":
    import fire

    fire.Fire()
