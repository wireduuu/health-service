from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# example services to monitor
SERVICES = {
    "Github": "https://www.github.com",
    "My Portfolio Website": "https://dsw-portfolio.vercel.app",
    "NonExistent": "http://example.nonexistent"  # simulate a failing service
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

@app.route("/health")
def health():
    """Return JSON metrics for services."""
    return jsonify(check_services())

@app.route("/")
def dashboard():
    """Render UI for humans."""
    return render_template("dashboard.html", results=check_services())

if __name__ == "__main__":
    app.run(debug=True)