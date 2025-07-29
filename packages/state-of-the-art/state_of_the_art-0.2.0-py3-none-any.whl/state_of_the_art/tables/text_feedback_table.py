import json
from typing import Any, Optional, Tuple
from state_of_the_art.infrastructure.datadog_utils import send_metric
from state_of_the_art.tables.base_table import BaseTable
from enum import Enum

class ScoreMeaning(Enum):
    changed_my_life = 4
    learned_something_new = 3
    interesting = 2
    bad = 1
    very_bad = 0


class TextFeedbackTable(BaseTable):
    table_name = "text_feedback"
    schema = {"text": {"type": str}, "score": {"type": Any}, "type": {"type": str}, "context": {"type": str}}

    def add_feedback(self, text: str, score: int, type: Optional[str] = None, context: Optional[str] = None):

        posible_values = [i.value for i in ScoreMeaning]

        if score not in posible_values:
            raise ValueError(f"Invalid score {score}")
        if not type: 
            type = TextTypes.default.value
        if not context: 
            context = ""
        else:
            context = json.dumps(context)
        
        self.add(text=text, score=score, type=type, context=context)

        num_feedbacks = self.len()
        print(f"Number of feedbacks: {num_feedbacks}")
        send_metric(metric="sota.number_of_feedbacks", value=num_feedbacks)


    def register_as_interesting(self, text: str, context: Optional[str] = None) -> Tuple[bool, str]:
        """
        Register a paper as interesting using the default score of 2.
        """
        # check if the paper is already registered as interesting
        if self.read()['text'].str.contains(text).any():
            return False, f"'{text}' already registered as interesting so not registering again"
        self.add_feedback(text=text, score=ScoreMeaning.interesting.value, type=TextTypes.default.value, context=context)

        return True, f"'{text}' registered as interesting"
class TextTypes(Enum):
    default = "default"
    paper_title = "paper_title"
    paper_insight = "paper_insight"

if __name__ == "__main__":
    import fire
    fire.Fire()
