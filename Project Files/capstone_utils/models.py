import uuid

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
