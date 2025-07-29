from typing import Generator, List, Optional, Union
from state_of_the_art.streamlit_app.utils.ai_gen_utils import extract_ai_insights
from state_of_the_art.streamlit_app.utils.paper_details_utils import render_tags_for_paper
from state_of_the_art.paper.paper_entity import Paper
from state_of_the_art.relevance_model.text_evaluation_inference import PersonalPreferenceInference
from state_of_the_art.search.bm25_search import Bm25Search
from state_of_the_art.tables.insights_table import InsightsTable
from state_of_the_art.tables.tags_table import TagsTable
import streamlit as st

from state_of_the_art.config import config
from state_of_the_art.text_feedback.feedback_elements import render_feedback


@st.dialog("More details")
def preview(paper):
    st.markdown("Title: " + paper.title)
    st.markdown(paper.abstract)


tags_table = TagsTable()

def render_papers():
    pass


class PapersRenderer:
    def __init__(self, disable_save_button=False, disable_metadata=False, enable_tags=False):
        self.disable_save_button = disable_save_button
        self.disable_metadata = disable_metadata
        self.enable_tags = enable_tags
        self.current_page = int(st.query_params.get("pagination", 1))
        self.total_papers_given = None
        self.PAGE_SIZE = 10

    def render(
        self,
        papers: Optional[Union[List[Paper], Generator[Paper, str, None]]] = None,
        papers_metadata: Optional[dict[str, str]] = None,
        generated_date=None,
        metadata: Optional[dict[str, str]] = None,
        max_num_of_renderable_results=None,
        expand_metadata=True,
    ):
        """
        Render papers in a paginated manner.

        """
        self._format_page()

        if not papers:
            st.warning("No papers found")
            return

        paper_list_is_generator = isinstance(papers, Generator)
        

        with st.expander("Narrow down papers", expanded=True if 'narrow_down_query' in st.query_params else False):
            narrow_down_query = st.text_input("Query", key="narrow_down_query", value=st.query_params.get('narrow_down_query', ''))
            if st.button("Search", key="narrow_down_button"):

                st.query_params['narrow_down_query'] = narrow_down_query

                with st.spinner("Filtering papers..."):
                    if narrow_down_query:
                        papers = Bm25Search(papers).search_returning_papers(narrow_down_query, get_all_papers=True)
                        if not metadata:
                            metadata = {}
                        metadata['Narrowed down query'] = narrow_down_query
            if st.button("Reset", key="narrow_down_reset"):
                st.query_params.pop('narrow_down_query', None)
                st.rerun()


        if not self.disable_metadata:
            with st.expander("Results information", expanded=expand_metadata):
                if generated_date:
                    st.markdown(f"**Generated at:** {str(generated_date).split('.')[0]}")
                    st.markdown(f"**Page:** {self.current_page}")
                if metadata:
                    for i, (k, v) in enumerate(metadata.items()):
                        st.markdown(f"**{k}:** {v}")
        st.divider()


        insights_table = InsightsTable()

        # Render papers
        for k, paper in enumerate(papers):
            if max_num_of_renderable_results and k > max_num_of_renderable_results:
                break

            paper_metadata = papers_metadata[paper.abstract_url] if papers_metadata and paper.abstract_url in papers_metadata else None

            # test if paper is a tuple

            if isinstance(paper, tuple):
                paper_metadata = paper[1]
                paper = paper[0]

            with st.container():
                self._render_single_paper(k, paper, paper_metadata, insights_table)
        
        st.divider()

        if not paper_list_is_generator:
            papers = self._paginate_paper_list(papers)
            st.query_params['pagination'] = self.current_page
            self.total_papers_given = len(papers)

            self._render_pagination_ui(position='bottom')

    def _render_single_paper(self, paper_index: int, paper: Paper, paper_metadata: dict, insights_table: InsightsTable):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f'<div class="paper-title">{paper_index+1+((self.current_page-1)*self.PAGE_SIZE)}. <a href="./paper_details_page?paper_id={paper.id}">{paper.title}</a>   </div>', unsafe_allow_html=True)
            st.markdown(f'<div class="paper-metadata">Published: {paper.published_date_str()}</div>', unsafe_allow_html=True)

            institution = insights_table.get_lastest_answer("Institution", paper.abstract_url)
            if institution:
                st.markdown(f'<div class="paper-metadata">Institution: {institution}</div>', unsafe_allow_html=True)

            
            if (paper_metadata and "labels" in paper_metadata):
                labels = paper_metadata["labels"]
                st.markdown(f'<div class="paper-metadata">Labels: {", ".join(labels)}</div>', unsafe_allow_html=True)
            

            insights = insights_table.get_all_answers_for_question_in_paper("TopInsights", paper.abstract_url)
            if insights:
                # sort by relevance
                scores = PersonalPreferenceInference().predict_batch(insights)
                # save insights and scores together
                insights_and_scores = list(zip(insights, scores))
                insights_and_scores.sort(key=lambda x: x[1], reverse=True)
            
            if len(insights) > 0:
                with st.expander("Top Insights", expanded=False):
                    for insight, score in insights_and_scores[:3]:
                        st.markdown(f'<div class="paper-insights">{insight} ({score})</div>', unsafe_allow_html=True)
                        render_feedback(insight, type="paper_insight", context={'paper_id': paper.abstract_url}, extra_identifier=f"insights_paper_position{paper_index}")
            else:
                with st.expander("Abstract", expanded=False):
                    st.markdown(f'<div class="paper-abstract">{paper.abstract}</div>', unsafe_allow_html=True)

        
        with col2:
            render_feedback(paper.title, type='paper_title', extra_identifier=f"paper_title_position{paper_index}")
            
            if not self.disable_save_button:
                if st.button("Save Paper", key=f"save_{paper_index}"):
                    tags_table.add_tag_to_paper(paper.abstract_url, "save for later")
                    st.success("Saved")
            
            if self.enable_tags:
                if st.button('Change Tags', key=f"tags_{paper_index}") or st.session_state.get(f'change_tags_for_{paper_index}', False):
                    st.session_state[f'change_tags_for_{paper_index}'] = True
                    render_tags_for_paper(paper)

            if st.button("Generate AI Insights", key=f"ai_insights_{paper_index}"):
                extract_ai_insights(paper.abstract_url)
            
        
    def _paginate_paper_list(self, paper_list: List[Paper]):
        self.current_page = int(st.query_params.get("pagination", 1))
        self.from_index = (self.current_page - 1) * self.PAGE_SIZE
        self.to_index = self.from_index + self.PAGE_SIZE
        return paper_list[self.from_index:self.to_index]
    

    def _format_page(self):
        # Add custom CSS for better styling
        st.markdown("""
        <style>
        .element-container {
            margin-bottom: 0.5rem;
        }
        .paper-container {
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .paper-title {
            color: #4e8cff;
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .paper-insights {
            border-left: 3px solid #4e8cff;
            padding-left: 0.5rem;
            margin-top: 0.5rem;
        }
        /* Dark mode adjustments */
        @media (prefers-color-scheme: dark) {
            .paper-container {
                border-color: rgba(250, 250, 250, 0.2);
            }
            .paper-title {
                color: #6c9fff;
            }
        }
        .paper-title a {
            color: inherit;
            text-decoration: none;
        }
        .paper-title a:hover {
            text-decoration: underline;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _render_pagination_ui(self, position='top'):
        if self.total_papers_given <= self.PAGE_SIZE:
            return

        total_pages = (self.total_papers_given + self.PAGE_SIZE - 1) // self.PAGE_SIZE
        
        st.markdown("""
        <style>
        .pagination-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 5px 0;
        }
        .pagination-button {
            margin: 0 5px;
        }
        .pagination-info {
            margin: 0 5px;
            font-size: 0.9em;
            color: #888;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            if st.button("⏪ First", key=f"first_{position}", disabled=self.current_page == 1):
                self.current_page = 1
                self._update_page()

        with col2:
            if st.button("◀ Previous", key=f"previous_{position}", disabled=self.current_page == 1):
                self.current_page = max(1, self.current_page - 1)
                self._update_page()

        with col3:
            if st.button("Next ▶", key=f"next_{position}", disabled=self.current_page == total_pages):
                self.current_page = min(total_pages, self.current_page + 1)
                self._update_page()

        with col4:
            if st.button("Last ⏩", key=f"last_{position}", disabled=self.current_page == total_pages):
                self.current_page = total_pages
                self._update_page()

    def _update_page(self):
        st.query_params['pagination'] = self.current_page
        st.rerun()
