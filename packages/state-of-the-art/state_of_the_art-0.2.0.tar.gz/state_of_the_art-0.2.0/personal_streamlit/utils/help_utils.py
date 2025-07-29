import streamlit as st


@st.dialog("Help")
def help_modal():
    st.markdown("""
    # Welcome to State of the Art with AI!

    Here's how to get started:
    
    1. Use the sidebar to navigate between different pages.
    2. Define your interests on the "Your Interests" page to get personalized recommendations.
    3. Explore the latest papers and load your own into the app.
    4. Save papers for later and explore them again.
    5. Generate automatic AI insights on your papers.
    If you need assistance, please contact me at machado.c.jean@gmail.com

    Jean
    """)

    st.link_button(
        "Give us Feedback",
        "https://docs.google.com/forms/d/e/1FAIpQLSffU-t3PBVLaqsW_5QF9JqnO8oFXGyHjLw0I6nfYvJ6QSztVA/viewform",
        use_container_width=True
    )
