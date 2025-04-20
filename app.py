from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY ="AIzaSyCfoApkAkVlpZktX-8ly3G5GRUQYOwIb10"

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

dish_data = {
    "pasta": {
        "description": "Pasta is an Italian dish made from wheat and shaped into various forms.",
        "ingredients": ["Wheat", "Water", "Salt"],
        "calories": 310
    },
    "biryani": {
        "description": "Biryani is a flavorful South Asian rice dish made with spices, rice, and meat or vegetables.",
        "ingredients": ["Basmati Rice", "Spices", "Chicken or Vegetables"],
        "calories": 450
    },
    "sushi": {
        "description": "Sushi is a Japanese dish consisting of vinegared rice with seafood, vegetables, and sometimes tropical fruits.",
        "ingredients": ["Rice", "Seaweed", "Fish", "Vinegar"],
        "calories": 200
    }
}

@app.route("/", methods=["GET", "POST"])
def home():
    dish_info = None
    dish_name = ""
    if request.method == "POST":
        dish_name = request.form["dish"].lower()
        dish_info = dish_data.get(dish_name)
        if not dish_info:
            return render_template("result.html", dish_name=dish_name, not_found=True)

    return render_template("index.html", dish_info=dish_info, dish_name=dish_name)

if __name__ == "__main__":
    app.run(debug=True)
