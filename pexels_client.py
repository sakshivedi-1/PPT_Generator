import streamlit as st
import requests

def get_image_url(api_key, query):
    """Fetches an image URL from Pexels API based on a query."""
    try:
        headers = {"Authorization": api_key}
        params = {"query": query, "per_page": 1, "orientation": "landscape"}
        url = "https://api.pexels.com/v1/search"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data["photos"]:
            return data["photos"][0]['src']['large']
        else: # Fallback query
            params['query'] = 'abstract technology background'
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if data["photos"]:
                return data["photos"][0]['src']['large']
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not fetch image from Pexels: {e}")
    return None