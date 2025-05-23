import pandas as pd
import re
import joblib
from sklearn.metrics import accuracy_score, classification_report

# Load trained model
model = joblib.load("best_svm_transaction_classifier_with_amount.pkl")

# Normalize function
def normalize_description(desc):
    desc = desc.lower()
    desc = re.sub(r'[^a-z\s]', '', desc)
    desc = re.sub(r'\s+', ' ', desc).strip()
    return desc

# Define test cases with expected accounts
test_data = pd.DataFrame([
    {"Description": "Merchant Bankcd Deposit", "Amount": 1420.55, "Expected_Account": "Accounts Receivable"},
    {"Description": "Merchant Bankcd Fee", "Amount": -45.00, "Expected_Account": "Merchant Account Fees"},
    {"Description": "Stripe Processing Fee", "Amount": -18.23, "Expected_Account": "Merchant Account Fees"},
    {"Description": "Stripe Transfer", "Amount": 388.50, "Expected_Account": "Accounts Receivable"},
    {"Description": "ExxonMobil Fuel", "Amount": -75.20, "Expected_Account": "Automobile Expense"},
    {"Description": "Google Workspace", "Amount": -21.00, "Expected_Account": "Dues and Subscriptions"},
    {"Description": "Starbucks Coffee", "Amount": -6.89, "Expected_Account": "Meals and Entertainment"},
    {"Description": "Walmart Grocery", "Amount": -210.30, "Expected_Account": "Food Purchases"},
    {"Description": "Geico Auto Insurance", "Amount": -345.67, "Expected_Account": "Insurance Expense"},
    {"Description": "DoorDash Driver Pay", "Amount": 614.90, "Expected_Account": "Accounts Receivable"},
])

# Preprocessing
test_data["Normalized_Description"] = test_data["Description"].apply(normalize_description)
test_data["Amount_Sign"] = test_data["Amount"].apply(lambda x: "positive" if x > 0 else "negative")
test_data["Combined_Input"] = test_data["Normalized_Description"] + " " + test_data["Amount_Sign"]

# Predict using model
test_data["Predicted_Account"] = model.predict(test_data["Combined_Input"])

# Accuracy check
accuracy = accuracy_score(test_data["Expected_Account"], test_data["Predicted_Account"])
print(f"\n✅ Prediction Accuracy: {accuracy * 100:.2f}%\n")
print("Detailed Comparison:\n")
print(test_data[["Description", "Amount", "Expected_Account", "Predicted_Account"]])

# Optional detailed report
print("\nClassification Report:\n")
print(classification_report(test_data["Expected_Account"], test_data["Predicted_Account"]))
