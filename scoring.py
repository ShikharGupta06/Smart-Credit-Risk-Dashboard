# scoring.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# 1. Load processed dataset
df = pd.read_csv("data/processed_dataset.csv")

# For demo: make a fake "target" column
# (1 = positive news/stock up, 0 = negative news/stock down)
df["target"] = [1, 0, 1, 1, 0]  # Just dummy labels

# 2. Define features (X) and labels (y)
# We'll use stock closing price as the feature
X = df[["Close"]]
y = df["target"]

# 3. Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train a simple Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# 5. Save the model for later use
with open("data/scoring_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved at data/scoring_model.pkl")
