import streamlit as st
import pandas as pd

def show_kpis(df: pd.DataFrame):
    """Render KPI metric tiles from the dashboard DataFrame."""
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        st.metric("Total Orders", len(df))
    with col2: 
        st.metric("Confirmed Orders", int(df["Confirmed"].sum()) if "Confirmed" in df.columns else 0)
    with col3: 
        st.metric("Delivered Orders", int((df["Delivery"] == "Delivered").sum()) if "Delivery" in df.columns else 0)
    with col4: 
        st.metric("Total Revenue ($)", f"{df['Amount'].sum():,.2f}" if "Amount" in df.columns else "0.00")
