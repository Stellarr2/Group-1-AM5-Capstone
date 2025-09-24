import graphviz
import streamlit as st

def generate_mto_flow_graph():
    """Return a Graphviz Digraph object for the MTO process flow."""
    dot = graphviz.Digraph(comment="MTO Process Flow")
    
    # Nodes
    dot.node("START", "VA01:\nCustomer Creates Sales Order", shape = "oval", style = "filled", color="#404246", fontcolor = "white")
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

def offer_flowchart_download(flow_chart, filename="mto_process_flow.pdf"):
    """
    Try to render a Graphviz Digraph to PDF bytes and show a download button.
    If Graphviz system binary is missing, show a note instead of breaking.
    
    Parameters
    ----------
    flow_chart : graphviz.Digraph
        The Graphviz diagram object to export.
    filename : str, optional
        Filename to suggest when downloading the PDF (default 'mto_process_flow.pdf').
    """
    try:
        pdf_bytes = flow_chart.pipe(format="pdf")
        if pdf_bytes:
            st.download_button(
                label="⬇️ Download process flow (PDF)",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf"
            )
    except Exception:
        st.info(
            "⚠️ PDF export requires the Graphviz system binary. "
            "If the button is missing, install Graphviz locally "
            "or generate the PDF on a machine with Graphviz installed."
        )