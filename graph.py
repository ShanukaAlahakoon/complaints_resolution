from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents import (
    input_agent,
    customer_history_agent,
    issue_classifier_agent,
    priority_agent,
    solution_agent,
    ticket_agent,
    final_response_agent
)

# ─────────────────────────────────────────
# Define the State Structure
# ─────────────────────────────────────────
class ComplaintState(TypedDict, total=False):
    complaint: str
    customer_id: str
    customer: dict
    issue_type: str
    priority: str
    solution: str
    ticket: dict
    final_message: str


# ─────────────────────────────────────────
# Build the Graph
# ─────────────────────────────────────────
def build_graph():
    graph = StateGraph(ComplaintState)

    # Add all agents as nodes
    graph.add_node("input_agent",            input_agent)
    graph.add_node("customer_history_agent", customer_history_agent)
    graph.add_node("issue_classifier_agent", issue_classifier_agent)
    graph.add_node("priority_agent",         priority_agent)
    graph.add_node("solution_agent",         solution_agent)
    graph.add_node("ticket_agent",           ticket_agent)
    graph.add_node("final_response_agent",   final_response_agent)

    # Connect agents in order
    graph.set_entry_point("input_agent")
    graph.add_edge("input_agent",            "customer_history_agent")
    graph.add_edge("customer_history_agent", "issue_classifier_agent")
    graph.add_edge("issue_classifier_agent", "priority_agent")
    graph.add_edge("priority_agent",         "solution_agent")
    graph.add_edge("solution_agent",         "ticket_agent")
    graph.add_edge("ticket_agent",           "final_response_agent")
    graph.add_edge("final_response_agent",   END)

    return graph.compile()