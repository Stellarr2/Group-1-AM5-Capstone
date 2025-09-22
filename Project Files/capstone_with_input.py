import uuid
import csv
import pandas as pd

# Classes
class SalesOrder:
    def __init__(self, customer_name, product, qty, price, order_date, status):
        self.id = f"SO-{uuid.uuid4().hex[:8]}"
        self.customer = customer_name
        self.product = product
        self.qty = qty
        self.price = round(price, 2)
        self.order_date = order_date
        self.planned_order = None
        self.status = status

class PlannedOrder:
    def __init__(self, sales_order):
        self.id = f"PL-{uuid.uuid4().hex[:8]}"
        self.sales_order_id = sales_order.id
        self.product = sales_order.product
        self.qty = sales_order.qty
        self.status = sales_order.status
        self.production_order = None

class ProductionOrder:
    def __init__(self, planned_order):
        self.id = f"PO-{uuid.uuid4().hex[:8]}"
        self.planned_order_id = planned_order.id
        self.product = planned_order.product
        self.qty = planned_order.qty
        self.status = planned_order.status
        self.confirmed = False

class Delivery:
    def __init__(self, production_order, customer):
        self.id = f"DLV-{uuid.uuid4().hex[:8]}"
        self.production_order_id = production_order.id
        self.customer = customer
        self.status = "Pending"

class Billing:
    def __init__(self, delivery, amount):
        self.id = f"INV-{uuid.uuid4().hex[:8]}"
        self.delivery_id = delivery.id
        self.amount = round(amount, 2)
        self.status = "Unpaid"

# Status Dictionary
status_rules = {
    "shipped": {
        "confirmed": True,
        "delivery": "In Transit",
        "billing": "Processed"
    },
    "disputed": {
        "confirmed": False,
        "delivery": "Not in Transit",
        "billing": "Not Processed"
    },
    "in process": {
        "confirmed": True,
        "delivery": "Not in Transit",
        "billing": "Not Processed"
    },
    "on hold": {
        "confirmed": False,
        "delivery": "Not in Transit",
        "billing": "Not Processed"
    },
    "resolved": {
        "confirmed": True,
        "delivery": "Delivered",
        "billing": "Processed"
    },
    "cancelled": {
        "confirmed": True,
        "delivery": "Not in Transit",
        "billing": "Not Processed"
    }
}

# Process Functions
def LogAndPrint(logfile, message):
    print(message)
    logfile.write(message + "\n")

def CreateSalesOrder(customer, product, qty, price, order_date, status, logfile):
    LogAndPrint(logfile, f"\n[{order_date}] Sales Order created for {customer}: {qty} x {product} @ {price:.2f}")
    return SalesOrder(customer, product, qty, price, order_date, status)

def GeneratePlannedOrder(sales_order, logfile):
    LogAndPrint(logfile, f"Planned Order generated from Sales Order {sales_order.id}")
    planned = PlannedOrder(sales_order)
    sales_order.planned_order = planned
    return planned

def ConvertToProductionOrder(planned_order, logfile):
    LogAndPrint(logfile, f"Production Order created from Planned Order {planned_order.id}")
    prod_order = ProductionOrder(planned_order)
    planned_order.production_order = prod_order
    return prod_order

def ConfirmProduction(production_order, logfile):
    if production_order.status == "Shipped" or production_order.status == "Resolved":
        production_order.confirmed = True
        LogAndPrint(logfile, f"Production Order {production_order.id} confirmed for {production_order.qty} units")
    else: 
        production_order.confirmed = False
    return production_order

def DeliverGoods(production_order, customer, logfile):
    if not production_order.confirmed:
        LogAndPrint(logfile,f"Production not confirmed, cannot deliver.")
    delivery = Delivery(production_order, customer)
    delivery.status = "Delivered"
    LogAndPrint(logfile, f"Delivery {delivery.id} executed for {customer}")
    return delivery

def GenerateBilling(delivery, unit_price, qty, logfile):
    total = round(unit_price * qty, 2)
    bill = Billing(delivery, total)
    if delivery.status == "Delivered":
        bill.status = "Paid"
        LogAndPrint(logfile, f"Invoice {bill.id} generated for Delivery {delivery.id}, Amount: {total:.2f}")
    else: 
        bill.status = "Unpaid"
        LogAndPrint(logfile, "No bill")
    return bill

