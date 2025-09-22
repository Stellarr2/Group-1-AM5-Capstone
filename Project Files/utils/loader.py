import os
import pandas as pd
import streamlit as st

def load_css(file_name: str):
    """Load external CSS file into Streamlit app."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def load_dashboard_df():
    """Safely load dashboard_data.csv into a DataFrame."""
    if os.path.exists("dashboard_data.csv"):
        try:
            return pd.read_csv("dashboard_data.csv")
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()
