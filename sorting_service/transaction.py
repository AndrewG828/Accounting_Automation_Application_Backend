from flask import Flask, request, jsonify
import joblib
import pandas as pd
import re


app = Flask(__name__)

# Load model and label classes once
model = joblib.load("transaction_classifier.pkl")
labels = model.classes_
threshold = 0.9

def normalize_description(desc):
    desc = desc.lower()
    desc = re.sub(r'[^a-z\s]', '', desc)
    desc = re.sub(r'\s+', ' ', desc).strip()
    return desc

def preprocess_and_predict(records):
    df = pd.DataFrame(records)

    # Basic validation
    required_cols = {"Description", "Amount"}
    if not required_cols.issubset(df.columns):
        raise ValueError("Missing required fields in input data.")

    # Convert Amount to float if needed
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna(subset=["Description", "Amount"])

    df["Normalized_Description"] = df["Description"].apply(normalize_description)
    df["Amount_Sign"] = df["Amount"].apply(lambda x: "positive" if x > 0 else "negative")
    df["Combined_Input"] = df["Normalized_Description"] + " " + df["Amount_Sign"]

    X = df["Combined_Input"]
    probas = model.predict_proba(X)

    predictions = []
    confidences = []

    for probs in probas:
        max_prob = max(probs)
        top_label = labels[probs.argmax()]
        predictions.append(top_label if max_prob >= threshold else "")
        confidences.append(round(max_prob, 4))

    df["Account"] = predictions
    # df["Confidence"] = confidences

    return df.to_dict(orient="records")


@app.route("/predict", methods = ['POST'])
def predict():
    input = request.get_json()

    if not input or "csvData" not in input:
        return jsonify({"Error": "Missing input and/or csv data in request."}), 400
    
    try:
        processed_data = preprocess_and_predict(input["csvData"])
        response = {
            "bankRecordId": input.get("bankRecordId"),
            "clientId": input.get("clientId"),
            "csvData": processed_data
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)