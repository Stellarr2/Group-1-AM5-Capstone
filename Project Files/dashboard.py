import os
import streamlit as st
from utils.loader import load_css, load_dashboard_df
from utils.flowchart import generate_mto_flow_graph, offer_flowchart_download
from pages_custom import charts, tables, data_processing, overview
import time

st.set_page_config(page_title="Group 1: MTO Production Dashboard", layout="wide")
load_css("styles.css")


# Sidebar Navigation
st.sidebar.header("📂 Navigation")
page = st.sidebar.radio("Go to:", ["Overview","Data Processing", "Charts", "Tables"])

# Sidebar Utilities
st.sidebar.subheader("⚙️ Data Management")

# Clear Data
if st.sidebar.button("🗑️ Clear All Data",type="primary"):
    if os.path.exists("dashboard_data.csv"):
        os.remove("dashboard_data.csv")
    if os.path.exists("mto_batch_flow_log.txt"):
        os.remove("mto_batch_flow_log.txt")
    if os.path.exists("mto_input_flow_log.txt"):        
        os.remove("mto_input_flow_log.txt")
    if os.path.exists("mto_process_flow.pdf"):        
        os.remove("mto_process_flow.pdf")
    if os.path.exists("uploaded_batch.csv"):        
        os.remove("uploaded_batch.csv")
    if os.path.exists("batch_report.pdf"):        
        os.remove("batch_report.pdf")
    if os.path.exists("input_report.pdf"):        
        os.remove("input_report.pdf")
        st.sidebar.success("All data cleared. Dashboard reset.")
    else:
        st.sidebar.error("No available data to clear.")
        time.sleep(0.5)
    st.rerun()

# Download CSV
st.sidebar.write("CSV File")
if os.path.exists("dashboard_data.csv"):
    with open("dashboard_data.csv", "rb") as f:
        st.sidebar.download_button("⬇️ Download Dashboard Data", f, "dashboard_data.csv")
else:
    st.sidebar.markdown("No dashboard data available yet.")

# Download Logs
st.sidebar.write("Text Logs")
if os.path.exists("mto_batch_flow_log.txt"):
    with open("mto_batch_flow_log.txt", "rb") as f:
        st.sidebar.download_button("⬇️ Download Batch Log", f, "mto_batch_flow_log.txt")

if os.path.exists("mto_input_flow_log.txt"):
    with open("mto_input_flow_log.txt", "rb") as f:
        st.sidebar.download_button("⬇️ Download Order Log", f, "mto_input_flow_log.txt")

# Download PDFs
st.sidebar.write("PDF Reports")
if os.path.exists("batch_report.pdf"):
    with open("batch_report.pdf", "rb") as f:
        st.sidebar.download_button("⬇️ Download Batch Report (PDF)", f, "batch_report.pdf")

if os.path.exists("input_report.pdf"):
    with open("input_report.pdf", "rb") as f:
        st.sidebar.download_button("⬇️ Download Input Report (PDF)", f, "input_report.pdf")

st.sidebar.write("Flow Chart")
flow_chart = generate_mto_flow_graph()
with st.sidebar.container(): offer_flowchart_download(flow_chart)


# Load Data Once
df = load_dashboard_df()


# Page Routing
if page == "Charts":
    charts.show_charts(df)
elif page == "Tables":
    tables.show_tables(df)
elif page == "Data Processing":
    data_processing.show_data_processing()
elif page == "Overview":
    overview.show_overview(df)
