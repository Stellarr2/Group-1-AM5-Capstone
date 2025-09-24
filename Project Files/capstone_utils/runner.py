import csv
import pandas as pd
from .process import ProcessOrder
from .pdf_export import export_batch_pdf, export_single_pdf

def run_batch_mode(csv_file="sales_orders.csv"):
    results = []

    with open("mto_batch_flow_log.txt", "w", encoding="utf-8") as logfile:
        with open(csv_file, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result = ProcessOrder(
                    row["CUSTOMERNAME"],
                    row["PRODUCTLINE"],
                    int(row["QUANTITYORDERED"]),
                    float(row["PRICEEACH"]),
                    row["ORDERDATE"],
                    row["STATUS"],
                    logfile
                )
                results.append(result)

    if results:
        df = pd.DataFrame(results)
        df.to_csv("dashboard_data.csv", index=False)
        export_batch_pdf(df, "batch_report.pdf")

def run_input_mode(customer, product, qty, price, order_date, status="Shipped"):
    results = []

    with open("mto_input_flow_log.txt", "w", encoding="utf-8") as logfile:
        result = ProcessOrder(customer, product, qty, price, order_date, status, logfile)
        results.append(result)

    if results:
        try:
            df_existing = pd.read_csv("dashboard_data.csv")
            df_combined = pd.concat([df_existing, pd.DataFrame(results)], ignore_index=True)
        except FileNotFoundError:
            df_combined = pd.DataFrame(results)
        df_combined.to_csv("dashboard_data.csv", index=False)
        export_single_pdf(results[0], "input_report.pdf")
