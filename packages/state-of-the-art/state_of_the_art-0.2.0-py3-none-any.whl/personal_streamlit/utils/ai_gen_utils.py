from state_of_the_art.infrastructure.shell import ShellRunner
import time
from state_of_the_art.tables.changelog_table import Changelog

import streamlit as st


@st.dialog("Generating insights...")
def extract_ai_insights(url: str):
    try:    
        with st.status("Insights generation in progress...") or st.session_state.get("ai_insights_status", None):
            st.session_state.ai_insights_status = "started"
            st.write("Generation started. This can take a while... ")
            for out in ShellRunner().run_and_yield_intermediate_results(f"sota InsightExtractor extract_insights_from_paper_url '{url}'", exception_on_error=True):
                st.write(f"{out}")
            
            Changelog().add_log(message=f"AI Insights generated for paper {url}", by_user=st.session_state.get("user_id", None))
            st.write("Generation completed")
            del st.session_state['ai_insights_status'] 
            # sleep 4 seconds
            time.sleep(4)
            st.rerun()
    except Exception as e:
        st.error(f"Error generating insights: {e}")
        return
