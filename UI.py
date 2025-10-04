
import streamlit as st

def render_ui():
    """
    Renders the Streamlit user interface and returns the user's inputs.
    """
    st.set_page_config(page_title="AI Presentation Generator", page_icon="✨", layout="wide")
    st.title("AI Presentation Generator (with Gemini)")

    with st.sidebar:
        st.header(" API Keys")
        google_api_key = st.text_input("Google Gemini API Key", type="password", help="Get yours from aistudio.google.com")
        pexels_api_key = st.text_input("Pexels API Key", type="password", help="Get yours from pexels.com/api/")

        st.header(" Presentation Settings")
        domain = st.selectbox("Select Domain", ["Business", "Academic", "Technology", "Creative", "General"])
        slide_count = st.slider("Number of Content Slides", min_value=3, max_value=10, value=5)

    st.header(" Enter Your Topic")
    topic = st.text_input("What is the presentation about?", placeholder="e.g., 'The Future of Renewable Energy'")
    additional_context = st.text_area("Add any specific details or a document abstract here (optional)")

    # The generate button is part of the UI, but its logic will be in app.py
    generate_button = st.button(" Generate Presentation", type="primary")

    # Return all the user inputs in a dictionary for the main app to use
    return {
        "google_api_key": google_api_key,
        "pexels_api_key": pexels_api_key,
        "domain": domain,
        "slide_count": slide_count,
        "topic": topic,
        "additional_context": additional_context,
        "generate_button": generate_button
    }