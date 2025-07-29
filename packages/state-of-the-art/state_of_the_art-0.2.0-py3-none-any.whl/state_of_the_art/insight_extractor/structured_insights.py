from enum import Enum
import random
from state_of_the_art.config import config
from state_of_the_art.insight_extractor.paper_questions import PaperQuestions
from openai import OpenAI


import json
import os
from typing import Optional, Tuple


class SupportedModels(Enum):
    gpt_4o_mini = "gpt-4o-mini"
    gpt_4o = "gpt-4o"


class StructuredPaperInsights:
    def __init__(self, model_to_use: Optional[str] = None):
        self.profile = config.get_current_audience()
        self.QUESTIONS: dict[str, str] = self.profile.paper_questions
        self.profile = config.get_current_audience()
        self.model_to_use = model_to_use

    def get_result(self, paper_content: str) -> PaperQuestions:
        if os.environ.get("SOTA_TEST"):
            return "Mocked result", {}

        used_model = (
            self.model_to_use if self.model_to_use else SupportedModels.gpt_4o.value
        )
        print("Using model: ", used_model)
        print("Paper preview to summarize: ", paper_content[0:3000])

        if len(paper_content) < 300:
            raise Exception(f"Paper content too short to send to OpenAI content: {paper_content}")

        if len(paper_content) > 120000:
            paper_content = paper_content[0:120000]
        

        instructions = f"""
You extract paper insights.
Returns the most insightful and actionable information from the given paper content
It optimized the answers for the following audience: {self.profile.get_preferences()[0:300]}
Make your answers not too small.
"""

        client = OpenAI(api_key=config.read_openai_key())
        result = client.responses.parse(
            model=used_model,
            input=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": paper_content}
                ],
            text_format=PaperQuestions,
        )
        parsed_results = result.output_parsed
        print("parsed_results: ", parsed_results)

        return parsed_results
