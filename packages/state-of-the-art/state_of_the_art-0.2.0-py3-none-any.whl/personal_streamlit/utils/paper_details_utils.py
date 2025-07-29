import os
from typing import List
import pandas as pd
from state_of_the_art.infrastructure.s3 import S3
from state_of_the_art.paper.article_creator import CustomArticleCreator
from state_of_the_art.insight_extractor.structured_insights import SupportedModels
from state_of_the_art.paper.url_sanitizer import UrlSanitizer
from streamlit_tags import st_tags
from state_of_the_art.paper.arxiv_paper import ArxivPaper
from state_of_the_art.register_papers.register_paper import PaperCreator
from state_of_the_art.relevance_model.text_evaluation_inference import PersonalPreferenceInference
from state_of_the_art.tables.paper_metadata_from_user_table import PaperMetadataFromUser
from state_of_the_art.tables.tags_table import TagsTable
import streamlit as st
from state_of_the_art.insight_extractor.insight_extractor import (
    AIInsightsExtractor,
)
from state_of_the_art.tables.questions_table import QuestionsTable
from state_of_the_art.utils.filesystem_utils import cleanup_file_name
from state_of_the_art.config import config


@st.dialog("Questions")
def questions(paper_url):
    tab1, tab2 = st.tabs(["Custom question", "Default questions"])

    with tab1:
        custom_question = st.text_input("Type the question here")

    with tab2:
        question_table = QuestionsTable()
        df = question_table.read()
        df_updated = st.data_editor(df, width=800, num_rows="dynamic")
        if st.button("Save"):
            question_table.replace(df_updated, dry_run=False)
            st.success("Successfully saved")

    supported_models = [model.value for model in SupportedModels]
    selected_model = st.selectbox(
        "Select a model",
        supported_models,
        index=supported_models.index(SupportedModels.gpt_4o.value),
    )
    extract_insights = st.button("Generate Insights", key="generate_insights_dialog")
    if extract_insights:
        AIInsightsExtractor().extract_insights_from_paper_url(
            paper_url,
            email_skip=True,
            disable_pdf_open=True,
            question=custom_question,
            selected_model=selected_model,
        )
        st.rerun()




def render_tags_for_paper(paper: ArxivPaper):
    tags_table = TagsTable()
    tags_table_df = tags_table.read()

    existing_tags = []
    existing_tags_df = tags_table_df[tags_table_df["paper_id"] == paper.abstract_url]
    if not existing_tags_df.empty:
        existing_tags = existing_tags_df.iloc[0]["tags"].split(",")
    currently_selected_tags = st_tags(
        label="", value=existing_tags, key=f'tags_{paper.abstract_url}', suggestions=TagsTable.DEFAULT_TAGS
    )
    currently_selected_tags = [tag.strip().lower() for tag in currently_selected_tags]
    st.session_state['tags_to_save'] = currently_selected_tags
    if st.button("Save Tags"):
        tags_table.replace_tags(paper.abstract_url, st.session_state['tags_to_save'])
        st.success(f"Tags updated successfully ({', '.join(currently_selected_tags)})")


def render_reading_progress(paper):
    query_progress = PaperMetadataFromUser().load_with_value(
        "abstract_url", paper.abstract_url
    )
    if not query_progress.empty:
        current_progress = int(query_progress.iloc[0]["progress"])
    else:
        current_progress = 0

    new_set_progress = st.select_slider(
        "Reading progress", options=tuple(range(0, 105, 5)), value=current_progress
    )
    if new_set_progress != current_progress:
        PaperMetadataFromUser().update_or_create(
            by_key="abstract_url",
            by_value=paper.abstract_url,
            new_values={"progress": new_set_progress},
        )
        st.success("Progress updated successfully")


@st.dialog("Load an Article")
def create_custom_paper():
    tab1, tab2, tab3 = st.tabs(["Upload custom Article", "Custom Article from URL", "Load an Arxiv Article"])

    with tab1:
        title = st.text_input("Title", key="title_upload_custom_paper")

        file = st.file_uploader("Upload article", type=["pdf", "docx", "txt"])
       
        if st.button("Upload", key="upload_custom_paper"):
            
            with st.spinner("Uploading file..."):
                url = upload_file_to_s3(file)
                st.write("File copied to s3, now you can import it ")
                st.write("Url: " + url)

                paper_id = CustomArticleCreator().create(url, title)
                st.query_params["paper_id"] = paper_id
                st.success("Paper saved successfully")
                st.link_button("Go to papers page", "/paper_details_page?paper_url=" + url)
                st.stop()
    with tab2:
        title = st.text_input("Title", key="title_custom_paper_from_url")
        paper_url = st.text_input("Url", key="url_custom_paper_from_url")
        if st.button("Save", key="save_custom_paper_from_url"):
            with st.spinner("Saving paper..."):
                st.session_state["save_paper_clicked"] = True
                st.query_params["paper_url"] = paper_url
                paper_id = CustomArticleCreator().create(paper_url, title)
                st.query_params["paper_id"] = paper_id
                st.success("Paper saved successfully")
                st.link_button("Go to papers page", "/paper_details_page?paper_url=" + paper_url)
                st.stop()

    with tab3:
        default_url = st.query_params.get("paper_url", "")
        url = st.text_input(
            "Paper URL",
            value=default_url,
            key="paper_url",
            help="Type the URL of the paper to be loaded",
        )
        if st.button("Register") and url:
            url = PaperCreator().register_arxiv_paper_by_url(url)

            st.write(f"Paper '{url}' registered successfully")
            st.link_button("Go to papers page", "/paper_details_page?paper_url=" + url)
            st.stop()


    return False

def upload_file_to_s3(file) -> str:
    """
    returns the url of the file in s3
    """
    # save to /tmp/folder
    file_path = os.path.join("/tmp/", cleanup_file_name(file.name)) 
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    S3().copy_article_to_s3(file_path)
    return config.ARTICLES_BASE_URL + "/" + cleanup_file_name(file.name)

def filter_insights(insights: pd.DataFrame, IGNORED_INSIGHTS: List[str]):
    insights = insights.to_dict(orient="records")
    insights = list(filter(lambda x: x["question"] not in IGNORED_INSIGHTS, insights))
    return [x['question'] + ": " + x['insight'] for x in insights]
