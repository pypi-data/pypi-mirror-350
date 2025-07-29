from typing import Optional

import pandas as pd
from state_of_the_art.tables.base_table import BaseTable


class PaperTable(BaseTable):
    table_name = "arxiv_papers"
    schema = {
        "abstract_url": {"type": str},
        "title": {"type": str},
        "published": {"type": int},
        "institution": {"type": Optional[str]},
    }

    def load_recent_papers_df(self) -> pd.DataFrame:
        return self.read(recent_first=True)[0:200]
