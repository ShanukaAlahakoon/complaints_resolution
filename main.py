from graph import build_graph

# ─────────────────────────────────────────
# Build the multi-agent graph
# ─────────────────────────────────────────
graph = build_graph()

# ─────────────────────────────────────────
# Test Complaints
# ─────────────────────────────────────────
test_cases = [
    {
        "complaint": "My internet is very slow since yesterday. I cannot work from home.",
        "customer_id": "C001"
    },
    {
        "complaint": "I was charged twice for this month. Please check my bill.",
        "customer_id": "C002"
    },
    {
        "complaint": "My IPTV is not showing any channels since morning.",
        "customer_id": "C004"
    }
]

# ─────────────────────────────────────────
# Run the system
# ─────────────────────────────────────────
def run_complaint(complaint: str, customer_id: str):
    print("\n" + "="*60)
    print("   SLT TELECOM - COMPLAINT RESOLUTION SYSTEM")
    print("="*60)

    initial_state = {
        "complaint": complaint,
        "customer_id": customer_id,
        "customer": {},
        "issue_type": "",
        "priority": "",
        "solution": "",
        "ticket": {},
        "final_message": ""
    }

    result = graph.invoke(initial_state)

    print("\n" + "─"*60)
    print("   FINAL TICKET SUMMARY")
    print("─"*60)
    print(f"  Ticket ID    : {result['ticket']['ticket_id']}")
    print(f"  Customer     : {result['customer']['name']}")
    print(f"  Package      : {result['customer']['package']}")
    print(f"  Location     : {result['customer']['location']}")
    print(f"  Issue Type   : {result['issue_type']}")
    print(f"  Priority     : {result['priority']}")
    print(f"  Status       : {result['ticket']['status']}")
    print("─"*60)
    print(f"\n  MESSAGE TO CUSTOMER:\n")
    print(f"  {result['final_message']}")
    print("\n" + "="*60)


# ─────────────────────────────────────────
# Run all test cases
# ─────────────────────────────────────────
if __name__ == "__main__":
    for case in test_cases:
        run_complaint(case["complaint"], case["customer_id"])
        print("\n\nPress Enter to run next complaint...")
        input()