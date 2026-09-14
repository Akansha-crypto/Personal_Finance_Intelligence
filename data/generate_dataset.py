import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Same dataset every time generate ho
np.random.seed(42)
random.seed(42)

# -----------------------------
# Settings
# -----------------------------
TOTAL_TRANSACTIONS = 1500

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

# -----------------------------
# Categories and descriptions
# -----------------------------
expense_data = {
    "Food": [
        "Swiggy", "Zomato", "Restaurant", "Cafe", "Pizza",
        "Lunch", "Dinner", "Coffee"
    ],
    "Transport": [
        "Uber", "Ola", "Auto Rickshaw", "Petrol",
        "Bus Pass", "Train Ticket", "Metro"
    ],
    "Shopping": [
        "Amazon", "Flipkart", "Myntra", "Clothes",
        "Shoes", "Electronics", "Accessories"
    ],
    "Bills": [
        "Electricity Bill", "Mobile Recharge",
        "Internet Bill", "Water Bill", "Gas Bill"
    ],
    "Entertainment": [
        "Netflix", "Spotify", "Movie", "Concert",
        "Gaming", "OTT Subscription"
    ],
    "Education": [
        "College Fees", "Books", "Course Fee",
        "Online Course", "Stationery"
    ],
    "Groceries": [
        "DMart", "BigBasket", "Reliance Smart",
        "Vegetables", "Groceries"
    ],
    "Healthcare": [
        "Medical Store", "Doctor Consultation",
        "Medicine", "Health Checkup"
    ],
    "Rent": [
        "House Rent", "PG Rent", "Room Rent"
    ]
}

income_data = {
    "Salary": [
        "Monthly Salary", "Salary Credit"
    ],
    "Freelance": [
        "Freelance Work", "Freelance Payment",
        "Project Payment"
    ],
    "Other Income": [
        "Cashback", "Interest", "Gift Received",
        "Other Income"
    ]
}

payment_modes = ["UPI", "Debit Card", "Credit Card", "Cash", "Bank Transfer"]

# -----------------------------
# Generate dates
# -----------------------------
date_range = (end_date - start_date).days

transactions = []

for i in range(TOTAL_TRANSACTIONS):

    transaction_date = start_date + timedelta(
        days=random.randint(0, date_range)
    )

    # Income approximately 15% of transactions
    if random.random() < 0.15:

        category = random.choice(list(income_data.keys()))
        description = random.choice(income_data[category])

        if category == "Salary":
            amount = random.randint(28000, 45000)

        elif category == "Freelance":
            amount = random.randint(2000, 15000)

        else:
            amount = random.randint(500, 5000)

        transaction_type = "Income"

    else:

        category = random.choice(list(expense_data.keys()))
        description = random.choice(expense_data[category])

        # Category-wise realistic expense ranges
        ranges = {
            "Food": (100, 1800),
            "Transport": (50, 2500),
            "Shopping": (300, 8000),
            "Bills": (300, 5000),
            "Entertainment": (100, 2500),
            "Education": (300, 10000),
            "Groceries": (300, 5000),
            "Healthcare": (200, 6000),
            "Rent": (6000, 20000)
        }

        low, high = ranges[category]
        amount = random.randint(low, high)

        transaction_type = "Expense"

    payment_mode = random.choice(payment_modes)

    transactions.append([
        f"T{i+1:04d}",
        transaction_date.strftime("%Y-%m-%d"),
        description,
        amount,
        transaction_type,
        category,
        payment_mode
    ])

# -----------------------------
# Create DataFrame
# -----------------------------
df = pd.DataFrame(
    transactions,
    columns=[
        "Transaction_ID",
        "Date",
        "Description",
        "Amount",
        "Transaction_Type",
        "Category",
        "Payment_Mode"
    ]
)

# Sort by date
df = df.sort_values("Date").reset_index(drop=True)

# Save CSV
df.to_csv("transactions.csv", index=False)

print("======================================")
print("DATASET CREATED SUCCESSFULLY!")
print("======================================")
print("Total Transactions:", len(df))
print("Columns:", len(df.columns))
print("Date Range:", df["Date"].min(), "to", df["Date"].max())
print("\nTransaction Type:")
print(df["Transaction_Type"].value_counts())

print("\nCategories:")
print(df["Category"].value_counts())

print("\nFirst 10 Records:")
print(df.head(10))

print("\nFile saved as: transactions.csv")