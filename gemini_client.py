import streamlit as st
import google.generativeai as genai

def generate_content(api_key, prompt_text, model_name="gemini-pro"):
    """Generic function to get a response from Google's Gemini API."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt_text)
        if not response.parts:
            st.error("The model's response was empty. This might be due to safety settings or an internal error. Please try a different topic.")
            return None
        return response.text
    except Exception as e:
        st.error(f"A Google Gemini API error occurred: {e}")
        return None