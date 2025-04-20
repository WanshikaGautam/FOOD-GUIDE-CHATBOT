import requests  # Import the requests module

def get_exchange_rate():
    url = "https://api.exchangerate-api.com/v4/latest/INR"  # Free exchange rate API
    try:
        response = requests.get(url)  # Sending API request
        data = response.json()  # Convert response to JSON format
        return data["rates"]["USD"]  # Extract INR to USD exchange rate
    except Exception as e:
        print("Error fetching exchange rate:", e)
        return None

# Dessert data
desserts = {
    "gulab jamun": {
        "description": "A traditional Indian sweet made from milk solids, soaked in rose-flavored sugar syrup.",
        "ingredients": ["Milk solids (khoya)", "Sugar", "Rose water", "Cardamom", "Ghee"],
        "calories": 300
    },
    "cheesecake": {
        "description": "A creamy dessert made with a soft cheese base, often with a crust and fruit topping.",
        "ingredients": ["Cream cheese", "Graham crackers", "Butter", "Sugar", "Eggs", "Vanilla"],
        "calories": 450
    },
    "brownie": {
        "description": "A rich, chocolate baked dessert with a fudgy or cakey texture.",
        "ingredients": ["Dark chocolate", "Butter", "Sugar", "Flour", "Eggs"],
        "calories": 400
    },
    "rasgulla": {
        "description": "A soft, spongy Indian sweet made from chenna (curdled milk) and soaked in sugar syrup.",
        "ingredients": ["Chenna", "Sugar", "Water", "Rose water"],
        "calories": 180
    }
}

# Get user name
user_name = input("Enter your name: ").strip().title()
print(f"\nHello {user_name}! Welcome to the Dessert Chatbot 🍮\n")

print("========= Available Desserts =========")
for dessert in desserts.keys():
    print(f"- {dessert.title()}")

dessert_name = input("\nEnter the name of a dessert you'd like to know about: ").strip().lower()

# Fetch dessert details
dessert_info = desserts.get(dessert_name)

if dessert_info:
    print("\n========= Dessert Details =========")
    print(f"Dessert: {dessert_name.title()}")
    print(f"Description: {dessert_info['description']}")
    print("Ingredients:", ", ".join(dessert_info["ingredients"]))
    print(f"Estimated Calories: {dessert_info['calories']} kcal")
    print("=====================================")

    # Save to text file
    with open("dessert_info.txt", "w", encoding="utf-8") as file:
        file.write(f"=========== Dessert Report for {user_name} ===============\n")
        file.write(f"Dessert: {dessert_name.title()}\n")
        file.write(f"Description: {dessert_info['description']}\n")
        file.write(f"Ingredients: {', '.join(dessert_info['ingredients'])}\n")
        file.write(f"Estimated Calories: {dessert_info['calories']} kcal\n")
        file.write("==========================================================\n")

    print(f"\nDessert report saved as 'dessert_info.txt'! 🍰")
else:
    print(f"\nSorry {user_name}, we don't have information on '{dessert_name.title()}'. 😔")
