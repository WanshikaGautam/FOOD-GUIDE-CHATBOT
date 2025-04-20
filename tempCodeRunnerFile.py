from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_exchange_rate():
    """Fetch real-time exchange rate from INR to USD"""
    url = "https://api.exchangerate-api.com/v4/latest/INR"
    try:
        response = requests.get(url)
        data = response.json()
        return data["rates"]["USD"]
    except Exception as e:
        print("Error fetching exchange rate:", e)
        return None
app = Flask(__name__)

# Simulated dish dataset
dish_data = {
    "pasta": {
        "description": "Pasta is a staple Italian dish made from durum wheat and water.",
        "ingredients": ["Durum Wheat", "Water", "Olive Oil", "Salt"],
        "calories": 310
    },
    "biryani": {
        "description": "Biryani is a flavorful rice dish cooked with aromatic spices and meat or veggies.",
        "ingredients": ["Rice", "Chicken", "Spices", "Yogurt", "Onions"],
        "calories": 480
    },
    "sushi": {
        "description": "Sushi is a Japanese dish with vinegared rice, raw fish, and vegetables.",
        "ingredients": ["Sushi Rice", "Nori", "Raw Fish", "Avocado", "Soy Sauce"],
        "calories": 200
    },
    "dosa": {
        "description": "Dosa is a South Indian crispy crepe made from fermented rice and urad dal.",
        "ingredients": ["Rice", "Urad Dal", "Salt", "Water", "Oil"],
        "calories": 160
    }
}

@app.route("/", methods=["GET", "POST"])
def home():
    dish_info = None
    dish_name = ""
    if request.method == "POST":
        dish_name = request.form["dish"].lower()
        dish_info = dish_data.get(dish_name)

        return render_template("result.html", dish_name=dish_name, dish_info=dish_info)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
