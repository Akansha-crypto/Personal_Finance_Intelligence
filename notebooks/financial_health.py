import pandas as pd

# Load dataset
df = pd.read_csv("../data/transactions.csv")

# Convert date
df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=True)

# Separate income and expenses
income = df[df["Transaction_Type"] == "Income"]["Amount"].sum()
expense = df[df["Transaction_Type"] == "Expense"]["Amount"].sum()

# Calculate balance
balance = income - expense

# Savings rate
if income > 0:
    savings_rate = (balance / income) * 100
else:
    savings_rate = 0

# Category-wise expenses
expense_df = df[df["Transaction_Type"] == "Expense"]
category_expense = expense_df.groupby("Category")["Amount"].sum()

# Highest spending category
highest_category = category_expense.idxmax()
highest_category_amount = category_expense.max()

# Calculate highest category percentage
highest_category_percentage = (highest_category_amount / expense) * 100


# -------------------------------
# Financial Health Score
# -------------------------------

score = 0

# Savings condition
if savings_rate >= 20:
    score += 40
elif savings_rate >= 10:
    score += 30
elif savings_rate >= 5:
    score += 20
else:
    score += 10

# Expense vs income
expense_ratio = (expense / income) * 100 if income > 0 else 100

if expense_ratio <= 70:
    score += 30
elif expense_ratio <= 85:
    score += 20
elif expense_ratio <= 100:
    score += 10
else:
    score += 0

# Spending concentration
if highest_category_percentage <= 25:
    score += 20
elif highest_category_percentage <= 40:
    score += 10
else:
    score += 5

# Balance condition
if balance > 0:
    score += 10


# Health status
if score >= 80:
    health = "Excellent"
elif score >= 60:
    health = "Good"
elif score >= 40:
    health = "Average"
else:
    health = "Poor"


# -------------------------------
# Display Results
# -------------------------------

print("\n========== FINANCIAL HEALTH REPORT ==========")

print(f"Total Income: ₹{income:,.2f}")
print(f"Total Expense: ₹{expense:,.2f}")
print(f"Balance: ₹{balance:,.2f}")

print(f"Savings Rate: {savings_rate:.2f}%")
print(f"Expense Ratio: {expense_ratio:.2f}%")

print(f"\nHighest Spending Category: {highest_category}")
print(f"Highest Category Expense: ₹{highest_category_amount:,.2f}")
print(f"Category Percentage: {highest_category_percentage:.2f}%")

print(f"\nFinancial Health Score: {score}/100")
print(f"Financial Health Status: {health}")

print("\n==============================================")