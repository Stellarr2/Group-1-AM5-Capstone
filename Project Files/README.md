Make-to-Order (MTO) Simulation Dashboard

Project summary

This project simulates a Make-to-Order production flow and provides a Streamlit dashboard for inspection. The simulation takes orders, steps them through planning/production/delivery/billing, and writes a dashboard\_data.csv file that the dashboard reads and visualizes.

Main idea:

Sales Order → Planned Order → Production Order → Delivery → Billing

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Quick facts (what’s in the zip)

•	capstone\_with\_input.py — simulation engine; functions to process CSV batches and single orders.

•	dashboard.py — Streamlit app entry point; reads dashboard\_data.csv and shows pages.

•	styles.css — visual styling used by the dashboard.

•	pages/

o	data\_processing.py — CSV upload, manual entry, Graphviz process flow (PDF export).

o	charts.py — KPI and chart page (calls utils.charts and utils.kpis).

o	tables.py — table view page (calls utils.tables).

•	utils/

o	loader.py — load\_css() and load\_dashboard\_df() helpers.

o	charts.py — Altair chart constructors (e.g., billing\_status\_chart, revenue\_by\_product\_chart, delivery\_status\_chart, revenue\_over\_time\_chart, orders\_per\_customer\_chart, confirmed\_chart).

o	kpis.py — show\_kpis(df) to render the top metric tiles.

o	tables.py — active\_orders\_table(df), billing\_table(df), full\_history\_table(df).

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Requirements \& installation

Python packages

Install the Python packages used by the project:

pip install streamlit pandas altair graphviz reportlab

System requirement for Graphviz PDF rendering

If you plan to export the Graphviz diagram to PDF, install the Graphviz system binary on your OS:

•	Ubuntu / Debian:

sudo apt-get update

sudo apt-get install graphviz

•	macOS (Homebrew):

brew install graphviz

•	Windows: install Graphviz from the official installer or via Chocolatey:

choco install graphviz

Note: the graphviz Python package is only a wrapper; the system binary is needed to render(...) to PDF.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

How to run

Recommended (UI-driven)

1\.	Start the dashboard:

streamlit run dashboard.py

2\.	In the dashboard sidebar choose Data Processing to:

o	Upload a CSV and run batch processing (overwrite or append).

o	Add a single order via the manual input form (requires entering the transaction code as shown on the page).

o	View and export the Graphviz process flow PDF.

Programmatic alternatives

If you prefer not to use the UI, you can call functions from capstone\_with\_input.py in Python:

from capstone\_with\_input import run\_batch\_mode, run\_input\_mode



\# process the default CSV (if present)

run\_batch\_mode("sales\_orders.csv")



\# process a single order

run\_input\_mode("Customer Name", "Product A", 5, 10.0, "2023-01-01", status="Shipped")

Note: The dashboard reads dashboard\_data.csv to build its charts and tables.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Expected input CSV format (batch mode)

When doing batch processing, the code expects the CSV rows to have these column names used in capstone\_with\_input.py:

•	CUSTOMERNAME

•	PRODUCTLINE

•	QUANTITYORDERED (integer)

•	PRICEEACH (float)

•	ORDERDATE (string date)

•	STATUS (string; e.g., Shipped, Disputed, Resolved, etc.)

Example CSV row (comma-separated):

CUSTOMERNAME,PRODUCTLINE,QUANTITYORDERED,PRICEEACH,ORDERDATE,STATUS

ACME Corp,Widget A,10,15.00,2023-01-05,Shipped

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Output / dashboard\_data.csv (what the dashboard reads)

Each processed order produces one row in dashboard\_data.csv with fields like:

•	Order Date

•	Customer

•	Product

•	Qty

•	Sales Order (SO-xxxx)

•	Planned Order (PL-xxxx)

•	Production Order (PO-xxxx)

•	Confirmed (boolean)

•	Delivery (string status)

•	Invoice (INV-xxxx)

•	Billing Status (Paid/Unpaid/Processed/Not Processed)

•	Amount (numeric)

The Streamlit pages rely on these columns for KPIs, charts, and tables.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Pages \& UX (what each dashboard page does)

Data Processing page

•	Upload CSV for batch processing (two modes: overwrite or append).

•	Manual order input form (transaction code verification on the page).

•	Generates and displays a Graphviz process flow diagram.

•	Can export the flow diagram as a PDF (requires Graphviz system binary).

Charts page

•	Shows KPI tiles (total orders, confirmed orders, delivered orders, total revenue).

•	Renders multiple Altair charts (billing status, revenue by product, delivery status, revenue over time, orders per customer, confirmed vs unconfirmed).

•	Charts are built by functions in utils/charts.py; KPI tiles by utils/kpis.show\_kpis.

Tables page

•	Shows Active Production Orders (filtered by Confirmed == True when those columns are present).

•	Shows Billing Overview (Invoice, Customer, Amount, Billing Status).

•	Shows full order history as a dataframe.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Notes \& troubleshooting

•	Missing or empty dashboard\_data.csv: the dashboard will still run but show no data. Use the Data Processing page to upload a CSV and process it.

•	Column mismatches: if your CSV uses different header names, map them to the expected headers or edit the batch code accordingly.

•	Graphviz errors exporting to PDF: ensure the Graphviz system package is installed and available on PATH.

•	Large CSVs: the app is not optimized for very large datasets; for heavy loads consider using a database backend.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Where the business logic lives

•	The status-to-outcome rules (how STATUS values map to production confirmation, delivery state, and billing state) are defined inside capstone\_with\_input.py. To change business rules, edit that dictionary / logic in the simulation engine.

