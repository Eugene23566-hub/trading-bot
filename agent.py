from flask import Flask, request, jsonify
import os
import datetime

app = Flask(__name__)
AUTH_KEY = os.getenv("AUTH_KEY", "08111990")

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "running", "time": datetime.datetime.utcnow().isoformat()})

@app.route("/log", methods=["POST"])
def log():
    if request.headers.get("Authorization") != AUTH_KEY:
        return jsonify({"error": "unauthorized"}), 403
    data = request.json
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}: {data}\n")
    return jsonify({"received": True})

@app.route("/edit", methods=["POST"])
def edit():
    if request.headers.get("Authorization") != AUTH_KEY:
        return jsonify({"error": "unauthorized"}), 403
    content = request.json
    file = content.get("file")
    code = content.get("code")
    if not file or not code:
        return jsonify({"error": "invalid input"}), 400
    try:
        with open(file, "w") as f:
            f.write(code)
        return jsonify({"status": "updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
