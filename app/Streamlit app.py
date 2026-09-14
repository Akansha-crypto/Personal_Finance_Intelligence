import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Personal Finance Intelligence",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------

st.title("💰 Personal Finance Intelligence")
st.subheader("Smart Expense Analysis & Financial Insights")

st.write(
    "This application analyzes your transactions and provides "
    "spending insights, financial health and recommendations."
)

# -----------------------------------
# LOAD DATA
# -----------------------------------

DATA_PATH = "../data/transactions.csv"

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    st.error("transactions.csv file not found!")
    st.stop()

# Convert date
df["Date"] = pd.to_datetime(
    df["Date"],
    format="mixed",
    dayfirst=True
)

# -----------------------------------
# BASIC CALCULATIONS
# -----------------------------------

income = df[df["Transaction_Type"] == "Income"]["Amount"].sum()

expense_df = df[df["Transaction_Type"] == "Expense"]

expense = expense_df["Amount"].sum()

balance = income - expense

if income > 0:
    savings_rate = (balance / income) * 100
else:
    savings_rate = 0

# -----------------------------------
# DASHBOARD METRICS
# -----------------------------------

st.markdown("## 📊 Financial Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Income",
        f"₹{income:,.0f}"
    )

with col2:
    st.metric(
        "Total Expenses",
        f"₹{expense:,.0f}"
    )

with col3:
    st.metric(
        "Balance",
        f"₹{balance:,.0f}"
    )

with col4:
    st.metric(
        "Savings Rate",
        f"{savings_rate:.2f}%"
    )

# -----------------------------------
# EXPENSE BY CATEGORY
# -----------------------------------

st.markdown("---")
st.markdown("## 🛒 Expense Analysis")

category_expense = (
    expense_df
    .groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

col1, col2 = st.columns(2)

with col1:

    st.write("### Category-wise Expenses")

    fig, ax = plt.subplots()

    category_expense.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Category")
    ax.set_ylabel("Expense (₹)")
    ax.set_title("Expense by Category")

    plt.xticks(rotation=45)

    st.pyplot(fig)

with col2:

    st.write("### Payment Mode Usage")

    payment_mode = (
        expense_df["Payment_Mode"]
        .value_counts()
    )

    fig, ax = plt.subplots()

    payment_mode.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )

    ax.set_ylabel("")

    st.pyplot(fig)

# -----------------------------------
# MONTHLY EXPENSE
# -----------------------------------

st.markdown("---")
st.markdown("## 📈 Monthly Spending")

monthly_expense = (
    expense_df
    .groupby(
        expense_df["Date"].dt.to_period("M")
    )["Amount"]
    .sum()
)

monthly_expense.index = monthly_expense.index.astype(str)

fig, ax = plt.subplots()

monthly_expense.plot(
    kind="line",
    marker="o",
    ax=ax
)

ax.set_xlabel("Month")
ax.set_ylabel("Expense (₹)")
ax.set_title("Monthly Expense Trend")

plt.xticks(rotation=45)

st.pyplot(fig)

# -----------------------------------
# HIGHEST SPENDING CATEGORY
# -----------------------------------

highest_category = category_expense.idxmax()
highest_amount = category_expense.max()

st.markdown("---")
st.markdown("## 🔍 Spending Insight")

st.info(
    f"Your highest spending category is "
    f"**{highest_category}** with an expense of "
    f"**₹{highest_amount:,.0f}**."
)

# -----------------------------------
# FINANCIAL HEALTH SCORE
# -----------------------------------

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

# Expense-income ratio
expense_ratio = (
    (expense / income) * 100
    if income > 0 else 100
)

if expense_ratio <= 70:
    score += 30
elif expense_ratio <= 85:
    score += 20
elif expense_ratio <= 100:
    score += 10

# Spending concentration
highest_percentage = (
    highest_amount / expense * 100
    if expense > 0 else 100
)

if highest_percentage <= 25:
    score += 20
elif highest_percentage <= 40:
    score += 10
else:
    score += 5

# Positive balance
if balance > 0:
    score += 10

# Health status
if score >= 80:
    health = "Excellent 🟢"
elif score >= 60:
    health = "Good 🟢"
elif score >= 40:
    health = "Average 🟡"
else:
    health = "Poor 🔴"

# -----------------------------------
# DISPLAY HEALTH
# -----------------------------------

st.markdown("---")
st.markdown("## ❤️ Financial Health")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Financial Health Score",
        f"{score}/100"
    )

with col2:
    st.metric(
        "Financial Status",
        health
    )

# -----------------------------------
# RECOMMENDATIONS
# -----------------------------------

st.markdown("---")
st.markdown("## 💡 Personalized Recommendations")

recommendations = []

if highest_category == "Shopping":
    recommendations.append(
        "Control shopping expenses and avoid unnecessary purchases."
    )

if highest_category == "Entertainment":
    recommendations.append(
        "Try reducing entertainment expenses to increase savings."
    )

if highest_category == "Food":
    recommendations.append(
        "Consider reducing food delivery and outside food expenses."
    )

if highest_category == "Rent":
    recommendations.append(
        "Rent is your highest expense. Plan your remaining budget carefully."
    )

if savings_rate < 10:
    recommendations.append(
        "Your savings rate is low. Try to save at least 10% of your income."
    )
else:
    recommendations.append(
        "Maintain your current saving habit and build an emergency fund."
    )

if expense_ratio > 85:
    recommendations.append(
        "Your expenses are high compared with your income. "
        "Consider setting monthly spending limits."
    )

for recommendation in recommendations:
    st.write("👉", recommendation)

# -----------------------------------
# TRANSACTION DATA
# -----------------------------------

st.markdown("---")
st.markdown("## 📋 Transaction Data")

st.write(
    f"Total Transactions: **{len(df)}**"
)

st.dataframe(
    df,
    use_container_width=True
)

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "Personal Finance Intelligence | Data Science Project"
)