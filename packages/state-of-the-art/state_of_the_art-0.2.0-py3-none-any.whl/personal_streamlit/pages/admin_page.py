import streamlit as st
from state_of_the_art.infrastructure.shell import ShellRunner
from state_of_the_art.recommenders.recommendations_email import RecommendationsEmail
from state_of_the_art.tables.changelog_table import Changelog
from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page
initialize_page()


tab1, tab2 = st.tabs(['Actions', "Changelog"])

with tab1:
    st.link_button("Datadog", 'https://app.datadoghq.eu/dashboard/4bw-h2v-usi/sota?fromUser=false&refresh_mode=sliding&from_ts=1729741790180&to_ts=1729745390180&live=true')
    st.link_button("Cloud run", 'https://console.cloud.google.com/run?referrer=search&hl=en&project=logger-288419')
    st.link_button("Cloud builds", 'https://console.cloud.google.com/cloud-build/builds?hl=en&project=logger-288419')
    st.link_button("Cloud billing", 'https://console.cloud.google.com/billing/013F49-5FC41F-4043B5?hl=en&project=logger-288419&inv=1&invt=AbjlTQ')

    if st.button("Send recommendations email"):
        RecommendationsEmail().send()


    shell_cmd = st.text_input("Shell command")
    if st.button("Run command"):
        with st.status("Running shell commnd"):
            for line in ShellRunner().run_and_yield_intermediate_results(shell_cmd):
                st.write(line)


with tab2: 
    df = Changelog().read(recent_first=True)
    # put first the date time column
    df = df[["tdw_timestamp", "message", "by_user"]]
    # remove seconds from date time
    df["tdw_timestamp"] = df["tdw_timestamp"].dt.strftime("%Y-%m-%d %H:%M")
    # limit to 10
    df = df.head(10)
    # remove index
    df = df.reset_index(drop=True)
    st.write(df)


if st.button("Close panel"):
    st.session_state["admin_panel_clicked"] = False
    st.rerun()
