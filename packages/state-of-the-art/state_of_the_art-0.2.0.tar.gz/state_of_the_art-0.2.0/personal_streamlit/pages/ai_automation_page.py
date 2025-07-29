from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page
from state_of_the_art.ai_automation.prompts import DefineTopic, GermanEmail, LearnEfficiently
initialize_page()
import streamlit as st
st.title("AI Automation")


message = st.text_area("Input something", height=250)

def render_output(function, message):
    with st.spinner("Generating..."):
        result = function(message)
    st.write("Input: " + message)
    st.write("Output: " + result)

columns = st.columns(3)
llm_call = None
with columns[0]:
    if st.button("Define Topic"):
        llm_call = DefineTopic().define

with columns[1]:
    if st.button("Generate German Email"):
        llm_call = GermanEmail().compose

with columns[2]:
    if st.button("Learn Efficiently"):
        llm_call = LearnEfficiently().give_advice

if llm_call is not None:
    render_output(llm_call, message)
