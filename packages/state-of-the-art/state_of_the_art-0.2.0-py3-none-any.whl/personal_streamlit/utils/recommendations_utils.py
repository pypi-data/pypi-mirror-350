import datetime

import subprocess
import time
import json
from typing import List

import streamlit as st

from state_of_the_art.streamlit_app.utils.login_utils import LoginInterface
from state_of_the_art.streamlit_app.utils.papers_renderer import PapersRenderer
from state_of_the_art.paper.paper_entity import Paper
from state_of_the_art.paper.papers_data_loader import PapersLoader
from state_of_the_art.relevance_model.text_evaluation_inference import PersonalPreferenceInference
from state_of_the_art.tables.recommendations_history_table import UserRecommendationsHistoryTable

score_legend = {
    'bm25_score': 'B25',
    'semantic_score': 'Semantic',
    'text_evaluation_score': 'Text',
    'final_score': 'Final',
}

def generate_new_recommendations(number_of_days_to_look_back):
    import streamlit as st
    with st.status("Generating recommendations..."):
        st.write(f"Generating recommendations for the last {number_of_days_to_look_back} day{'s' if number_of_days_to_look_back > 1 else ''}...")
        user_id = LoginInterface.get_session().get_user().get_uuid()
        cmd = f"sota InterestsRecommender generate -n {number_of_days_to_look_back} -u {user_id} & "
        st.write('Running command: ', cmd)


        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,start_new_session=True)
        # print also stderr
        # add seconds since start to the output
        start_time = time.time()
        for line in iter(process.stdout.readline, b''):
            st.write(f"{time.time() - start_time:.2f}s: {line.decode('utf-8')}")
        for line in iter(process.stderr.readline, b''):
            st.write(f"{time.time() - start_time:.2f}s: {line.decode('utf-8')}")

        if process.returncode != 0:
            st.error("Failed to generate recommendations!")
        else:
            st.success("Recommendations generated successfully!")
            st.rerun()


def score_and_sort_papers(paper_list: List[Paper]) -> List[Paper]:
    if paper_list:
        inference = PersonalPreferenceInference()
        papers_scored = inference.predict_batch([paper.title for paper in paper_list])
        return [paper for _, paper in sorted(zip(papers_scored, paper_list), key=lambda pair: pair[0], reverse=True)]
    return []


def load_deep_recommendations(id_to_load):
    base_recos_df = load_recommendations()
    row_dict = base_recos_df[base_recos_df["tdw_uuid"] == id_to_load].iloc[0].to_dict() if id_to_load else base_recos_df.iloc[0].to_dict()

    papers, papers_metadata = load_papers_and_metadata(row_dict)

    current_time = datetime.datetime.now()
    generation_start_time = datetime.datetime.fromisoformat(row_dict["start_time"])
    time_since_generation = current_time - generation_start_time

    recommendation_metadata = {
        "Number of days": (datetime.datetime.fromisoformat(row_dict["to_date"]) - datetime.datetime.fromisoformat(row_dict["from_date"])).days,
        "Time since generation": f"{time_since_generation.days}d {time_since_generation.seconds // 3600}h {(time_since_generation.seconds // 60) % 60}m ago",
        "Papers from": row_dict["from_date"],
        "Papers to": row_dict["to_date"],
        "Total papers analysed": row_dict["papers_analysed_total"],
        "Id": row_dict["tdw_uuid"],
        "Status": row_dict["status"],
    }
    PapersRenderer().render(
        papers,
        papers_metadata=papers_metadata,
        metadata=recommendation_metadata,
        expand_metadata=False,
    )


def load_papers_and_metadata(row_dict):
    papers = []
    papers_metadata = {}
    if row_dict["recommended_papers"]:
        structured = json.loads(row_dict["recommended_papers"])
        #st.write(structured)
        for recommended_interest in structured["interests"]:
            for recommended_paper in recommended_interest["papers"][:3]:
                paper = PapersLoader().load_papers_from_urls([recommended_paper['url']])[0]
                papers.append(paper)

                labels = [f"{recommended_interest['name']}"]

                for key, value in recommended_paper['scores'].items():
                    letter = score_legend[key]
                    value = round(value, 2) if isinstance(value, float) else value
                    score_label = f"{letter}:{value}"
                    labels.append(score_label)

                if paper.abstract_url not in papers_metadata:
                    papers_metadata[paper.abstract_url] = {"labels": labels}
                else:
                    papers_metadata[paper.abstract_url]["labels"].extend(labels)
    return papers, papers_metadata


def load_recommendations():
    return UserRecommendationsHistoryTable().read(recent_first=True)


def render_old_recommendations_list():
    st.subheader("Recent deep recommendations")
    with st.expander("View all", expanded=False):
        runs = load_recommendations().head(4)

        for run in runs.to_dict(orient='records'):
            current_time = datetime.datetime.now()
            days_covered = (datetime.datetime.fromisoformat(run["to_date"]) - datetime.datetime.fromisoformat(run["from_date"])).days
            time_since_start = current_time - datetime.datetime.fromisoformat(run["start_time"])

            status_color = {
                "error": "🔴",
                "success": "🟢",
                "started": "🟠"
            }.get(run["status"], "⚪")

            error_details = f"- Error: {run['error_details']}" if run["status"] == "error" else ""

            st.markdown(f"""
            {status_color} **Run {run['tdw_uuid'][:4]}** ({run['status']})
            - {days_covered} days covered
            - {run['papers_analysed_total']} papers analyzed
            - {time_since_start.days}d {time_since_start.seconds // 3600}h ago
            {error_details}
            """)

            if st.button("View", key=f"view_{run['tdw_uuid']}"):
                st.query_params.update({"run_id": run["tdw_uuid"]})
                st.rerun()

            st.divider()
