import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. Load the data
df = pd.read_csv("./Sorting_Data.csv")

# 2. Normalize descriptions (same as before)
def normalize_description(desc):
    desc = desc.lower()
    desc = re.sub(r'[^a-z\s]', '', desc)
    desc = re.sub(r'\s+', ' ', desc).strip()
    return desc

df["Normalized_Description"] = df["Description"].apply(normalize_description)

# 3. Add a column for amount sign (as string to treat it like text)
df["Amount_Sign"] = df["Amount"].apply(lambda x: "positive" if x > 0 else "negative")

# 4. Combine text and sign for modeling
df["Combined_Input"] = df["Normalized_Description"] + " " + df["Amount_Sign"]

# 5. Split features and labels
X = df["Combined_Input"]
y = df["Account"]

# 6. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 7. Define pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 3),
        min_df=2,
        max_df=0.95,
        stop_words='english'
    )),
    ("svm", SVC(
        kernel='linear',
        C=1.0,
        probability=True
    ))
])

# 8. Train the model
print("Training the SVM model with amount sign included...")
pipeline.fit(X_train, y_train)

# 9. Evaluate
y_pred = pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {acc:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 10. Save the model
joblib.dump(pipeline, "best_svm_transaction_classifier_with_amount.pkl")
print("\nModel saved as 'best_svm_transaction_classifier_with_amount.pkl'")
