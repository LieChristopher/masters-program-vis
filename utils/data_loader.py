"""
Data loading functions
"""
import json
from pathlib import Path
import streamlit as st

@st.cache_data
def load_data():
    json_path = Path(__file__).parent.parent / "university_data.json"
    with open(json_path, 'r') as f:
        return json.load(f)
