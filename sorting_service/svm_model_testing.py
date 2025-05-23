import joblib

model = joblib.load("best_svm_transaction_classifier.pkl")

# Sample real-world transaction descriptions
test_descriptions = [
    "UBER *TRIP OCT03A 800-123-4567",         # should match Accounts Receivable
    "GGL*YouTube Premium 650-253-0000 CA",    # Dues and Subscriptions
    "WALMART SUPERCENTER #1234",             # Food Purchases
    "EXXONMOBIL 12345678 TX",                # Automobile Expense
    "IPFS CORPORATION PAYMENT 123456",       # Insurance Expense
    "HOME DEPOT #3827 TOOLS AND SUPPLIES",   # Repairs and Maintenance
    "ADOBE PHOTOGPHY PLAN ADOBE.COM CA",     # Likely Dues and Subscriptions or new category
    "Amazon Prime Membership",               # Dues and Subscriptions
    "Unknown charge TINY MART",              # Could be ambiguous
]

predicted_accounts = model.predict(test_descriptions)

# Show results
for desc, account in zip(test_descriptions, predicted_accounts):
    print(f"{desc} → {account}")
