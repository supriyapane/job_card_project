from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_service import process_text

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Server running successfully"

@app.route("/create-job", methods=["POST"])
def create_job():
    data = request.get_json()
    text = data.get("text")
    result = process_text(text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)