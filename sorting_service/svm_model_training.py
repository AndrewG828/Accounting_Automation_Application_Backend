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

# 2. Normalize descriptions
def normalize_description(desc):
    desc = desc.lower()
    desc = re.sub(r'[^a-z\s]', '', desc)
    desc = re.sub(r'\s+', ' ', desc).strip()
    return desc

df["Normalized_Description"] = df["Description"].apply(normalize_description)

# 3. Split features and labels
X = df["Normalized_Description"]
y = df["Account"]

# 4. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Create SVM pipeline with tuned TF-IDF
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 3),      # unigrams, bigrams, trigrams
        min_df=2,                # ignore words that appear only once
        max_df=0.95,             # ignore very common words
        stop_words='english'
    )),
    ("svm", SVC(
        kernel='linear',         # best for text data
        C=1.0,                   # regularization strength
        probability=True
    ))
])

# 6. Train model
print("Training the SVM model...")
pipeline.fit(X_train, y_train)

# 7. Evaluate
y_pred = pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {acc:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 8. Save the model
joblib.dump(pipeline, "best_svm_transaction_classifier.pkl")
print("\nModel saved as 'best_svm_transaction_classifier.pkl'")
