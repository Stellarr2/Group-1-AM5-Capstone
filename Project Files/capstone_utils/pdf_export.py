import pandas as pd
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def export_batch_pdf(dataframe, filename="batch_report.pdf"):
    """Generate a PDF report with summary metrics + slim table for batch mode."""
    doc = SimpleDocTemplate(filename, pagesize= landscape(LETTER))
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("📑 MTO Batch Report", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # --- Metrics ---
    total_orders = len(dataframe)
    total_revenue = dataframe["Amount"].sum()
    paid_count = (dataframe["Billing Status"] == "Paid").sum()
    unpaid_count = (dataframe["Billing Status"] == "Unpaid").sum()

    metrics = [
        f"Total Orders: {total_orders}",
        f"Total Revenue: {total_revenue:,.2f}",
        f"Paid Invoices: {paid_count}",
        f"Unpaid Invoices: {unpaid_count}"
    ]
    for m in metrics:
        elements.append(Paragraph(m, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # --- Table ---
    # Wrap all cell text in Paragraph (so it auto-wraps within narrow columns)
    table_data = [
        [Paragraph(str(col), styles["BodyText"]) for col in dataframe.columns]
    ] + [
        [Paragraph(str(val), styles["BodyText"]) for val in row]
        for row in dataframe.values.tolist()
    ]

    # Narrower columns, text will wrap
    col_widths = [60] * len(dataframe.columns)

    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 6),   # smaller font
    ("TOPPADDING", (0, 0), (-1, -1), 1),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ("WORDWRAP", (0, 0), (-1, -1), "CJK"),  # allows breaking instead of cut-off
    ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
    ]))


    elements.append(table)
    doc.build(elements)
    print(f"✅ Slim Batch PDF generated: {filename}")

def export_single_pdf(order_dict, filename="input_report.pdf"):
    """Generate a PDF report for just one single order."""
    doc = SimpleDocTemplate(filename, pagesize=LETTER)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("📑 MTO Input Report (Single Order)", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # --- Key Order Info ---
    elements.append(Paragraph(f"Customer: {order_dict['Customer']}", styles["Normal"]))
    elements.append(Paragraph(f"Product: {order_dict['Product']}", styles["Normal"]))
    elements.append(Paragraph(f"Quantity: {order_dict['Qty']}", styles["Normal"]))
    elements.append(Paragraph(f"Amount: {order_dict['Amount']:.2f}", styles["Normal"]))
    elements.append(Paragraph(f"Status: {order_dict['Status']}", styles["Normal"]))
    elements.append(Paragraph(f"Billing Status: {order_dict['Billing Status']}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # --- Small Table (IDs) ---
    table_data = [
        ["Sales Order", order_dict["Sales Order"]],
        ["Planned Order", order_dict["Planned Order"]],
        ["Production Order", order_dict["Production Order"]],
        ["Invoice", order_dict["Invoice"]],
    ]

    table = Table(table_data, colWidths=[120, 200])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)
    print(f"✅ Single Order PDF generated: {filename}")
