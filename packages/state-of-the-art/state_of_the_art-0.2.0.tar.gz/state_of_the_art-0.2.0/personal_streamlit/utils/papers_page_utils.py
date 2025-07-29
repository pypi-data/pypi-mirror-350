from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.paper.url_extractor import PapersUrlsExtractor
from state_of_the_art.tables.recommendations_history_table import (
    UserRecommendationsHistoryTable,
)


def load_papers_from_last_report(report_id=None, max_num_of_results=None):
    report_df = UserRecommendationsHistoryTable().read()
    if report_id:
        report_df = report_df[report_df["tdw_uuid"] == report_id].iloc[-1]
    else:
        report_df = report_df.iloc[-1]

    latest_summary = report_df.to_dict()

    latest_urls = PapersUrlsExtractor().extract_urls(latest_summary["summary"])
    papers = PapersLoader().load_papers_from_urls(latest_urls)
    if max_num_of_results:
        papers = papers[0:max_num_of_results]

    return papers, latest_summary["tdw_timestamp"]
