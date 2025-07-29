import streamlit as st
import os
from state_of_the_art.config import config
from state_of_the_art.infrastructure.datadog_utils import setup_datadog

def get_commit_hash():
    home = os.path.expanduser("~")
    with open(f"{home}/.commit_hash", "r") as f:
        return f.read().strip()

setup_datadog()

# Set page configuration
title = 'State of the Art with AI' if config.is_production() else 'DEV State of the Art with AI'
st.set_page_config(page_title=title, layout="wide", initial_sidebar_state='expanded', menu_items=None)



# Define pages
pages = {
    "": [
        st.Page("pages/read_backlog_page.py", title="Read Backlog", url_path="read_backlog_page"),
        st.Page("pages/image_evaluator.py", title="Image Evaluator", url_path="image_evaluator"),
        st.Page("pages/ai_automation_page.py", title="AI Automation", url_path="ai_automation_page"),
        st.Page("pages/all_papers_page.py", title="Latest Articles", url_path="all_papers_page"),
        st.Page("pages/recommendations_page.py", title="Recommendations", url_path="recommendations_page"),
        st.Page("pages/interests_page.py", title="Your Interests", url_path="interests_page"),
        st.Page("pages/your_papers_page.py", title="Your Articles", url_path="your_papers_page"),
        st.Page("pages/papers_with_insights_generated_page.py", title="Papers with Insights Generated", url_path="papers_with_insights_generated_page"),
        st.Page("pages/profile_page.py", title="Your Profile", url_path="profile_page"),
        st.Page("pages/paper_details_page.py", title="Article Details", url_path="paper_details_page"),
        st.Page("pages/learning_assistant_page.py", title="Exercise Learning Assistant", url_path="learning_assistant_page"),
        st.Page("pages/article_url_translation_page.py", title="Article Translation", url_path="article_url_translation_page"),
        st.Page("pages/content_translation_page.py", title="Content Translation", url_path="content_translation_page"),
        st.Page("pages/energy_tracker.py", title="Energy Tracker", url_path="energy_tracker"),
        st.Page("pages/admin_page.py", title="Admin", url_path="admin_page"),
    ],
}

pg = st.navigation(pages)
pg.run()
