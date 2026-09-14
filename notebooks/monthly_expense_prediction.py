import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

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

# Create Month column
expenses["Month"] = expenses["Date"].dt.to_period("M")

# Calculate total expense for each month
monthly_expense = expenses.groupby("Month")["Amount"].sum().reset_index()

# Convert month to number
monthly_expense["Month_Number"] = range(1, len(monthly_expense) + 1)

# Features and target
X = monthly_expense[["Month_Number"]]
y = monthly_expense["Amount"]

# Use first 80% for training
split_point = int(len(monthly_expense) * 0.8)

X_train = X.iloc[:split_point]
X_test = X.iloc[split_point:]

y_train = y.iloc[:split_point]
y_test = y.iloc[split_point:]

# Create model
model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Predict test data
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Predict next month
next_month = np.array([[len(monthly_expense) + 1]])
next_month_prediction = model.predict(next_month)[0]

print("----- Monthly Expense Prediction -----")

print("Total Months:", len(monthly_expense))
print("Training Months:", len(X_train))
print("Testing Months:", len(X_test))

print("\nModel Evaluation:")
print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 2))

print(
    "\nPredicted Next Month Expense: ₹",
    round(next_month_prediction, 2)
)

print("\nMonthly Expense Data:")
print(monthly_expense)# -----------------------------
# Actual vs Predicted Graph
# -----------------------------

import matplotlib.pyplot as plt
import os

# Create images folder if it does not exist
os.makedirs("../images", exist_ok=True)

# Predict values for all months
all_predictions = model.predict(X)

# Create graph
plt.figure(figsize=(10, 5))

plt.plot(
    monthly_expense["Month"].astype(str),
    monthly_expense["Amount"],
    marker="o",
    label="Actual Expense"
)

plt.plot(
    monthly_expense["Month"].astype(str),
    all_predictions,
    marker="o",
    linestyle="--",
    label="Predicted Expense"
)

plt.title("Actual vs Predicted Monthly Expense")
plt.xlabel("Month")
plt.ylabel("Expense Amount (₹)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Save graph
plt.savefig("../images/monthly_actual_vs_predicted.png", dpi=300)

plt.close()

print("\nGraph saved: monthly_actual_vs_predicted.png")