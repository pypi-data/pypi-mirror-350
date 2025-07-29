import time

import pandas as pd

from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.recommenders.interest_recommender import InterestRecommender
from state_of_the_art.recommenders.simple_recommender import PaperRecommender
from personal_streamlit.utils.ui_components import render_date_filters

start_time = time.time()
from personal_streamlit.utils.sidebar_utils import initialize_page
initialize_page()

from state_of_the_art.tables.interest_table import InterestTable
from personal_streamlit.utils.papers_renderer import PapersRenderer
import streamlit as st

topic_description = None

def load_topics_df() -> pd.DataFrame:
    return InterestTable().read_sorted_by_position()

st.title("Interest Recommendations")

    
with st.spinner("Loading topics"):
    topics_df = load_topics_df()

if len(topics_df) == 0:
    st.error("You don't have any interests. Please define some interests to get recommendations.")
    st.stop()

topics_list = topics_df["name"].to_list()

select_only = st.multiselect("Select topics", topics_list, default=[])

if len(select_only) > 0:
    topics_df = topics_df[topics_df["name"].isin(select_only)]

max_results_per_topic_default = 2
results_per_topic = st.number_input("Results per topic", value=max_results_per_topic_default, min_value=1, max_value=100)

st.query_params["results_per_topic"] = results_per_topic

def get_recommendations(paper_per_topic: int, date_from, date_to):
    papers_df = PapersLoader().load_between_dates(date_from, date_to)
    recommender = InterestRecommender(papers_df=papers_df)
    for topic in topics_df.to_dict(orient="records"):
        topic_recommendations = recommender.recommend(topic["name"], return_papers=True)
        for i in range(0, paper_per_topic):
            if len(topic_recommendations) <= i:
                continue
            yield (topic_recommendations[i], {"labels": [topic['name']]})


date_from, date_to = render_date_filters(numbers_of_days_lookback=7)
with st.spinner("Loading recommendations"):
    metadata = {
        "Date From": date_from,
        "Date To": date_to,
        'Number of topics': len(topics_df),
    }


    PapersRenderer().render(get_recommendations(paper_per_topic=results_per_topic, date_from=date_from, date_to=date_to), metadata=metadata)