def ProcessOrder(customer, product, qty, price, order_date, status, logfile):

    # Normalize date
    if hasattr(order_date, "strftime"):  # handles datetime.date/datetime.datetime
        order_date = order_date.strftime("%Y-%m-%d")
    elif isinstance(order_date, str):
        try:
            # Try parsing common formats
            parsed = pd.to_datetime(order_date, errors="coerce")
            if pd.notna(parsed):
                order_date = parsed.strftime("%Y-%m-%d")
        except Exception:
            pass  # keep as raw string if parsing fails

    so = CreateSalesOrder(customer, product, qty, price, order_date, status, logfile)
    po = GeneratePlannedOrder(so, logfile)
    prod = ConvertToProductionOrder(po, logfile)

    # Apply status rules
    rules = status_rules.get(status.lower(), None)

    if rules:
        prod.confirmed = rules["confirmed"]
        delivery_status = rules["delivery"]
        billing_status = rules["billing"]
    else:
        # fallback if unknown status
        prod.confirmed = False
        delivery_status = "Unknown"
        billing_status = "Not Processed"

    # Delivery + Billing objects
    delivery = Delivery(prod, so.customer)
    delivery.status = delivery_status

    billing = Billing(delivery, so.price * so.qty)
    billing.status = "Paid" if billing_status == "Processed" else "Unpaid"

    # Log summary
    LogAndPrint(logfile, "\n--- Process Summary ---")
    LogAndPrint(logfile, f"Order Date: {so.order_date}")
    LogAndPrint(logfile, f"Sales Order ID: {so.id}")
    LogAndPrint(logfile, f"Production Order ID: {prod.id}, Confirmed: {prod.confirmed}")
    LogAndPrint(logfile, f"Delivery Status: {delivery.status}")
    LogAndPrint(logfile, f"Invoice: {billing.id}")
    LogAndPrint(logfile, f"Billing Status: {billing.status}, Amount: {billing.amount:.2f}")
    LogAndPrint(logfile, "-" * 50)

    # Collect results for dashboard
    order_results.append({
        "Order Date": so.order_date,
        "Customer": so.customer,
        "Product": so.product,
        "Qty": so.qty,
        "Sales Order": so.id,
        "Planned Order": po.id,
        "Production Order": prod.id,
        "Confirmed": prod.confirmed,
        "Delivery": delivery.status,
        "Invoice": billing.id,
        "Billing Status": billing.status,
        "Amount": billing.amount
    })

order_results = []   # will collect data for dashboard

def run_batch_mode(csv_file="sales_orders.csv"):
    """Process CSV batch and overwrite dashboard_data.csv"""
    global order_results
    order_results = []

    with open("mto_batch_flow_log.txt", "w", encoding="utf-8") as logfile:
        with open(csv_file, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ProcessOrder(
                    row["CUSTOMERNAME"],
                    row["PRODUCTLINE"],
                    int(row["QUANTITYORDERED"]),
                    float(row["PRICEEACH"]),
                    row["ORDERDATE"],
                    row["STATUS"],
                    logfile
                )

    # Always create/overwrite dashboard_data.csv
    if order_results:
        df = pd.DataFrame(order_results)
        df.to_csv("dashboard_data.csv", index=False)



def run_input_mode(customer, product, qty, price, order_date, status="Shipped"):
    """Process a single order and append to dashboard_data.csv"""
    global order_results
    order_results = []

    # Ensure order_date is a string in YYYY-MM-DD format
    if hasattr(order_date, "strftime"):  # if it's a date/datetime object
        order_date = order_date.strftime("%Y-%m-%d")

    with open("mto_input_flow_log.txt", "w", encoding="utf-8") as logfile:
        ProcessOrder(customer, product, qty, price, order_date, status, logfile)

    if order_results:
        try:
            df_existing = pd.read_csv("dashboard_data.csv")
            df_combined = pd.concat([df_existing, pd.DataFrame(order_results)], ignore_index=True)
        except FileNotFoundError:
            df_combined = pd.DataFrame(order_results)
        df_combined.to_csv("dashboard_data.csv", index=False)


    
