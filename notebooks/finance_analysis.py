import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# PERSONAL FINANCE INTELLIGENCE - EDA
# ==========================================

print("====================================")
print("PERSONAL FINANCE DATA ANALYSIS")
print("====================================")

# Load dataset
df = pd.read_csv("../data/transactions.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Make sure images folder exists
os.makedirs("../images", exist_ok=True)

# ==========================================
# BASIC INFORMATION
# ==========================================

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 10 Records:")
print(df.head(10))

# ==========================================
# INCOME AND EXPENSE
# ==========================================

income = df[df["Transaction_Type"] == "Income"]["Amount"].sum()
expense = df[df["Transaction_Type"] == "Expense"]["Amount"].sum()
balance = income - expense

print("\nTotal Income:", income)
print("Total Expense:", expense)
print("Remaining Balance:", balance)

# ==========================================
# TRANSACTION TYPE
# ==========================================

print("\nTransaction Type:")
print(df["Transaction_Type"].value_counts())

# ==========================================
# CATEGORY-WISE EXPENSE
# ==========================================

expense_df = df[df["Transaction_Type"] == "Expense"].copy()

category_expense = (
    expense_df.groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nCategory-wise Expense:")
print(category_expense)

# ==========================================
# PAYMENT MODE
# ==========================================

print("\nPayment Mode Usage:")
print(df["Payment_Mode"].value_counts())

# ==========================================
# MONTHLY EXPENSE
# ==========================================

expense_df["Month"] = expense_df["Date"].dt.to_period("M")

monthly_expense = (
    expense_df.groupby("Month")["Amount"]
    .sum()
)

print("\nMonthly Expense:")
print(monthly_expense)

# ==========================================
# GRAPH 1 - CATEGORY-WISE EXPENSE
# ==========================================

plt.figure(figsize=(10, 5))

category_expense.plot(kind="bar")

plt.title("Category-wise Expense")
plt.xlabel("Category")
plt.ylabel("Total Expense")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("../images/category_expense.png", dpi=300)
plt.close()

print("\nGraph 1 saved: category_expense.png")

# ==========================================
# GRAPH 2 - MONTHLY EXPENSE
# ==========================================

plt.figure(figsize=(10, 5))

monthly_expense.plot(kind="line", marker="o")

plt.title("Monthly Expense Trend")
plt.xlabel("Month")
plt.ylabel("Total Expense")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("../images/monthly_expense.png", dpi=300)
plt.close()

print("Graph 2 saved: monthly_expense.png")

# ==========================================
# GRAPH 3 - PAYMENT MODE
# ==========================================

plt.figure(figsize=(8, 5))

payment_count = df["Payment_Mode"].value_counts()

payment_count.plot(kind="bar")

plt.title("Payment Mode Usage")
plt.xlabel("Payment Mode")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("../images/payment_mode.png", dpi=300)
plt.close()

print("Graph 3 saved: payment_mode.png")

# ==========================================
# FINAL MESSAGE
# ==========================================

print("\n====================================")
print("ANALYSIS COMPLETED SUCCESSFULLY!")
print("====================================")

print("\nAll 3 graphs have been saved in:")
print("Personal_Finance_Intelligence/images/")

print("\nFiles:")
print("1. category_expense.png")
print("2. monthly_expense.png")
print("3. payment_mode.png")