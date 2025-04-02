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

# Get user name
user_name = input("Enter your name: ").strip().title()
print(f"\nHello {user_name}! Welcome to Tax Assistant.\n")

print("===========Welcome to Tax Assistant===============")
income = float(input("Enter your income: "))
expenses = float(input("Enter your expenses: "))
taxable_income = income - expenses
print("Choose your tax regime: ")
print("1. Old Tax Regime (with deductions)")
print("2. New Tax Regime (lower tax but no deductions)")
choice = int(input("Enter 1 or 2: "))
def calculate_old_tax(income):
    tax = 0
    if income > 1000000:
        tax += (income - 1000000) * 0.3
        income = 1000000
    if income > 500000:
        tax += (income - 500000) * 0.2
        income = 500000
    if income > 250000:
        tax += (income - 250000) * 0.05  # 5% tax in old regime
    return tax

def calculate_new_tax(income):
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
if choice == 1:
    tax = calculate_old_tax(taxable_income)
elif choice == 2:
    tax = calculate_new_tax(taxable_income)
else:
    print("Invalid choice! Defaulting to Old Tax Regime.")
    tax = calculate_old_tax(taxable_income)

exchange_rate = get_exchange_rate()

# Display the tax amount in both INR and USD
print("\n========= Tax Summary =========")
print(f"Taxable Income: ₹{taxable_income}")
print(f"Tax to be Paid (INR): ₹{tax}")
if exchange_rate:
    tax_in_usd = round(tax * exchange_rate, 2)
    print(f"Tax to be Paid (USD): ${tax_in_usd}")
else:
    print("Failed to fetch exchange rate. Showing INR only.")
print("=======================================")

# Save updated tax report with USD conversion
with open("tax_report.txt", "w", encoding="utf-8") as file:
    file.write(f"=========== Tax Report for {user_name} ===============\n")
    file.write(f"Income: ₹{income}\n")
    file.write(f"Expenses: ₹{expenses}\n")
    file.write(f"Taxable Income: ₹{taxable_income}\n")
    file.write(f"Tax Paid (INR): ₹{tax}\n")
    if exchange_rate:
        file.write(f"Tax Paid (USD): ${tax_in_usd}\n")
    else:
        file.write("Failed to fetch exchange rate. Showing INR only.\n")
    file.write("===============================\n")

print(f"Tax report saved as 'tax_report.txt'! for {user_name}")


     
    