import streamlit as st
import random
from state_of_the_art.streamlit_app.utils.sidebar_utils import initialize_page
from state_of_the_art.learning_assistant.exercise_generator import AnswerChecker, ExerciseGenerator

initialize_page()

temperature = random.uniform(0.0, 2.0)
st.title("Learning Assistant")


# get topic from query params
topic = st.query_params.get("topic", "")
topic = st.text_input("Topic", value=topic, key="topic")
# save topic in query params
st.query_params["topic"] = topic


def cleanup_exercise(exercise: str) -> str:
    # remove the [CORRECT] from the exercise
    exercise = exercise.replace("[CORRECT]", "")
    # remove everything after the explanation
    exercise = exercise.replace("**", "")
    exercise = exercise.split("Explanation")[0]
    # make string again
    exercise = "".join(exercise)
    return exercise

def generate_exercise(topic: str) -> str:
    global temperature
    temperature = random.uniform(0.0, 2.0)
    with st.spinner("Generating exercise"):      
        current_exercise = ExerciseGenerator().generate_exercise(topic, temperature=temperature)
        st.session_state["current_exercise"] = current_exercise

c1, c2 = st.columns([1, 1])
with c1:
    if st.button("Generate New Exercise"):
        if not topic:
            st.write("Please type a topic first")
            st.stop()
        generate_exercise(topic)
with c2:
    st.metric("Temperature", f"{temperature:.2f}")

if not st.session_state.get("current_exercise") and topic:
    generate_exercise(topic)

st.write(cleanup_exercise(st.session_state.get("current_exercise", "")))

answer = st.text_input("Type your answer")


if st.button("Check Answer"):
    checker = AnswerChecker()
    if not st.session_state.get("current_exercise"):
        st.warning("Please generate an exercise first")
        st.stop()
    result, correct_option_number = checker.correct_answer(st.session_state["current_exercise"], answer)
    if result:
        st.success("Correct!")
    else:
        st.error(f"Incorrect! The correct option is '{correct_option_number}'")
    
    # get the explanation
    explanation = st.session_state["current_exercise"].split("Explanation")[1]
    st.write(explanation)
