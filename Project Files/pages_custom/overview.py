from utils.kpis import show_kpis
from utils.flowchart import generate_mto_flow_graph, offer_flowchart_download
import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd

def show_overview(df: pd.DataFrame):
    show_kpis(df)

    st.markdown("---")
    st.title("📘 Make-to-Order (MTO) Process — Overview")
    st.markdown(
        """
This page explains the Make-to-Order (MTO) process used in this project.
"""
    )

    st.header("What is Make-to-Order (MTO)?")
    st.markdown(
        """
Make-to-Order is a production strategy in which goods are manufactured once a confirmed customer order is received.
Unlike make-to-stock (where products are produced ahead of demand), MTO focuses resources on fulfilling **specific customer requests**.
This project simulates that lifecycle and produces a dataset you can analyze in the dashboard.
"""
    )

    st.header("High-level Process (short)")
    st.markdown(
        """
Sales Order -> Planned Order -> Production Order -> Confirmation -> Delivery -> Billing.

Each step transforms the order and adds status information that the dashboard uses for KPIs, charts, and tables.
"""
    )

    st.header("Process Details")
    st.markdown(
        """
Below is a short, human-friendly description of each step. Expand each item to read a bit more.
"""
    )
    with st.expander("Sales Order"):
        st.write(
            """
A Sales Order is the original order from a customer. It contains the customer name, product (or product line),
quantity, unit price, order date, and a free-form STATUS field that will drive business decisions.
In batch mode the app expects CSV rows with columns such as `CUSTOMERNAME`, `PRODUCTLINE`, `QUANTITYORDERED`, `PRICEEACH`, `ORDERDATE`, `STATUS`.
"""
        )

    with st.expander("Planned Order"):
        st.write(
            """
A Planned Order is generated automatically from the Sales Order. It represents the instruction to plan capacity,
reserve materials, and schedule production for the requested quantity.
The Planned Order links back to the Sales Order for traceability.
"""
        )

    with st.expander("Production Order"):
        st.write(
            """
The Planned Order becomes a Production Order when the manufacturing process starts. The Production Order stores
the quantity to be produced and whether production is considered 'confirmed' — that confirmation may be automatic
or driven by the STATUS value of the original Sales Order.
"""
        )

    with st.expander("Confirmation"):
        st.write(
            """
Confirmation is the decision point: should production proceed to completion and shipment? This module applies the
project's **status rules** (see table below) to decide whether production is confirmed, whether delivery will be processed,
and whether billing is ready.
"""
        )

    with st.expander("Delivery"):
        st.write(
            """
Delivery represents physically shipping goods to the customer. Delivery status values include: Pending, In Transit, Delivered, etc.
A delivered item often triggers billing/invoicing.
"""
        )

    with st.expander("Billing"):
        st.write(
            """
Billing issues invoices tied to the Delivery. Invoices are labeled (e.g. INV-xxxx) and marked Paid or Unpaid depending on the outcome.
Billing status is also derived from the initial STATUS via the status rules.
"""
        )

    st.header("Status rules (how STATUS maps to outcomes)")
    st.markdown(
        "The project uses a status-to-outcomes mapping (a single source of truth). Below is the typical mapping used — edit the code if you want to change business rules."
    )

    # Present the mapping as a table for clarity
    status_data = {
        "STATUS": ["Shipped", "Disputed", "In Process", "On Hold", "Resolved", "Cancelled"],
        "Confirmed (Production)": [True, False, True, False, True, True],
        "Delivery Outcome": ["In Transit", "Not in Transit", "Not in Transit", "Not in Transit", "Delivered", "Not in Transit"],
        "Billing Outcome": ["Processed", "Not Processed", "Not Processed", "Not Processed", "Processed", "Not Processed"]
    }
    df_status = pd.DataFrame(status_data)
    st.table(df_status)

    st.info(
        """
If you want to change how a STATUS value is interpreted, edit the status mapping in the simulation module
(e.g., `capstone_utils/status_rules.py` or `capstone_with_input.py` depending on your project structure).
"""
    )

    st.header("Sample order walkthrough")
    st.markdown(
        """
Here is a compact example showing how one order moves through the system.
"""
    )

    sample = {
        "Input (Sales Order)": {
            "CUSTOMERNAME": "ACME Corp",
            "PRODUCTLINE": "Widget A",
            "QUANTITYORDERED": 10,
            "PRICEEACH": 15.00,
            "ORDERDATE": "2023-01-05",
            "STATUS": "Shipped"
        },
        "Output (dashboard_data.csv) - key fields": {
            "Order Date": "2023-01-05",
            "Customer": "ACME Corp",
            "Product": "Widget A",
            "Qty": 10,
            "Sales Order": "SO-xxxx",
            "Planned Order": "PL-xxxx",
            "Production Order": "PO-xxxx",
            "Confirmed": True,
            "Delivery": "In Transit",
            "Invoice": "INV-xxxx",
            "Billing Status": "Paid",
            "Amount": 150.00
        }
    }

    st.subheader("Example as JSON")
    st.json(sample)

    st.header("Visual process map")
    st.markdown("The diagram below is a simple flowchart of the MTO pipeline. You can export this diagram as a PDF if your environment supports Graphviz rendering.")

    flow_chart = generate_mto_flow_graph()
    with st.container(border=True, height = "content", width=900):
        st.graphviz_chart(flow_chart)
    offer_flowchart_download(flow_chart)

    st.header("FAQ / Troubleshooting")
    with st.expander("What if the dashboard shows no data?"):
        st.write(
            """
If `dashboard_data.csv` is missing or empty, go to **Data Processing** and run batch processing (upload a sample CSV)
or add a manual order. The dashboard reads `dashboard_data.csv` to render charts and tables.
"""
        )

    with st.expander("My CSV has different column names — what do I do?"):
        st.write(
            """
Either rename your CSV headers to match the expected batch input (`CUSTOMERNAME`, `PRODUCTLINE`, `QUANTITYORDERED`, `PRICEEACH`, `ORDERDATE`, `STATUS`), or update the batch loader code in the simulation module to map your column names into the internal names used by the pipeline.
"""
        )

    with st.expander("Where do I change the business rules?"):
        st.write(
            """
Edit the `status_rules` mapping in the simulation code (either `capstone_with_input.py` or `capstone_utils/status_rules.py` in the refactored version).
Changing that mapping will alter how orders are confirmed, shipped, and billed.
"""
        )

    st.markdown("---")
    st.caption("This overview is part of the MTO Simulation Dashboard. " \
    "It is used to orient new users and describe the project.")

