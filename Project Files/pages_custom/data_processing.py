import os
import streamlit as st
import pandas as pd
import capstone_with_input as capstone
from utils.flowchart import generate_mto_flow_graph, offer_flowchart_download
import time
import datetime

def show_data_processing():
    st.title("⚙️ Data Processing")

    # --- Batch Processing ---
    st.subheader("📂 Batch Processing")
    uploaded_csv = st.file_uploader("Upload CSV for Batch Processing", type=["csv"])

    if uploaded_csv is not None:
        tmp_batch_path = "uploaded_batch.csv"
        with open(tmp_batch_path, "wb") as f:
            f.write(uploaded_csv.getbuffer())
        st.success(f"Uploaded file saved as {tmp_batch_path}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Run New Batch (Overwrite)"):
                capstone.run_batch_mode(tmp_batch_path)
                st.success("Batch processed successfully (overwrite).")
                st.rerun()
        with col2:
            if st.button("Add Batch (Append)"):
                try:
                    df_existing = pd.read_csv("dashboard_data.csv")
                except FileNotFoundError:
                    df_existing = pd.DataFrame()

                capstone.run_batch_mode(tmp_batch_path)
                df_new = pd.read_csv("dashboard_data.csv")

                df_combined = pd.concat([df_existing, df_new], ignore_index=True) if not df_existing.empty else df_new
                df_combined.to_csv("dashboard_data.csv", index=False)

                st.success("Batch processed successfully (append).")
                st.rerun()

    # ✅ Always check for batch log, even after rerun
    if os.path.exists("mto_batch_flow_log.txt"):
        with open("mto_batch_flow_log.txt", "rb") as f:
            st.download_button("⬇️ Download Batch Log", f, "mto_batch_flow_log.txt")
    
    if os.path.exists("batch_report.pdf"):
        with open("batch_report.pdf", "rb") as f:
            st.download_button("⬇️ Download Batch Report (PDF)", f, "batch_report.pdf")


    st.markdown("---")

    # --- Single Order ---
    st.subheader("➕ Add Sales Order")

    
    va01 = st.text_input("Transaction Code",type="password",
                         placeholder="Enter Create Sales Order Transaction Code")
    

    if va01 != "VA01":
    
        pass

    else:
        customer = st.text_input("Customer")
        product = st.text_input("Product")
        qty = st.number_input("Quantity", min_value=1, step=10)
        price = st.number_input("Price per unit", min_value=0.0, step=10.0)
        order_date = st.date_input(
        "Order Date",
        value=datetime.date(2003,1,1),
        min_value=datetime.date(2003, 1, 1),   # <-- set earliest date allowed
        max_value=datetime.date(2005, 12, 31)  # <-- upper bound to simulate scenario of dataset
    )
        status = st.selectbox("Status", ["Shipped", "Disputed", "In Process", "On Hold", "Resolved", "Cancelled"])      
            
        if st.button("Add Order"):
            if(va01 == "VA01"):
                capstone.run_input_mode(customer, product, int(qty), float(price), str(order_date), status)
                st.success("Order added successfully.")
                time.sleep(1.4)
                    
                st.rerun()
            else:
                st.warning("WARNING: TRANSACTION CODE MISSING")

    if os.path.exists("mto_input_flow_log.txt"):
            with open("mto_input_flow_log.txt", "rb") as f:
                st.download_button("⬇️ Download Order Log", f, "mto_input_flow_log.txt")
    
    if os.path.exists("input_report.pdf"):
        with open("input_report.pdf", "rb") as f:
            st.download_button("⬇️ Download Input Report (PDF)", f, "input_report.pdf")

    st.markdown("---")
    st.subheader("📑 Process Flow Documentation")

    # Show the flow chart inside the dashboard
    flow_chart = generate_mto_flow_graph()
    with st.container(border=True, height = "content", width=1000):
        st.graphviz_chart(flow_chart, use_container_width=True)

    offer_flowchart_download(flow_chart)