import json
import os
from pathlib import Path

CUSTOMER_FILE = Path(__file__).parent / "data" / "customers.json"

def load_customers() -> dict:
    if CUSTOMER_FILE.exists():
        with open(CUSTOMER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_customers(customers: dict):
    with open(CUSTOMER_FILE, "w") as f:
        json.dump(customers, f, indent=4)

def get_customer(customer_id: str) -> dict:
    customers = load_customers()
    return customers.get(customer_id.upper(), None)

def update_past_complaints(customer_id: str, new_complaint: str):
    customers = load_customers()
    cid = customer_id.upper()
    if cid in customers:
        if new_complaint not in customers[cid]["past_complaints"]:
            customers[cid]["past_complaints"].append(new_complaint)
            save_customers(customers)
            print(f"  Past complaints updated for {cid} ✅")
    else:
        print(f"  Customer {cid} not found.")

def get_all_customers() -> dict:
    return load_customers()