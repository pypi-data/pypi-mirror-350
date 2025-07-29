
import streamlit as st
from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page

initialize_page()

from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.streamlit_app.utils.papers_renderer import PapersRenderer
from state_of_the_art.tables.insights_table import InsightsTable, InsightsTableNew


st.title("Papers with Insights Generated")

df = InsightsTableNew().read(recent_first=True)

# get only paper ids unique
paper_urls = df['paper_id'].unique().tolist()
st.write("Found", len(paper_urls), "papers")
papers = PapersLoader().load_papers_from_urls(paper_urls)



PapersRenderer().render(papers)
