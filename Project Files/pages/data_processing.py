import os
import streamlit as st
import pandas as pd
import capstone_with_input as capstone
import graphviz
import time
import datetime

def generate_mto_flow_graph():
    """Return a Graphviz Digraph object for the MTO process flow."""
    dot = graphviz.Digraph(comment="MTO Process Flow")
    
    # Nodes
    dot.node("START", "VA01:\nCustomer Orders", shape = "oval", style = "filled", color="#404246", fontcolor = "white")
    dot.node("SO", "Sales Order\n(SO-XXXX)", shape="box", style="filled", color="#1976d2", fontcolor="white")
    dot.node("PL", "Planned Order\n(PLN-XXXX)", shape="box", style="filled", color="#0288d1", fontcolor="white")
    dot.node("PO", "Production Order\n(PO-XXXX)", shape="box", style="filled", color="#388e3c", fontcolor="white")
    dot.node("CF", "Confirmation", shape="ellipse", style="filled", color="#2e7d32", fontcolor="white")
    dot.node("DL", "Delivery", shape="box", style="filled", color="#fbc02d", fontcolor="black")
    dot.node("BL", "Billing\n(Invoice INV-XXXX)", shape="box", style="filled", color="#e64a19", fontcolor="white")

    # Edges
    dot.edge("START","SO", label = " Generate Sales Order")
    dot.edge("SO", "PL", label="  Auto-generate Planned Order")
    dot.edge("PL", "PO", label="  Convert Planned Order to Production Order")
    dot.edge("PO", "CF", label="  Confirm Production Order")
    dot.edge("CF", "DL", label="  Ship/Deliver Product")
    dot.edge("DL", "BL", label="  Generate Invoice & Payment")

    return dot

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
            if st.button("Run Batch New (Overwrite)"):
                capstone.run_batch_mode(tmp_batch_path)
                st.success("Batch processed successfully (overwrite).")
                st.rerun()
        with col2:
            if st.button("Run Batch Add (Append)"):
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

    st.markdown("---")

    # --- Single Order ---
    st.subheader("➕ Add New Order (VA01)")
    va01 = st.text_input("CODE")
    customer = st.text_input("Customer")
    product = st.text_input("Product")
    qty = st.number_input("Quantity", min_value=1, step=1)
    price = st.number_input("Price per unit", min_value=0.0, step=0.01)
    order_date = st.date_input(
    "Order Date",
    value=datetime.date(2003,1,1),
    min_value=datetime.date(2003, 1, 1),   # <-- set earliest date allowed
    max_value=datetime.date(2005, 12, 31)  # <-- optional upper bound
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

    st.markdown("---")
    st.subheader("📑 Process Flow Documentation")

    # Show the flow chart inside the dashboard
    flow_chart = generate_mto_flow_graph()
    st.graphviz_chart(flow_chart)

    # Export as PDF
    if st.button("⚙️ Generate Process Flow PDF"):
        pdf_path = "mto_process_flow"
        flow_chart.render(pdf_path, format="pdf", cleanup=True)
        with open(pdf_path + ".pdf", "rb") as f:
            st.download_button("⬇️ Download Process Flow", f, file_name="mto_process_flow.pdf")
