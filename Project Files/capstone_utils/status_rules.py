# Status-Outcome mapping using a dictionary
status_rules = {
    "shipped": {"confirmed": True, "delivery": "In Transit", "billing": "Processed"},
    "disputed": {"confirmed": True, "delivery": "Not in Transit", "billing": "Not Processed"},
    "in process": {"confirmed": True, "delivery": "Not in Transit", "billing": "Not Processed"},
    "on hold": {"confirmed": False, "delivery": "Not in Transit", "billing": "Not Processed"},
    "resolved": {"confirmed": True, "delivery": "Delivered", "billing": "Processed"},
    "cancelled": {"confirmed": True, "delivery": "Not in Transit", "billing": "Not Processed"},
}
