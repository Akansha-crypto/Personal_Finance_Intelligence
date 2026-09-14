import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
df = pd.read_csv("../data/transactions.csv")

# Convert Date column
df["Date"] = pd.to_datetime(
    df["Date"],
    format="mixed",
    dayfirst=True
)

# Keep only expenses
expenses = df[df["Transaction_Type"] == "Expense"].copy()

# Create date features
expenses["Month"] = expenses["Date"].dt.month
expenses["Day"] = expenses["Date"].dt.day
expenses["DayOfWeek"] = expenses["Date"].dt.dayofweek

# Features
X = expenses[
    ["Month", "Day", "DayOfWeek", "Category", "Payment_Mode"]
]

# Target
y = expenses["Amount"]

# Categorical and numerical features
categorical_features = ["Category", "Payment_Mode"]
numerical_features = ["Month", "Day", "DayOfWeek"]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)

# Random Forest model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    max_depth=10
)

# Complete ML pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
pipeline.fit(X_train, y_train)

# Predictions
y_pred = pipeline.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("----- Improved Expense Prediction Model -----")
print("Total Expense Transactions:", len(expenses))
print("Training Data:", len(X_train))
print("Testing Data:", len(X_test))

print("\nModel Evaluation:")
print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 2))

# Example prediction
new_data = pd.DataFrame({
    "Month": [10],
    "Day": [15],
    "DayOfWeek": [3],
    "Category": ["Food"],
    "Payment_Mode": ["UPI"]
})

prediction = pipeline.predict(new_data)

print(
    "\nPredicted Expense for Example Transaction: ₹",
    round(prediction[0], 2)
)

# Save model
os.makedirs("../models", exist_ok=True)

import joblib
joblib.dump(pipeline, "../models/expense_prediction_model.pkl")

print("\nModel saved successfully!")