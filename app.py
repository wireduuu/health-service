from flask import Flask, jsonify, render_template
import requests, random

app = Flask(__name__)

# ----------------------------
# Define your own endpoints
# ----------------------------

@app.route("/api/v1/users")
def users_service():
    """Simulated Users service (application-level)."""
    if random.choice([True, False, False]):  # ~33% chance of failure
        return jsonify({"error": "Application error occurred"}), 500
    return jsonify({"status": "users service active"}), 200


@app.route("/api/v1/db-check")
def db_service():
    """Simulated Database connectivity check."""
    if random.choice([True, False]):  # 50% chance of DB outage
        return jsonify({"error": "Database unreachable"}), 503
    return jsonify({"status": "database reachable"}), 200


@app.route("/api/v1/payment-status")
def payment_service():
    """Simulated Payment API check (external dependency)."""
    if random.choice([True, False, False]):  # ~33% chance external API down
        return jsonify({"error": "Payment provider unavailable"}), 502
    return jsonify({"status": "payment API healthy"}), 200


# ----------------------------
# Services to monitor
# ----------------------------
SERVICES = {
    "Users Service": "http://localhost:5000/api/v1/users",
    "Database Service": "http://localhost:5000/api/v1/db-check",
    "Payment Service": "http://localhost:5000/api/v1/payment-status"
}

def check_services():
    """Helper function to check all services."""
    results = {}
    for name, url in SERVICES.items():
        try:
            response = requests.get(url, timeout=3)
            results[name] = "UP" if response.status_code == 200 else "DOWN"
        except Exception:
            results[name] = "DOWN"
    return results


# ----------------------------
# Health endpoint + Dashboard
# ----------------------------
@app.route("/health")
def health():
    """Return JSON metrics for services."""
    return jsonify(check_services())


@app.route("/")
def dashboard():
    """Render UI for humans (using template)."""
    return render_template("dashboard.html", results=check_services())


if __name__ == "__main__":
    app.run(debug=True)
