import datetime
import time
start_time = time.time()

from state_of_the_art.infrastructure.datadog_utils import send_metric

from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page
initialize_page()

from typing import List
from state_of_the_art.infrastructure.cache import MemoryCache
import streamlit as st
import itertools

from state_of_the_art.streamlit_app.data import papers
from state_of_the_art.streamlit_app.utils.papers_renderer import PapersRenderer
from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.tables.tags_table import TagsTable


num_of_results = 15
lookback_days = None
topic_description = None
num_of_results = 15
papers = None
send_by_email = False

st.title("Your papers")
st.info("Here you find the papers you assinged tags to. You can filter by tags, date and also remove tags.")

def load_all_tags():
    return TagsTable().read()

all_tags_df = load_all_tags()
all_tags = all_tags_df["tags"].to_list()
all_tags = [tags.split(",") for tags in all_tags]
merged = list(itertools.chain(*all_tags))
all_unique_tags = list(set(merged))


filters = {}

with st.expander("Filters"):
    options = ['Select'] + all_unique_tags
    index = 0 if 'selected_tags' not in st.query_params else options.index(st.query_params["selected_tags"])
    selected_tags = st.selectbox("Filter By tags", options=options, index=index)
    st.query_params["selected_tags"] = selected_tags
    filters["Selected tags"] = selected_tags

    url_from_date = st.query_params.get("from_date", None)  
    if url_from_date:
        url_from_date = datetime.datetime.strptime(url_from_date, "%Y-%m-%d").date()        
        filters["From date"] = url_from_date

    url_to_date = st.query_params.get("to_date", None)
    if url_to_date:
        url_to_date = datetime.datetime.strptime(url_to_date, "%Y-%m-%d").date()
        filters["To date"] = url_to_date



    # add from and to published date filters
    from_date = st.date_input("Published from", value=url_from_date)
    to_date = st.date_input("Published to", value=url_to_date)
    if from_date:
        st.query_params["from_date"] = from_date
    if to_date:
        st.query_params["to_date"] = to_date


    if st.button("Clear filters"):
        st.query_params.clear()

    

if selected_tags == 'Select':
    selected_tags = all_unique_tags
else:
    selected_tags = [selected_tags]



def load_papers_for_selected_tags(selected_tags: List[str]):
    if MemoryCache().has_item(f"papers_for_selected_tags", context=selected_tags ):
        return MemoryCache().get_item(f"papers_for_selected_tags", context=selected_tags)

    all_papers_selected = all_tags_df[
        all_tags_df["tags"].str.contains("|".join(selected_tags))
    ]
    all_papers_selected = all_papers_selected["paper_id"].to_list()
    unique_papers = list(set(all_papers_selected))

    result = PapersLoader().load_papers_from_urls(unique_papers)

    MemoryCache().set_item(f"papers_for_selected_tags", result, context=selected_tags, ttl_seconds=60*5)
    return result

papers = load_papers_for_selected_tags(selected_tags)

if from_date:
    papers = [paper for paper in papers if paper.has_published_date() and paper.get_published_date() >= from_date]
if to_date:
    papers = [paper for paper in papers if paper.has_published_date() and paper.get_published_date() <= to_date]

# sort papers by the bookmarked date
papers = sorted(
    papers,
    key=lambda x: all_tags_df[all_tags_df["paper_id"] == x.abstract_url][
        "tdw_timestamp"
    ].values[0],
    reverse=True,
)

with st.spinner("Rendering papers ..."):
    PapersRenderer(disable_save_button=True, enable_tags=True).render(papers, papers_metadata=filters)

send_metric("sota.your_papers_page.render_duration", time.time() - start_time)
