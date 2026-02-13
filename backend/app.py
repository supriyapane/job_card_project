from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json
import re

from google.generativeai import GenerativeModel, configure

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

configure(api_key=API_KEY)
model = GenerativeModel("gemini-2.5-flash")

MANDATORY_FIELDS = [
    "Registration_No",
    "odometer_reading",
    "avg_kms_perday",
    "Make",
    "model",
    "year",
    "customer_name",
    "mobile_number",
    "Estimated_Delivery_Date",
]

def process_text(user_text):
    try:
        prompt = f"""
You are an intelligent AI assistant for an automobile service center.

The user may speak in ANY language (voice or typed text).

Your tasks:
1. Detect the language of the user input.
2. Translate the input into English internally.
3. Understand the meaning clearly (even if spoken casually).
4. Extract job card details from the translated text.
5. Return ONLY valid JSON.
6. Do NOT include any explanation or extra text.
7. If a field is not found, return an empty string "".
8. The response must be strictly valid JSON (no markdown, no comments).

IMPORTANT:
The following fields are MANDATORY.
If ANY of these fields are missing or empty, return:
{{
  "error": "Missing mandatory fields"
}}

MANDATORY FIELDS:
- Registration_No
- odometer_reading
- avg_kms_perday
- Make
- model
- year
- customer_name
- mobile_number
- Estimated_Delivery_Date

Extract and return data in the following JSON format:
{{
  "Registration_No": "",
  "odometer_reading": "",
  "avg_kms_perday": "",
  "VIN": "",
  "Engine_No": "",
  "Make": "",
  "model": "",
  "year": "",
  "variant": "",
  "fuel_type": "",
  "vehicle_color": "",
  "service_type": "",
  "service_advisor_name": "",
  "Source": "",
  "Advisor": "",
  "Technician": "",
  "Estimated_Delivery_Date": "",
  "customer_name": "",
  "mobile_number": "",
  "Alternative_Contact_Number": "",
  "Email_ID": "",
  "Contact_Name_OR_Driver_Name": "",
  "Flat_House_No": "",
  "Colony_Street_Location": "",
  "Town_city": "",
  "state": "",
  "pincode": "",
  "address": ""
}}

User Input:
{user_text}
"""

        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json"
            }
        )

        cleaned_text = response.text.strip()
        cleaned_text = re.sub(r"```json|```", "", cleaned_text).strip()

        data = json.loads(cleaned_text)

        if "error" in data:
            return data

        for field in MANDATORY_FIELDS:
            if not data.get(field, "").strip():
                return {"error": f"Missing mandatory field: {field}"}

        return data

    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON from AI: {str(e)}"}
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}

@app.route("/process-text", methods=["POST"])
def process_text_endpoint():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "No text provided"}), 400

        result = process_text(data["text"])
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
