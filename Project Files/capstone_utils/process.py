import pandas as pd
from .models import SalesOrder, PlannedOrder, ProductionOrder, Delivery, Billing
from .status_rules import status_rules

order_results = []  # shared global

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

def ProcessOrder(customer, product, qty, price, order_date, status, logfile):
    import pandas as pd

    # Normalize date
    if hasattr(order_date, "strftime"):
        order_date = order_date.strftime("%Y-%m-%d")
    elif isinstance(order_date, str):
        parsed = pd.to_datetime(order_date, errors="coerce")
        if pd.notna(parsed):
            order_date = parsed.strftime("%Y-%m-%d")

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
        prod.confirmed = False
        delivery_status = "Unknown"
        billing_status = "Not Processed"

    delivery = Delivery(prod, so.customer)
    delivery.status = delivery_status
    billing = Billing(delivery, so.price * so.qty)
    billing.status = "Paid" if billing_status == "Processed" else "Unpaid"

    # Log
    LogAndPrint(logfile, "\n--- Process Summary ---")
    LogAndPrint(logfile, f"Order Date: {so.order_date}")
    LogAndPrint(logfile, f"Sales Order ID: {so.id}")
    LogAndPrint(logfile, f"Status: {so.status}")
    LogAndPrint(logfile, f"Production Order ID: {prod.id}, Confirmed: {prod.confirmed}")
    LogAndPrint(logfile, f"Delivery Status: {delivery.status}")
    LogAndPrint(logfile, f"Invoice: {billing.id}")
    LogAndPrint(logfile, f"Billing Status: {billing.status}, Amount: {billing.amount:.2f}")
    LogAndPrint(logfile, "-" * 50)

    # ✅ Return result instead of appending to a global
    return {
        "Order Date": so.order_date,
        "Customer": so.customer,
        "Product": so.product,
        "Qty": so.qty,
        "Sales Order": so.id,
        "Planned Order": po.id,
        "Production Order": prod.id,
        "Confirmed": prod.confirmed,
        "Status": so.status,
        "Delivery": delivery.status,
        "Invoice": billing.id,
        "Billing Status": billing.status,
        "Amount": billing.amount
    }