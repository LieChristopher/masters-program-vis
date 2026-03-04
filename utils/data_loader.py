"""
Data loading functions
"""
import json
from pathlib import Path
import streamlit as st

@st.cache_data
def load_data():
    json_path = Path(__file__).parent.parent / "data" / "university_data.json"
    with open(json_path, 'r') as f:
        return json.load(f)

@st.cache_data
def load_countries():
    json_path = Path(__file__).parent.parent / "data" / "countries.json"
    with open(json_path, 'r') as f:
        return json.load(f)

@st.cache_data
def load_exchange_rates():
    json_path = Path(__file__).parent.parent / "data" / "exchange_rates.json"
    with open(json_path, 'r') as f:
        return json.load(f)
