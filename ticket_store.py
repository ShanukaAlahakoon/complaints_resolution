import json
import os
from datetime import datetime
from pathlib import Path

TICKET_FILE = Path(__file__).parent / "data" / "tickets.json"


def _read_tickets() -> list:
    if not TICKET_FILE.exists():
        return []

    try:
        with TICKET_FILE.open("r", encoding="utf-8") as file_handle:
            tickets = json.load(file_handle)
    except (json.JSONDecodeError, OSError, ValueError):
        return []

    return tickets if isinstance(tickets, list) else []

def save_ticket(ticket: dict):
    # Add timestamp
    ticket["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Load existing tickets
    tickets = _read_tickets()

    # Append new ticket
    tickets.append(ticket)

    # Save back to file
    with TICKET_FILE.open("w", encoding="utf-8") as file_handle:
        json.dump(tickets, file_handle, indent=4)

    print(f"  Ticket saved to {TICKET_FILE} ✅")


def load_all_tickets():
    return _read_tickets()