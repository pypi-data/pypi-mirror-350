

from state_of_the_art.infrastructure.datadog_utils import send_metric
from state_of_the_art.register_papers.arxiv_miner import ArxivMiner
from state_of_the_art.tables.paper_table import PaperTable

import datetime

class ArxivSyncChecker:

    def get_latest_paper_registered_date_in_sota(self) -> datetime.date:
        df = PaperTable().load_recent_papers_df()
        return df.published.max().date()
    
    def get_latest_paper_registered_date_from_arxiv(self) -> datetime.date:
        return ArxivMiner().latest_date_with_papers()
    
    def get_delay_from_today_in_days(self) -> dict[str, int]:
        return {
            "sota": (datetime.date.today() - self.get_latest_paper_registered_date_in_sota()).days,
            "arxiv": (datetime.date.today() - self.get_latest_paper_registered_date_from_arxiv()).days,
        }


    def send_to_datadog(self):
        delay_from_today = self.get_delay_from_today_in_days()
        send_metric('sota.arxiv_sync_checker.delay_from_today', delay_from_today['sota'], tags=['sota'])
        send_metric('sota.arxiv_sync_checker.delay_from_today', delay_from_today['arxiv'], tags=['arxiv'])
    
