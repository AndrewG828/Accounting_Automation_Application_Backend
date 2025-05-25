import pandas as pd
import re
import joblib
from sklearn.metrics import accuracy_score, classification_report

# === Load trained model ===
model = joblib.load("transaction_classifier.pkl")

# === Normalize function ===
def normalize_description(desc):
    desc = desc.lower()
    desc = re.sub(r'[^a-z\s]', '', desc)
    desc = re.sub(r'\s+', ' ', desc).strip()
    return desc

# === Load and clean test data ===
csv_path = "testing.csv"  # Replace with your file path
df = pd.read_csv(csv_path)

# Ensure correct columns exist
assert "Description" in df.columns and "Amount" in df.columns, "CSV must contain 'Description' and 'Amount' columns."

# Drop rows with missing data
df = df.dropna(subset=["Description", "Amount"])

# === Preprocessing ===
df["Normalized_Description"] = df["Description"].apply(normalize_description)
df["Amount_Sign"] = df["Amount"].apply(lambda x: "positive" if x > 0 else "negative")
df["Combined_Input"] = df["Normalized_Description"] + " " + df["Amount_Sign"]

# === Predict with probabilities ===
X_test = df["Combined_Input"]
probas = model.predict_proba(X_test)
labels = model.classes_

# === Apply threshold logic ===
threshold = 0.9
predictions = []
confidences = []

for probs in probas:
    max_prob = max(probs)
    top_label = labels[probs.argmax()]
    predictions.append(top_label if max_prob >= threshold else "UNMATCHED")
    confidences.append(max_prob)

# === Add predictions to DataFrame ===
df["Predicted_Account"] = predictions
df["Confidence"] = confidences

# Optional: if Account column is included, show evaluation
if "Account" in df.columns:
    # Ensure both 'Account' and 'Predicted_Account' are strings
    df["Account"] = df["Account"].apply(lambda x: str(x) if pd.notnull(x) else 'UNMATCHED')  # Replace NaN with 'UNMATCHED' and convert to string
    df["Predicted_Account"] = df["Predicted_Account"].apply(lambda x: str(x) if pd.notnull(x) else 'UNMATCHED')  # Same for predicted accounts

    # Remove any blank strings by replacing them with 'UNMATCHED'
    df["Account"] = df["Account"].replace("", 'UNMATCHED')
    df["Account"] = df["Account"].replace("Match", 'UNMATCHED')
    df["Predicted_Account"] = df["Predicted_Account"].replace("", 'UNMATCHED')

    # Now calculate accuracy and classification report
    accuracy = accuracy_score(df["Account"], df["Predicted_Account"])
    print(f"\n✅ Prediction Accuracy: {accuracy * 100:.2f}%\n")
    print("\nClassification Report:\n")
    print(classification_report(df["Account"], df["Predicted_Account"]))

    # Show incorrect predictions (where Account does not match Predicted_Account)
    incorrect_predictions = df[df["Account"] != df["Predicted_Account"]]
    
    # Only print the incorrect predictions
    if len(incorrect_predictions) > 0:
        print(f"\n❌ Incorrect Predictions (Total: {len(incorrect_predictions)}):")
        print(incorrect_predictions[["Description", "Amount", "Account", "Predicted_Account", "Confidence"]])

# Preview predictions (optional, showing a small sample)
print("\nSummary DataFrame (Top 10 rows):\n")
print(df[["Description", "Amount", "Predicted_Account", "Confidence"]].head(10))
