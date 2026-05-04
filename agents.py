from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from mock_data import get_customer
import os

load_dotenv()

# Initialize Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# ─────────────────────────────────────────
# AGENT 1: Input Agent
# ─────────────────────────────────────────
def input_agent(state: dict) -> dict:
    print("\n[Agent 1] Input Agent: Reading complaint...")
    complaint = state["complaint"]
    customer_id = state["customer_id"]
    print(f"  Complaint : {complaint}")
    print(f"  Customer ID: {customer_id}")
    return state


# ─────────────────────────────────────────
# AGENT 2: Customer History Agent
# ─────────────────────────────────────────
def customer_history_agent(state: dict) -> dict:
    print("\n[Agent 2] Customer History Agent: Fetching customer data...")
    customer_id = state["customer_id"]
    customer = get_customer(customer_id)

    if customer:
        print(f"  Name     : {customer['name']}")
        print(f"  Package  : {customer['package']}")
        print(f"  Location : {customer['location']}")
        print(f"  Past Complaints: {customer['past_complaints']}")
        state["customer"] = customer
    else:
        print("  Customer not found. Using unknown profile.")
        state["customer"] = {
            "name": "Unknown",
            "package": "Unknown",
            "location": "Unknown",
            "past_complaints": []
        }
    return state


# ─────────────────────────────────────────
# AGENT 3: Issue Classifier Agent
# ─────────────────────────────────────────
def issue_classifier_agent(state: dict) -> dict:
    print("\n[Agent 3] Issue Classifier Agent: Identifying issue type...")
    complaint = state["complaint"]

    prompt = f"""
    You are a telecom support classifier for SLT (Sri Lanka Telecom).
    Classify the following customer complaint into ONE of these categories:
    - Internet Speed
    - Router Problem
    - Billing Issue
    - Fiber Connection
    - IPTV Problem
    - Network Outage
    - Other

    Complaint: "{complaint}"

    Reply with ONLY the category name. Nothing else.
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    issue_type = response.content.strip()
    print(f"  Issue Type: {issue_type}")
    state["issue_type"] = issue_type
    return state


# ─────────────────────────────────────────
# AGENT 4: Priority Agent
# ─────────────────────────────────────────
def priority_agent(state: dict) -> dict:
    print("\n[Agent 4] Priority Agent: Assigning priority level...")
    complaint = state["complaint"]
    customer = state["customer"]
    issue_type = state["issue_type"]

    prompt = f"""
    You are a priority assignment agent for SLT Telecom support.
    Based on the details below, assign a priority level: Low, Medium, or High.

    Customer Package : {customer['package']}
    Issue Type       : {issue_type}
    Complaint        : "{complaint}"
    Past Complaints  : {customer['past_complaints']}

    Rules:
    - High   : Fiber issues, repeated complaints, complete outage
    - Medium : Slow internet, IPTV issues, single billing issue
    - Low    : General queries, minor issues

    Reply with ONLY one word: Low, Medium, or High.
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    priority = response.content.strip()
    print(f"  Priority: {priority}")
    state["priority"] = priority
    return state


# ─────────────────────────────────────────
# AGENT 5: Solution Agent
# ─────────────────────────────────────────
def solution_agent(state: dict) -> dict:
    print("\n[Agent 5] Solution Agent: Generating solution...")
    complaint = state["complaint"]
    customer = state["customer"]
    issue_type = state["issue_type"]
    priority = state["priority"]

    prompt = f"""
    You are a technical support agent for SLT Sri Lanka Telecom.
    Provide a short, clear solution for this customer complaint.

    Customer Name    : {customer['name']}
    Package          : {customer['package']}
    Location         : {customer['location']}
    Issue Type       : {issue_type}
    Priority         : {priority}
    Complaint        : "{complaint}"
    Past Complaints  : {customer['past_complaints']}

    Give 2-3 practical steps to resolve this issue.
    Keep it professional and simple.
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    solution = response.content.strip()
    print(f"  Solution: {solution}")
    state["solution"] = solution
    return state


# ─────────────────────────────────────────
# AGENT 6: Ticket Agent
# ─────────────────────────────────────────
def ticket_agent(state: dict) -> dict:
    print("\n[Agent 6] Ticket Agent: Creating support ticket...")
    import random
    from ticket_store import save_ticket
    from mock_data import update_past_complaints

    ticket_id = f"TKT-{random.randint(10000, 99999)}"

    ticket = {
        "ticket_id": ticket_id,
        "customer_id": state["customer_id"],
        "customer_name": state["customer"]["name"],
        "issue_type": state["issue_type"],
        "priority": state["priority"],
        "complaint": state["complaint"],
        "solution": state["solution"],
        "status": "Open"
    }

    print(f"  Ticket ID : {ticket_id}")
    print(f"  Status    : Open")

    # Save ticket to JSON
    save_ticket(ticket)

    # ✅ Update customer's past complaints automatically
    update_past_complaints(
        state["customer_id"],
        state["issue_type"]
    )

    state["ticket"] = ticket
    return state

# ─────────────────────────────────────────
# AGENT 7: Final Response Agent
# ─────────────────────────────────────────
def final_response_agent(state: dict) -> dict:
    print("\n[Agent 7] Final Response Agent: Preparing final message...")
    ticket = state["ticket"]
    customer = state["customer"]
    solution = state["solution"]

    prompt = f"""
    You are a customer service agent for SLT Sri Lanka Telecom.
    Write a short, polite final response message to the customer.

    Customer Name : {customer['name']}
    Ticket ID     : {ticket['ticket_id']}
    Issue Type    : {ticket['issue_type']}
    Priority      : {ticket['priority']}
    Solution      : {solution}

    The message should:
    - Thank the customer
    - Mention the ticket ID
    - Briefly explain what will be done
    - Be professional and friendly
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    final_message = response.content.strip()
    print(f"\n  Final Message:\n{final_message}")
    state["final_message"] = final_message
    return state