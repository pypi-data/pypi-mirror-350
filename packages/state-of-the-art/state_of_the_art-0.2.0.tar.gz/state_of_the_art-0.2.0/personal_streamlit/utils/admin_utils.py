import streamlit as st
from state_of_the_art.infrastructure.s3 import S3
from state_of_the_art.infrastructure.shell import ShellRunner
from state_of_the_art.register_papers.arxiv_miner import ArxivMiner
from state_of_the_art.tables.changelog_table import Changelog
from state_of_the_art.tables.open_tasks_table import TasksTable
from state_of_the_art.tasks_queue.TasksRunner import TasksRunner


def task_manager_view():
    df = TasksTable().read(recent_first=True)
    df = df.head(5)
    # drop column task_name
    df = df.drop(columns=["task_name"])
    st.write(df)
    if st.button("Run a task"):
        with st.status("Running task... "):
            for line in TasksRunner().run_a_pending_task(yield_info=True):
                st.write(line)

    if st.button("Get slo status"):
        with st.status("Getting slo status"):
            result = ShellRunner().run_waiting("sota RecommenderDeliverySLO check")
            st.write(result)
    
def actions_view():
    if st.button("Mine all keywords"):
        with st.status("Mining all keywords"):
            for line in ArxivMiner().mine_all_keywords():
                st.write(line)

    # column for the button and the checkbox
    col1, col2 = st.columns(2)  
    with col1:
            # checkbox i do understand the risks
        marked_checkbox = st.checkbox("I do understand the risks")
    with col2:

        push_data_clicked = st.button("Push data")
        if push_data_clicked and not marked_checkbox:
            st.error("You must accept the risks")

        if push_data_clicked and marked_checkbox:
            S3().push_data_to_s3()
            st.success("Data pushed successfully")

    if st.button("Pull s3 data"):
        with st.status("Pulling data"):
            for out in S3().pull_data_iterator():
                st.write(out)

    shell_cmd = st.text_input("Shell command")
    if st.button("Run command"):
        with st.status("Running shell commnd"):
            for line in ShellRunner().run_and_yield_intermediate_results(shell_cmd):
                st.write(line)


def changelog_view():
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


@st.dialog("Admin panel")
def admin_panel():
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Changelog", "Generate recos", 'Actions', "Tasks Manager", "Observability"])

    with tab1: 
        # changelog
        changelog_view()
    with tab2:
        number_of_days = st.number_input("Number of days to cover", value=1, min_value=1, max_value=10)
        if st.button("Generate recos syncronous"):
            with st.status("Generating recos syncronous"):
                for line in ShellRunner().run_and_yield_intermediate_results(f"sota InterestsRecommender generate -n {number_of_days}"):
                    st.write(line)
    with tab3:
        actions_view()
    with tab4:
        task_manager_view()
    with tab5:
        st.link_button("Datadog", 'https://app.datadoghq.eu/dashboard/4bw-h2v-usi/sota?fromUser=false&refresh_mode=sliding&from_ts=1729741790180&to_ts=1729745390180&live=true')
        st.link_button("Cloud run", 'https://console.cloud.google.com/run?referrer=search&hl=en&project=logger-288419')
        st.link_button("Cloud builds", 'https://console.cloud.google.com/cloud-build/builds?hl=en&project=logger-288419')
    
    if st.button("Close panel"):
        st.session_state["admin_panel_clicked"] = False
        st.rerun()
