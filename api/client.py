import requests
import streamlit as st

API_KEY = st.secrets['API_KEY']
API_HOST = 'insightsentry.p.rapidapi.com'
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST,
}

def get(endpoint: str, params: dict = None) -> dict:
    """Generic GET request with RapidAPI headers."""
    url = f"https://{API_HOST}{endpoint}"
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()