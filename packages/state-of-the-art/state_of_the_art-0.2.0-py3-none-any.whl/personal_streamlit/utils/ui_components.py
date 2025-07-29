import datetime
import streamlit as st

from state_of_the_art.text_feedback.feedback_elements import render_feedback

def styled_button(label, on_click=None):
    custom_css = """
        <style>
        .stButton > button {
            color: #4F8BF9;
            border-radius: 4px;
            border: 1px solid #4F8BF9;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #4F8BF9;
        }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    return st.button(
        label,
        on_click=on_click,
        use_container_width=True,
    )

def styled_expander(title, content, opened=False):
    with st.expander(title, expanded=opened):
        if isinstance(content, list):
            for item in content:
                st.markdown(f"- {item}")
                render_feedback(item)
        else:
            st.markdown(content)
            render_feedback(content)

def styled_header(label, value):
    st.markdown(f"**{label}**")
    st.markdown(f"<p style='font-size: 1.2em;'>{value}</p>", unsafe_allow_html=True)


def render_date_filters(default_date_from = None, default_date_to = None, numbers_of_days_lookback = 3):
    default_date_to = default_date_from or datetime.datetime.now().date()
    # by default date_from is 3 days in the past from date_to
    default_date_from = default_date_to - datetime.timedelta(days=numbers_of_days_lookback)


    default_date_from = st.query_params.get("date_from", default_date_from)
    if isinstance(default_date_from, str):
        default_date_from = datetime.datetime.strptime(default_date_from, "%Y-%m-%d").date()
    
    default_date_to = st.query_params.get("date_to", default_date_to)
    if isinstance(default_date_to, str):
        default_date_to = datetime.datetime.strptime(default_date_to, "%Y-%m-%d").date()

    date_from = st.date_input("Date or Date From", value=default_date_from)
    date_to = st.date_input("Date To", value=default_date_to)

    st.query_params["date_from"] = date_from
    st.query_params["date_to"] = date_to

    return date_from, date_to
