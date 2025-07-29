import streamlit as st
import subprocess

from personal_streamlit.utils.help_utils import help_modal
from personal_streamlit.utils.login_utils import LoginInterface, setup_login
from personal_streamlit.utils.paper_details_utils import create_custom_paper
from state_of_the_art.infrastructure.s3 import S3
from state_of_the_art.register_papers.arxiv_miner import ArxivMiner
from state_of_the_art.utils.git import get_commit_hash


@st.cache_data
def get_last_release_date():
    p = subprocess.Popen(
        "uptime", shell=True, text=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    out, error = p.communicate()
    time_up = out.split(" up ")[1].split(",")[0]
    return time_up


def render_sidebar():
    # Custom CSS for a more professional look
    st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-image: linear-gradient(#2e7bcf,#2e7bcf);
            color: white;
        }
        .sidebar .sidebar-content .stButton>button {
            width: 100%;
            border-radius: 5px;
            background-color: #ffffff;
            color: #2e7bcf;
        }
        .sidebar .sidebar-content .stButton>button:hover {
            background-color: #f0f0f0;
            color: #1e5b9f;
        }
        .reportview-container .main .block-container {
            padding-top: 2rem;
        }
        h1, h2, h3 {
            color: #2e7bcf;
        }
    </style>
    """, unsafe_allow_html=True)
    # Sidebar content
    with st.sidebar:
        #st.image("path/to/your/logo.png", width=200)  # Add your logo here
        #username = LoginInterface.get_session().get_user().get_name()
        #if username:
        #    st.markdown(f"### Welcome, {username}!")

        if st.button("Push data"):
            with st.status("Pushing data"):
                S3().sync_local_to_s3()
                st.success("Data pushed successfully")

        if st.button("Pull data"):
            with st.status("Pulling data"):
                for out in S3().pull_data_iterator():
                    st.write(out)


        if st.button("New Article"):
            create_custom_paper()

        if st.button("Mine Articles"):
            with st.status("Mining new papers from arxiv"):
                for line in ArxivMiner().mine_all_keywords():
                    st.write(line)



        # renders the logout button
        LoginInterface.get_session().get_authenticator().logout()
        st.info(f"Commit: {get_commit_hash()}")

def initialize_page():
    setup_login()
    render_sidebar()
