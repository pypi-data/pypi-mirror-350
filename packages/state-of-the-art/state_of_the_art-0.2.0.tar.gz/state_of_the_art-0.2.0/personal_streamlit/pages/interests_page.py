import time

start_time = time.time()
from state_of_the_art.infrastructure.datadog_utils import send_metric

from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page

initialize_page()
from state_of_the_art.streamlit_app.data import papers, topics
from state_of_the_art.streamlit_app.utils.papers_renderer import PapersRenderer
from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.search.bm25_search import Bm25Search
from state_of_the_art.tables.interest_table import InterestTable
import streamlit as st

from state_of_the_art.tables.paper_table import PaperTable

generated_date = None
lookback_days = None
topic_description = None

st.title("Your Interests")
st.info("Here you can register your interests you will immediately see papers related to the described interest.")
papers = None
send_by_email = False

topics = InterestTable()
topics_df = topics.read_sorted_by_position()
interests_names = topics_df["name"].tolist()

colouter1, colouter2 = st.columns([2, 1])
with colouter1:
    with st.expander("Selected Interest", expanded=True):
        if "interest" in st.query_params:
            selected_interest = st.query_params["interest"]
        elif "new" in st.query_params :
            selected_interest = ""
        else:
            selected_interest = interests_names[0] if interests_names else ""

        if selected_interest and not topics_df[topics_df["name"] == selected_interest].empty:
            interest_name = topics_df[topics_df["name"] == selected_interest].iloc[0]["name"] 
            topic_description = topics_df[topics_df["name"] == selected_interest].iloc[0][
                "description"
            ]
        else: 
            interest_name = ""
            topic_description = ""


        interest_name = st.text_input("Interest name", value=interest_name)
        topic_description = st.text_area("Query / Description", value=topic_description)

        c1, c2, c3 = st.columns([1, 1, 5 ])
        with c1:
            if st.button("New"):
                if "interest" in st.query_params:
                    del st.query_params["interest"]
                st.query_params["new"] = 'True'
                st.rerun()
        with c2:
            if st.button("Save"):
                topics.add_interest(name=interest_name, description=topic_description)
                st.query_params["interest"] = interest_name
                if "new" in st.query_params:
                    del st.query_params["new"]
                st.success("Interest saved successfully")
                time.sleep(0.1)
                st.rerun()
        with c3:
            if st.button("Delete"):
                topics.delete_by_name(interest_name)
                del st.query_params["interest"]
                st.success("Interest deleted successfully")
                st.rerun()

        st.write(f"Selected interest: {interest_name}")
with colouter2:
    with st.expander("All Interests", expanded=False):
        if len(interests_names) > 0:
            st.write(f"{len(interests_names)} Interests registered")

        for interest in interests_names:
            c1, c2, c3 = st.columns([1, 1, 1])
            try:
                with c1:
                    if st.button(interest, key=f"t{interest}"):
                        st.query_params["interest"] = interest
                with c2:
                    if st.button("Move to top", key=f"t{interest}_top"):
                        topics.move_to_top(interest)
                        st.success("Interest moved to top")
                with c3:
                    if st.button("Move to bottom", key=f"t{interest}_bottom"):
                        topics.move_to_bottom(interest)
                        st.success("Interest moved to bottom")
            except:
                pass

with st.spinner("Searching similar papers ..."):
    recent_papers_df = PaperTable().load_recent_papers_df()
    papers = PapersLoader().from_pandas_to_paper_list(recent_papers_df)
    papers = Bm25Search(papers).search_returning_papers(
        interest_name + " " + topic_description
    )
# render all papeers
PapersRenderer().render(papers, generated_date=generated_date, metadata={'Query': interest_name + " " + topic_description})

send_metric("sota.interests_page.render_duration", time.time() - start_time)
