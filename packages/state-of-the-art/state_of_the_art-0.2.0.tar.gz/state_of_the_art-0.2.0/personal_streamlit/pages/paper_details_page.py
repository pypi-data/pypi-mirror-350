import time
import streamlit as st

from state_of_the_art.image_processing.image_inference import ImageInference
from state_of_the_art.image_processing.images_extractor import ImagesExtractor
from state_of_the_art.image_processing.images_renderer import ImagesRenderer
from state_of_the_art.paper.arxiv_paper import ArxivPaper
from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page
initialize_page()
from state_of_the_art.paper.arxiv_url_converter import ArxivUrlConverter
from state_of_the_art.paper.paper_entity import Paper
from state_of_the_art.tables.changelog_table import Changelog
from state_of_the_art.tables.text_feedback_table import TextFeedbackTable
start_time = time.time()

from state_of_the_art.infrastructure.datadog_utils import send_metric

from typing import List
from state_of_the_art.streamlit_app.utils.ai_gen_utils import extract_ai_insights
from state_of_the_art.streamlit_app.utils.login_utils import setup_login
from state_of_the_art.streamlit_app.utils.paper_details_utils import filter_insights
from state_of_the_art.paper.email_paper import EmailAPaper
from state_of_the_art.paper.url_sanitizer import UrlSanitizer
from state_of_the_art.register_papers.register_paper import PaperCreator
from state_of_the_art.tables.insights_table import InsightsTable
from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.tables.tags_table import TagsTable
from state_of_the_art.text_feedback.feedback_elements import TextWithFeedback, render_feedback
from state_of_the_art.streamlit_app.utils.ui_components import styled_button, styled_expander, styled_header


IGNORED_INSIGHTS = [
    "institution",
    "conference",
    "definitions",
    "recommended_resources",
    'size_and_readtime'
]

url = st.query_params.get("paper_url", "")
url = UrlSanitizer().sanitize(url)
url = ArxivUrlConverter().convert_pdf_url_to_abstract_url(url)
st.query_params.paper_url = url

paper_id  = st.query_params.get("paper_id", "")
if not url and not paper_id:
    st.write("No paper loaded. Click on a paper or load a new one using the left menu button.")
    st.stop()

if not PaperCreator().is_paper_registered(url):
    st.error(f"Paper '{url}' not registered and not created. Create this paper before.")
    st.stop()

if paper_id:    
    paper: Paper = PapersLoader().load_paper_from_id(paper_id)
else:
    paper: Paper = PapersLoader().load_paper_from_url(url)

insights_table = InsightsTable()
insights = insights_table.read()
insights = insights[insights["paper_id"] == paper.abstract_url]
insights = insights.sort_values(by="tdw_timestamp", ascending=False)
has_insights = not insights.empty

pdf_markup = ""
if paper.pdf_url:
    pdf_markup = f"<a href='{paper.pdf_url}' target='_blank'>PDF</a>"
st.markdown(f"<h1 style='text-align: center;'><a href='{paper.abstract_url}' target='_blank'>{paper.title}</a> {pdf_markup}</h1>", unsafe_allow_html=True)

try:
    # thorws exception if the paper is already registered as interesting
    result = TextFeedbackTable().register_as_interesting(paper.title, context={"paper_id": paper.abstract_url, 'from': 'render_paper_details_page'})
    if result[0]:
        st.success(result[1])
except Exception as e:
    st.warning(str(e))

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if styled_button("Generate AI Insights") or (not has_insights and not st.session_state.get("attempeted_to_generate_insights", False)):
        extract_ai_insights(paper.abstract_url)
        st.session_state.attempeted_to_generate_insights = True
with col2:
    if styled_button("Save Paper"):
        with st.status("Saving paper..."):
            st.write("Adding paper to your list of papers to read later...")
            tags_table = TagsTable()
            tags_table.add_tag_to_paper(paper.abstract_url, "save for later")
            Changelog().add_log(message=f"Paper saved for later: {paper.abstract_url}")
            st.success("Paper saved successfully")
            st.rerun()
with col3:
    if styled_button("Send to Email"):
        with st.status("Sending email..."):
            st.write("Sending email to your email address...")
            email_paper = EmailAPaper()
            result = email_paper.send(paper)
            st.success(f"Email sent successfully to {email_paper.get_destination_email()}")
            st.write(result)
with col4:
    if styled_button("Extract images"):
        with st.status("Extracting images..."):
            ImagesExtractor().extract_images_from_paper(paper=paper)
            st.success("Images extracted successfully")
            st.rerun()

# render images
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    styled_header("Published", paper.published_date_str())
with col2:
    institution = insights_table.get_lastest_answer("institution", paper.abstract_url)
    styled_header("Institution", institution or "N/A")
with col3:
    conference = insights_table.get_lastest_answer("conference", paper.abstract_url)
    styled_header("Conference", conference or "N/A")
with col4:
    size_and_readtime = insights_table.get_lastest_answer("size_and_readtime", paper.abstract_url)
    styled_header("Size and Readtime", size_and_readtime or "N/A")

top_insights: List[str] = insights_table.get_all_answers_for_question_in_paper("top_insights", paper.abstract_url)

with st.expander("Images"):
    if ArxivPaper.is_arxiv_url(paper.abstract_url):
        images: List[str] = ImagesRenderer().get_images_from_paper(paper)
        # sort images by predicted score
        image_inference = ImageInference()
        sorted_images = sorted(images, key=lambda x: image_inference.predict_image(x), reverse=True)
        for image in sorted_images:
            st.image(image)
    else:
        st.write("Cant still process images for this paper as its not an arxiv paper")


if paper.abstract:
    with st.expander("Abstract", expanded=not top_insights):
        st.subheader("Abstract")
        st.markdown(paper.abstract)
        render_feedback(paper.abstract, type='paper_insight', context={'paper_id': paper.abstract_url})


explain_for_friends: str = insights_table.get_lastest_answer("explain_for_friends", paper.abstract_url)
st.write(explain_for_friends)
c1, c2 = st.columns([1, 1])
text_with_feedback = TextWithFeedback()
with c1:
    with st.expander("Definitions", expanded=True):
        definitions = insights_table.get_all_answers_for_question_in_paper("definitions", paper.abstract_url)
        if definitions:
            text_with_feedback.render_batch(definitions, st.markdown, paper_id=paper.abstract_url)
with c2:
    with st.expander("Resources", expanded=True):
        resources: List[str] = insights_table.get_all_answers_for_question_in_paper("recommended_resources", paper.abstract_url)
        if resources:
            text_with_feedback.render_batch(resources, st.markdown, paper_id=paper.abstract_url)

with st.spinner("Loading insights..."):
    # More Insights
    filtered_insights = filter_insights(insights, IGNORED_INSIGHTS)
    st.info("The insights are scored based on how relevant they to you.")

    if filtered_insights:
        st.subheader("More Insights")
        text_with_feedback.render_batch(filtered_insights, st.markdown, paper_id=paper.abstract_url)
    else:
        st.write("No more insights found")

send_metric("sota.paper_details_page.render_duration", time.time() - start_time)
