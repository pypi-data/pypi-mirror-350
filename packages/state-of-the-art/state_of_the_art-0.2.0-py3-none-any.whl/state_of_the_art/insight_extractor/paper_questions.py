
from typing import List

from pydantic import BaseModel, Field

class PaperQuestions(BaseModel):
    institution: str = Field(description="the institution or insitutions that authored the paper")
    conference: str = Field(description="the conference of the paper")
    top_insights: List[str] = Field(description="the top insights of the paper")
    weaknesses: List[str] = Field(description="the weaknesses of the paper")
    size_and_readtime: str = Field(description="the size of the paper and the time it takes to read it")
    recommended_resources: List[str] = Field(description="Return further resources recommendations if somebody wants to go deep into it. Books, articles, papers, people, organization or conferences to follow related to the topic that helps to get a deeper understanding of it.")
    unique_insights: List[str] = Field(description="What is unique about this paper if anything")
    definitions: List[str] = Field(description="Explain the terminology used in the paper of the top 10 topics")
    explain_for_friends: str = Field(description="If i want to start a conversation with frinds on how cool this paper is how should i describe it to a scientific minded person")
    concrete_recommendations: List[str] = Field(description="Assuming the paper claims are true, what one should do in the day to day to act on them?")
    outcomes: List[str] = Field(description="What are the real outcomes of the paper? Anything trully novel that can be acted upon? ")
    explain_the_structure_and_most_important_parts: str = Field(description="Explain the structure and most important parts of the paper so as to help me to read it efficiently")
    main_idea_of_the_paper: str = Field(description="What is the main idea of the paper?")
