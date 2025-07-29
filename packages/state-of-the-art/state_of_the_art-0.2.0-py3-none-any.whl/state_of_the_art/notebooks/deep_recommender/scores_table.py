
from state_of_the_art.tables.base_table import BaseTable


class ScoresTable(BaseTable):
    table_name = "folder"
    schema = {
        'paper_url': {'type': str},
        'paper_title': {'type': str},
        'bm25_sum_score': {'type': float},
        'predictor_score': {'type': float},
        'generated_date': {'type': 'str'},
        'final_score': {'type': float},
    }
