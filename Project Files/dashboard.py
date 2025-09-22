import os
import streamlit as st
from utils.loader import load_css, load_dashboard_df
from pages import charts, tables, data_processing
import time

st.set_page_config(page_title="MTO Production Dashboard", layout="wide")
load_css("styles.css")


# Sidebar Navigation
st.sidebar.header("📂 Navigation")
page = st.sidebar.radio("Go to:", ["Data Processing", "Charts", "Tables"])

# Sidebar Utilities
st.sidebar.subheader("⚙️ Data Utilities")

# Clear Data
if st.sidebar.button("🗑️ Clear All Data"):
    if os.path.exists("dashboard_data.csv"):
        os.remove("dashboard_data.csv")
    if os.path.exists("mto_batch_flow_log.txt"):
        os.remove("mto_batch_flow_log.txt")
    if os.path.exists("mto_input_flow_log.txt"):        
        os.remove("mto_input_flow_log.txt")
    if os.path.exists("mto_process_flow.pdf"):        
        os.remove("mto_process_flow.pdf")
        st.sidebar.success("All data cleared. Dashboard reset.")
    else:
        st.sidebar.error("No available data to clear.")
        time.sleep(0.5)
    st.rerun()

# Download CSV
if os.path.exists("dashboard_data.csv"):
    with open("dashboard_data.csv", "rb") as f:
        st.sidebar.download_button("⬇️ Download dashboard_data.csv", f, "dashboard_data.csv")
else:
    st.sidebar.markdown("No dashboard data available yet.")

# Download Logs
if os.path.exists("mto_batch_flow_log.txt"):
    with open("mto_batch_flow_log.txt", "rb") as f:
        st.sidebar.download_button("⬇️ Download Batch Log", f, "mto_batch_flow_log.txt")

if os.path.exists("mto_input_flow_log.txt"):
    with open("mto_input_flow_log.txt", "rb") as f:
        st.sidebar.download_button("⬇️ Download Order Log", f, "mto_input_flow_log.txt")

# Load Data Once
df = load_dashboard_df()


# Page Routing
if page == "Charts":
    charts.show_charts(df)
elif page == "Tables":
    tables.show_tables(df)
elif page == "Data Processing":
    data_processing.show_data_processing()
