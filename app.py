from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Endpoints definition
@app.route("/api/v1/users")
def users_service():
    return jsonify({"status": "users service active"}), 200

@app.route("/api/v1/db-check")
def db_service():
    return jsonify({"error": "Database unreachable"}), 503

@app.route("/api/v1/payment-status")
def payment_service():
    return jsonify({"status": "payment API healthy"}), 200


# Services to monitor
SERVICES = {
    "Users Service": "/api/v1/users",
    "Database Service": "/api/v1/db-check",
    "Payment Service": "/api/v1/payment-status"
}


def check_services():
    """Check services internally using Flask test client (no HTTP needed)."""
    results = {}
    with app.test_client() as client:
        for name, route in SERVICES.items():
            try:
                response = client.get(route)
                results[name] = "UP" if response.status_code == 200 else "DOWN"
            except Exception:
                results[name] = "DOWN"
    return results


@app.route("/health")
def health():
    return jsonify(check_services())


@app.route("/")
def dashboard():
    return render_template("dashboard.html", results=check_services())


if __name__ == "__main__":
    app.run(debug=True)
