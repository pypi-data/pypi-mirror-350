from typing import Callable, List, Optional
import streamlit as st
from state_of_the_art.relevance_model.text_evaluation_inference import PersonalPreferenceInference
from state_of_the_art.tables.changelog_table import Changelog
from state_of_the_art.tables.text_feedback_table import TextFeedbackTable

def render_feedback(text: str, type=None, context=None, extra_identifier: Optional[str] = None):
    """
    Render a feedback component for a given text.

    Args:
        text (str): The text to render the feedback for.
        type (str): The type of feedback to render.
        context (dict): The context to render the feedback for.
        extra_identifier (Optional[str]): An extra identifier to add to the feedback component.
    """
    id = text 
    if extra_identifier:
        id = id + extra_identifier
    id = "".join([i for i in id if i.isalnum()])
    try:  
        feedback_score = st.feedback(options="faces", key=f"feedback{id}")
    except Exception as e:
        st.error(f"Failed to render feedback {e}")
        return
    
    if feedback_score is not None:
        with st.spinner("Sending feedback..."):
            TextFeedbackTable().add_feedback(
                text=text,
                score=feedback_score,
                type=type,
                context=context
            )
            message = f"Feedback {feedback_score} added for text {text[:15]}..."
            Changelog().add_log(message=message, by_user=st.session_state.get("user_id", None))
            st.success(message)

class TextWithFeedback():
    def __init__(self):
        self.inference = PersonalPreferenceInference.get_instance()

    def render_batch(self, texts: List[str], element: Callable, paper_id: Optional[str] = None):
        predictions = self.inference.predict_batch(texts)
        # sort texts by prediction
        texts = [x for _, x in sorted(zip(predictions, texts), key=lambda pair: pair[0], reverse=True)]
        predictions = sorted(predictions, reverse=True)
        for text, prediction in zip(texts, predictions):
            self.render(text, element, paper_id, prediction)

    def render(self, text: str, element: Callable, paper_id: Optional[str] = None, existing_prediction: Optional[int] = None):
        if not type(text) == str:
            raise ValueError(f"Text must be a string, got {type(text)}")

        element(text + f" (Prediction: {existing_prediction or self.inference.predict(text)})")
        context = {}
        if paper_id:
            context = {
                "paper_id": paper_id
            }
        render_feedback(text, type="paper_insight", context=context)
