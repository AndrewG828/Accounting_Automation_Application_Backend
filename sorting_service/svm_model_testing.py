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
    {"Description": "Paypal payment", "Amount": 1500.21, "Expected_Account": "UNMATCHED"},
])

# Preprocessing
test_data["Normalized_Description"] = test_data["Description"].apply(normalize_description)
test_data["Amount_Sign"] = test_data["Amount"].apply(lambda x: "positive" if x > 0 else "negative")
test_data["Combined_Input"] = test_data["Normalized_Description"] + " " + test_data["Amount_Sign"]

# Predict with probabilities
X_test = test_data["Combined_Input"]
probas = model.predict_proba(X_test)
labels = model.classes_

# Apply threshold logic (optional)
threshold = 0.9
predictions = []
confidences = []

for i, probs in enumerate(probas):
    max_prob = max(probs)
    top_label = labels[probs.argmax()]
    confidences.append(max_prob)
    if max_prob >= threshold:
        predictions.append(top_label)
    else:
        predictions.append("UNMATCHED")

# Add predictions to DataFrame
test_data["Predicted_Account"] = predictions
test_data["Confidence"] = confidences

# Print accuracy
accuracy = accuracy_score(test_data["Expected_Account"], test_data["Predicted_Account"])
print(f"\n✅ Prediction Accuracy: {accuracy * 100:.2f}%\n")

# Print detailed row-by-row comparison
print("Detailed Predictions:")
for i, row in test_data.iterrows():
    print(f"{row['Combined_Input']} → predicted: {row['Predicted_Account']} ({row['Confidence']:.2f}), actual: {row['Expected_Account']}")

# Print summary DataFrame
print("\nDataFrame View:\n")
print(test_data[["Description", "Amount", "Expected_Account", "Predicted_Account", "Confidence"]])

# Classification report
print("\nClassification Report:\n")
print(classification_report(test_data["Expected_Account"], test_data["Predicted_Account"]))
