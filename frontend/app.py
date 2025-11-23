import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
API_BASE = os.getenv("API_BASE", "http://tictactoe-backend:5000")

@app.route("/")
def index():
    # just serve the static HTML/JS page
    return render_template("index.html")

# proxy endpoints – frontend talks to backend inside cluster
@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    r = requests.post(f"{API_BASE}/api/move", json=data)
    return jsonify(r.json())

@app.route("/reset")
def reset():
    r = requests.get(f"{API_BASE}/api/reset")
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
