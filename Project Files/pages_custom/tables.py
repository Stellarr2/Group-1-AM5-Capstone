import streamlit as st
from utils import tables
from utils import kpis

def show_tables(df): # Tables for Raw Data
    kpis.show_kpis(df)

    st.title("📋 Tables")
    if df.empty:
        st.warning("No data to show.")
        return

    st.subheader("📦 Active Production Orders")
    tables.active_orders_table(df)

    st.subheader("💳 Billing Overview")
    tables.billing_table(df)

    st.subheader("📚 Full Order History")
    tables.full_history_table(df)
