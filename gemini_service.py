
import os
import json
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = "AIzaSyBNzEQmDCyBy95APxnSMmQDnFPxoVTEytM"

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)

MANDATORY_FIELDS = [
    "Registration_No",
    "odometer_reading",
    "avg_kms_perday",
    "Make",
    "model",
    "year",
    "customer_name",
    "mobile_number",
    "variant",
    "Estimated_Delivery_Date"
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
If ANY of these fields are missing or empty, return empty string for them.
Backend will validate mandatory fields separately.

MANDATORY FIELDS:
- Registration_No
- odometer_reading
- avg_kms_perday
- Make
- model
- year
- variant
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

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        cleaned_text = re.sub(r"```json|```", "", response.text).strip()

        data = json.loads(cleaned_text)

        missing_fields = []

        for field in MANDATORY_FIELDS:
            value = data.get(field)
            if not value or str(value).strip() == "":
                missing_fields.append(field)
        if missing_fields:
            return {
                "error": True,
                "missing_fields": missing_fields
            }

        return data

    except json.JSONDecodeError:
        return {
            "error": True,
            "message": "Invalid JSON returned from AI"
        }

    except Exception as e:
        return {
            "error": True,
            "message": str(e)
        }
