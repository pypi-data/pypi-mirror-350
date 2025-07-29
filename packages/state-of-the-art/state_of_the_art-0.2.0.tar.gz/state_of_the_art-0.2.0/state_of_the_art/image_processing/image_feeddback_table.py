from typing import Any
from state_of_the_art.tables.base_table import BaseTable


class ImageFeedbackTable(BaseTable):
    """
    scoring semantics

    1: Very Bad, horrible
    2: Bad: not helpful
    3: Interesting: Make the know more but not sure if it is a good one
    4: Good, already gives me a lot by just looking at it
    5: Very Good, mindblowing
    """
    table_name = "image_feedback"
    schema = {"paper_id": {"type": str}, "image_position": {"type": str}, "score": {"type": Any}}

    def add_feedback(self, *, paper_id: str, image_position: str, score: int):
        if not image_position.isdigit():
            raise ValueError("Image position must be an integer got {}".format(image_position))
        return super().add(paper_id=paper_id, image_position=str(image_position), score=str(score))
    
    def get_image_score(self, *, paper_id: str, image_position: str) -> int | None:
        df = self.read()
        df = df[df["paper_id"] == paper_id]
        df = df[df["image_position"] == image_position]
        if len(df) == 0:
            return None
        return df["score"].tolist()[0]
