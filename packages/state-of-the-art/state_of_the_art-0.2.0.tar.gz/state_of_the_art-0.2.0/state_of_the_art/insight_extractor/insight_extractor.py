import os
from typing import List, Tuple
from state_of_the_art.config import config
from state_of_the_art.insight_extractor.paper_questions import PaperQuestions
from state_of_the_art.insight_extractor.structured_insights import StructuredPaperInsights, SupportedModels
from state_of_the_art.tables.insights_table import InsightsTable
from state_of_the_art.utils import pdf
from state_of_the_art.insight_extractor.content_extractor import get_content_from_url


class AIInsightsExtractor:
    """
    Looks into a single paper and extracts insights
    """

    def extract_insights_from_paper_url(
        self,
        url: str,
    ) -> None:
        """
        Generates insights for a given paper
        Accepts an url with a pdf, downloads it and extracts the insights
        """
        paper_questions = self.get_paper_questions(url)
        self.post_extraction(
            paper_questions,
            url,
        )

    def get_paper_questions(self, url: str) -> PaperQuestions:
        url = self._clean_url(url)
        try:
            article_content, title, document_pdf_location = get_content_from_url(url)
        except Exception as e:
            raise e
        paper_questions = StructuredPaperInsights().get_result(article_content)
        return paper_questions

    def post_extraction(
        self,
        paper_questions: PaperQuestions,
        url: str,
    ):
        if os.environ.get("SOTA_TEST"):
            print("SOTA_TEST is set, skipping post_extraction")
            return

        insights = self._convert_sturctured_output_to_insights(paper_questions)
        self._write_insights_into_table(insights, url)


    def _convert_sturctured_output_to_insights(self, structured_result: PaperQuestions) -> List[Tuple[str, str]]:
        result = []
        for key, value in structured_result.dict().items():
            if isinstance(value, str):
                result.append((key, value))
            else:
                # if its a list
                for insight_row in value:
                    result.append((key, insight_row))

        return result

    def _write_insights_into_table(self, insights, url):
        # reverse order of insights
        insights.reverse()

        insights_table = InsightsTable()
        for question, insight in insights:
            insights_table.add_insight(insight, question, url, None)

    def _clean_url(self, url):
        print("Given url: ", url)
        url = url.strip()
        url = url.replace("file://", "")
        return url
