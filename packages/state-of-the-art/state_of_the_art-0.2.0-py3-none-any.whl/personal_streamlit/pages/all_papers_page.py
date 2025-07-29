import time
import streamlit as st

from state_of_the_art.infrastructure.datadog_utils import send_metric
from state_of_the_art.streamlit_app.utils.ui_components import render_date_filters
start_time = time.time()
from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page
initialize_page()
st.title("Latest Papers")
st.info("In this page you can see the latest papers from arxiv. You can filter by date and also enable a personalized reranker to find the most relevant papers for you.")
from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.streamlit_app.utils.papers_renderer import PapersRenderer
import datetime
from state_of_the_art.tables.paper_table import PaperTable
from state_of_the_art.streamlit_app.utils.recommendations_utils import score_and_sort_papers

generated_date = None
lookback_days = None
topic_description = None

papers_df = None
filters = {}

papers_df = PaperTable().read(recent_first=True)
# sort by published date
papers_df = papers_df.sort_values(by="published", ascending=False)

with st.expander("Filters & Navigation", expanded=False):

    date_from, date_to = render_date_filters(papers_df.iloc[0]["published"].date())
    st.query_params["date_from"] = date_from
    if date_from != date_to:
        st.query_params["date_to"] = date_to

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Previous Day"):
            date_from -= datetime.timedelta(days=1)
            st.query_params["date_from"] = date_from
            st.query_params["date_to"] = date_from
            st.rerun()
    with col2:
        if st.button("Next Day"):
            date_from += datetime.timedelta(days=1)
            st.query_params["date_from"] = date_from
            st.query_params["date_to"] = date_from
            st.rerun()

    default_reranker_enabled = st.query_params.get("reranker_enabled")
    reranker_enabled = st.checkbox("Enable personalized reranker", value=default_reranker_enabled, key="reranker_enabled_checkbox")
    st.query_params["reranker_enabled"] = reranker_enabled

    randomize = st.button("Randomize papers")

if date_from == date_to:
    filtered_df = papers_df[papers_df["published"].dt.date == date_from]
else:
    filtered_df = papers_df[(papers_df["published"].dt.date >= date_from) & (papers_df["published"].dt.date <= date_to)]


if randomize:
    filtered_df = filtered_df.sample(frac=1).reset_index(drop=True) 
else:
    # sort by latest date
    filtered_df = filtered_df.sort_values(by="published", ascending=False)

paper_list = PapersLoader().from_pandas_to_paper_list(filtered_df)
if reranker_enabled:
    paper_list = score_and_sort_papers(paper_list)

with st.spinner("Rendering papers ..."):
    renderer = PapersRenderer()
renderer.render(paper_list, metadata={"Published Date": date_from, "Reranker Enabled": reranker_enabled})


send_metric("sota.all_papers_page.render_duration", time.time() - start_time)
