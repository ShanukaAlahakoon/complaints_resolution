from flask import Flask, render_template, request, jsonify
from graph import build_graph
from ticket_store import load_all_tickets
from mock_data import get_all_customers

app = Flask(__name__)
graph = build_graph()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    complaint = data.get("complaint", "")
    customer_id = data.get("customer_id", "")

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

    return jsonify({
        "ticket_id":    result["ticket"]["ticket_id"],
        "customer":     result["customer"]["name"],
        "package":      result["customer"]["package"],
        "location":     result["customer"]["location"],
        "issue_type":   result["issue_type"],
        "priority":     result["priority"],
        "solution":     result["solution"],
        "final_message": result["final_message"],
        "status":       result["ticket"]["status"]
    })

@app.route("/tickets")
def tickets():
    all_tickets = load_all_tickets()
    return jsonify(all_tickets)

@app.route("/api/customers")
def api_customers():
    customers = get_all_customers()
    return jsonify(customers)



if __name__ == "__main__":
    app.run(debug=True)
