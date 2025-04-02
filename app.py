from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = "AIzaSyCfoApkAkVlpZktX-8ly3G5GRUQYOwIb10"

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)

def chat_with_bot(user_message):
    """Handles chatbot conversation using Google Gemini API"""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content([user_message])  # Ensure input is in a list
        return response.text if response and hasattr(response, 'text') else "Error: No response from AI"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    """API route for chatbot messages"""
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"reply": "Please enter a message."})

    bot_reply = chat_with_bot(user_message)
    return jsonify({"reply": bot_reply})

def get_exchange_rate():
    """Fetch real-time exchange rate from INR to USD"""
    url = "https://api.exchangerate-api.com/v4/latest/INR"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if request fails
        data = response.json()
        return data.get("rates", {}).get("USD", None)
    except Exception as e:
        print("Error fetching exchange rate:", e)
        return None

def calculate_old_tax(income):
    """Calculate tax based on old regime"""
    tax = 0
    if income > 1000000:
        tax += (income - 1000000) * 0.3
        income = 1000000
    if income > 500000:
        tax += (income - 500000) * 0.2
        income = 500000
    if income > 250000:
        tax += (income - 250000) * 0.05
    return tax

def calculate_new_tax(income):
    """Calculate tax based on new regime"""
    tax = 0
    if income > 1500000:
        tax += (income - 1500000) * 0.3
        income = 1500000
    if income > 1250000:
        tax += (income - 1250000) * 0.25
        income = 1250000
    if income > 1000000:
        tax += (income - 1000000) * 0.2
        income = 1000000
    if income > 750000:
        tax += (income - 750000) * 0.15
        income = 750000
    if income > 500000:
        tax += (income - 500000) * 0.1
        income = 500000
    if income > 250000:
        tax += (income - 250000) * 0.05
    return tax

@app.route("/", methods=["GET", "POST"])
def home():
    tax = None
    tax_in_usd = None
    if request.method == "POST":
        try:
            name = request.form["name"]
            income = float(request.form["income"])
            expenses = float(request.form["expenses"])
            tax_regime = request.form["tax_regime"]

            taxable_income = income - expenses

            if tax_regime == "old":
                tax = calculate_old_tax(taxable_income)
            elif tax_regime == "new":
                tax = calculate_new_tax(taxable_income)
            else:
                return jsonify({"error": "Invalid tax regime selected."})

            exchange_rate = get_exchange_rate()
            if exchange_rate:
                tax_in_usd = round(tax * exchange_rate, 2)

            return render_template("result.html", name=name, taxable_income=taxable_income, tax=tax, tax_in_usd=tax_in_usd)
        except ValueError:
            return jsonify({"error": "Invalid input. Please enter numeric values for income and expenses."})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
