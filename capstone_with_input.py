import uuid
import csv
import pandas as pd
import sys

# --- Classes ---
class SalesOrder:
    def __init__(self, customer_name, product, qty, price, order_date):
        self.id = f"SO-{uuid.uuid4().hex[:8]}"
        self.customer = customer_name
        self.product = product
        self.qty = qty
        self.price = round(price, 2)
        self.order_date = order_date
        self.planned_order = None

class PlannedOrder:
    def __init__(self, sales_order):
        self.id = f"PL-{uuid.uuid4().hex[:8]}"
        self.sales_order_id = sales_order.id
        self.product = sales_order.product
        self.qty = sales_order.qty
        self.production_order = None

class ProductionOrder:
    def __init__(self, planned_order):
        self.id = f"PO-{uuid.uuid4().hex[:8]}"
        self.planned_order_id = planned_order.id
        self.product = planned_order.product
        self.qty = planned_order.qty
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

# --- Process Functions ---
def LogAndPrint(logfile, message):
    print(message)
    logfile.write(message + "\n")

def CreateSalesOrder(customer, product, qty, price, order_date, logfile):
    LogAndPrint(logfile, f"\n[{order_date}] Sales Order created for {customer}: {qty} x {product} @ {price:.2f}")
    return SalesOrder(customer, product, qty, price, order_date)

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
    production_order.confirmed = True
    LogAndPrint(logfile, f"Production Order {production_order.id} confirmed for {production_order.qty} units")
    return production_order

def DeliverGoods(production_order, customer, logfile):
    if not production_order.confirmed:
        raise Exception("Production not confirmed, cannot deliver.")
    delivery = Delivery(production_order, customer)
    delivery.status = "Delivered"
    LogAndPrint(logfile, f"Delivery {delivery.id} executed for {customer}")
    return delivery

def GenerateBilling(delivery, unit_price, qty, logfile):
    total = round(unit_price * qty, 2)
    bill = Billing(delivery, total)
    bill.status = "Paid"
    LogAndPrint(logfile, f"Invoice {bill.id} generated for Delivery {delivery.id}, Amount: {total:.2f}")
    return bill

def ProcessOrder(customer, product, qty, price, order_date, logfile):
    so = CreateSalesOrder(customer, product, qty, price, order_date, logfile)
    po = GeneratePlannedOrder(so, logfile)
    prod = ConvertToProductionOrder(po, logfile)
    ConfirmProduction(prod, logfile)
    delivery = DeliverGoods(prod, so.customer, logfile)
    billing = GenerateBilling(delivery, so.price, so.qty, logfile)

    # Summary block
    LogAndPrint(logfile, "\n--- Process Summary ---")
    LogAndPrint(logfile, f"Order Date: {so.order_date}")
    LogAndPrint(logfile, f"Sales Order ID: {so.id}")
    LogAndPrint(logfile, f"Planned Order ID: {po.id}")
    LogAndPrint(logfile, f"Production Order ID: {prod.id}, Confirmed: {prod.confirmed}")
    LogAndPrint(logfile, f"Sales Order to Production Order Linkage: {so.id} -> {po.id} -> {prod.id}")
    LogAndPrint(logfile, f"Delivery Status: {delivery.status}")
    LogAndPrint(logfile, f"Invoice: {billing.id}")
    LogAndPrint(logfile, f"Billing Status: {billing.status}, Amount: {billing.amount:.2f}")
    LogAndPrint(logfile, "-" * 50)

    # ⬅️ Append results for dashboard
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

def VerifyMember(logfile):
    member_name = input("Enter your name for verification: ")
    LogAndPrint(logfile, f"Code run verified by: {member_name}")

order_results = []   # will collect data for dashboard

if __name__ == "__main__":

    mode = input("Choose mode: (1) CSV Batch or (2) Manual Input: ")

    if mode == "1":
        with open("mto_batch_flow_log.txt", "w", encoding="utf-8") as logfile:
            VerifyMember(logfile)
            with open("sales_orders.csv", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    ProcessOrder(
                        row["CUSTOMERNAME"],
                        row["PRODUCTLINE"],
                        int(row["QUANTITYORDERED"]),
                        float(row["PRICEEACH"]),
                        row["ORDERDATE"],
                        logfile
                    )

    elif mode == "2":
        with open("mto_input_flow_log.txt", "w", encoding="utf-8") as logfile:
            VerifyMember(logfile)
            customer = input("Enter Customer Name: ")
            product = input("Enter Product: ")
            qty = int(input("Enter Quantity: "))
            price = float(input("Enter Price per unit: "))
            order_date = input("Enter Order Date (YYYY-MM-DD): ")

            ProcessOrder(customer, product, qty, price, order_date, logfile)

    else:
        print("Invalid choice. Exiting.")
        sys.exit(0)

    # --- Save results for dashboard ---
    if order_results:
        df = pd.DataFrame(order_results)
        df.to_csv("dashboard_data.csv", index=False)

        # --- Launch dashboard automatically ---
        
if order_results:
    df = pd.DataFrame(order_results)
    df.to_csv("dashboard_data.csv", index=False)

    print("\n enter `streamlit run dashboard.py` to launch dashboard!")
    
