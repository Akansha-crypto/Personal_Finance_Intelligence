import pandas as pd

# Load dataset
df = pd.read_csv("../data/transactions.csv")

# Convert date
df["Date"] = pd.to_datetime(
    df["Date"],
    format="mixed",
    dayfirst=True
)

# Keep only expenses
expenses = df[df["Transaction_Type"] == "Expense"].copy()

# Total expense
total_expense = expenses["Amount"].sum()

# Category-wise expense
category_expense = (
    expenses.groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("----- Personal Finance Recommendations -----")

print("\nTotal Expense: ₹", round(total_expense, 2))

print("\nCategory-wise Expenses:")
print(category_expense)

# Highest spending category
highest_category = category_expense.index[0]
highest_amount = category_expense.iloc[0]

print("\nHighest Spending Category:")
print(highest_category, "₹", round(highest_amount, 2))

# Generate recommendation
print("\n----- Financial Recommendations -----")

print(
    f"1. Your highest spending category is {highest_category}. "
    f"Consider reducing spending in this category."
)

# Check categories for recommendations
if "Shopping" in category_expense.index:
    shopping = category_expense["Shopping"]

    if shopping > total_expense * 0.15:
        print(
            "2. Shopping expenses are relatively high. "
            "Try setting a monthly shopping budget."
        )

if "Entertainment" in category_expense.index:
    entertainment = category_expense["Entertainment"]

    if entertainment > total_expense * 0.10:
        print(
            "3. Entertainment expenses are high. "
            "Consider reducing unnecessary entertainment spending."
        )

if "Food" in category_expense.index:
    food = category_expense["Food"]

    if food > total_expense * 0.15:
        print(
            "4. Food expenses are high. "
            "Try reducing outside food and food delivery expenses."
        )

print(
    "\n5. Maintain a monthly budget and track your expenses regularly."
)

print(
    "6. Try to save at least 10-20% of your monthly income."
)

print("\nRecommendation system completed successfully!")