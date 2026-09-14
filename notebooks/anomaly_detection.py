import pandas as pd
import numpy as np
import os

from sklearn.ensemble import IsolationForest

# Load dataset
df = pd.read_csv("../data/transactions.csv")

# Convert Date
df["Date"] = pd.to_datetime(
    df["Date"],
    format="mixed",
    dayfirst=True
)

# Keep only expenses
expenses = df[df["Transaction_Type"] == "Expense"].copy()

# Select amount for anomaly detection
X = expenses[["Amount"]]

# Create Isolation Forest model
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

# Detect anomalies
expenses["Anomaly"] = model.fit_predict(X)

# -1 = anomaly, 1 = normal
anomalies = expenses[expenses["Anomaly"] == -1].copy()

print("----- Expense Anomaly Detection -----")

print("Total Expense Transactions:", len(expenses))
print("Unusual Expenses Detected:", len(anomalies))

print("\nTop Unusual Expenses:")

top_anomalies = anomalies.sort_values(
    by="Amount",
    ascending=False
).head(10)

print(
    top_anomalies[
        [
            "Transaction_ID",
            "Date",
            "Description",
            "Amount",
            "Category",
            "Payment_Mode"
        ]
    ].to_string(index=False)
)

# Save anomaly results
os.makedirs("../images", exist_ok=True)

top_anomalies[
    [
        "Transaction_ID",
        "Date",
        "Description",
        "Amount",
        "Category",
        "Payment_Mode"
    ]
].to_csv(
    "../images/unusual_expenses.csv",
    index=False
)

print("\nAnomaly results saved successfully!")