import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

from database import (
    save_monthly_finance,
    save_expense,
    get_monthly_history,
    get_expenses
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Personal Finance Intelligence",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Finance Intelligence")
st.caption("Expense Analysis • Spending Prediction • Financial Recommendations")


# --------------------------------------------------
# SIDEBAR - MONTHLY FINANCE INPUT
# --------------------------------------------------

st.sidebar.header("📊 Monthly Finance Input")

income = st.sidebar.number_input(
    "Monthly Income (₹)",
    min_value=0.0,
    value=50000.0,
    step=1000.0
)

st.sidebar.subheader("Category-wise Expenses")

categories = [
    "Rent",
    "Food",
    "Shopping",
    "Transport",
    "Bills",
    "Education",
    "Entertainment",
    "Healthcare",
    "Groceries",
    "Other"
]

category_expenses = {}

for category in categories:
    category_expenses[category] = st.sidebar.number_input(
        category + " (₹)",
        min_value=0.0,
        value=0.0,
        step=500.0
    )


calculate = st.sidebar.button(
    "Calculate Finance",
    use_container_width=True
)


# --------------------------------------------------
# CALCULATE MONTHLY FINANCE
# --------------------------------------------------

if calculate:

    total_expense = sum(category_expenses.values())

    balance = income - total_expense

    if income > 0:
        savings_rate = (balance / income) * 100
    else:
        savings_rate = 0

    current_month = date.today().strftime("%Y-%m")

    # Save to SQLite database
    save_monthly_finance(
        current_month,
        income,
        total_expense,
        balance,
        savings_rate
    )

    st.success("✅ Monthly finance saved successfully!")

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    st.subheader("📌 Financial Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Monthly Income",
        f"₹{income:,.0f}"
    )

    col2.metric(
        "Total Expense",
        f"₹{total_expense:,.0f}"
    )

    col3.metric(
        "Balance",
        f"₹{balance:,.0f}"
    )

    col4.metric(
        "Savings Rate",
        f"{savings_rate:.1f}%"
    )


    # --------------------------------------------------
    # FINANCIAL HEALTH SCORE
    # --------------------------------------------------

    st.subheader("❤️ Financial Health")

    score = 0

    # Savings score
    if savings_rate >= 20:
        score += 40
    elif savings_rate >= 10:
        score += 30
    elif savings_rate >= 5:
        score += 20
    else:
        score += 10

    # Expense ratio score
    if income > 0:
        expense_ratio = (total_expense / income) * 100
    else:
        expense_ratio = 100

    if expense_ratio <= 70:
        score += 30
    elif expense_ratio <= 85:
        score += 20
    elif expense_ratio <= 100:
        score += 10

    # Spending concentration
    if total_expense > 0:
        highest_category = max(
            category_expenses,
            key=category_expenses.get
        )

        highest_amount = category_expenses[highest_category]

        highest_percentage = (
            highest_amount / total_expense
        ) * 100

        if highest_percentage <= 25:
            score += 20
        elif highest_percentage <= 40:
            score += 10
        else:
            score += 5
    else:
        highest_category = "None"
        highest_percentage = 0

    # Positive balance
    if balance > 0:
        score += 10

    if score >= 80:
        status = "Excellent 🟢"
    elif score >= 60:
        status = "Good 🟡"
    elif score >= 40:
        status = "Average 🟠"
    else:
        status = "Poor 🔴"

    col1, col2 = st.columns(2)

    col1.metric(
        "Financial Health Score",
        f"{score}/100"
    )

    col2.metric(
        "Financial Status",
        status
    )


    # --------------------------------------------------
    # CATEGORY-WISE ANALYSIS
    # --------------------------------------------------

    st.subheader("📊 Category-wise Expense Analysis")

    category_df = pd.DataFrame(
        list(category_expenses.items()),
        columns=["Category", "Amount"]
    )

    category_df = category_df[
        category_df["Amount"] > 0
    ]

    if not category_df.empty:

        col1, col2 = st.columns(2)

        with col1:

            fig, ax = plt.subplots()

            ax.bar(
                category_df["Category"],
                category_df["Amount"]
            )

            ax.set_xlabel("Category")
            ax.set_ylabel("Expense (₹)")
            ax.set_title("Category-wise Expenses")

            plt.xticks(rotation=45)

            st.pyplot(fig)

        with col2:

            fig, ax = plt.subplots()

            ax.pie(
                category_df["Amount"],
                labels=category_df["Category"],
                autopct="%1.1f%%"
            )

            ax.set_title("Expense Distribution")

            st.pyplot(fig)


# --------------------------------------------------
# INDIVIDUAL EXPENSE ENTRY
# --------------------------------------------------

st.subheader("➕ Add Individual Expense")

with st.form("expense_form"):

    col1, col2 = st.columns(2)

    with col1:

        expense_date = st.date_input(
            "Date",
            value=date.today()
        )

        description = st.text_input(
            "Description",
            placeholder="Example: Swiggy, Amazon, Uber"
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=100.0
        )

    with col2:

        expense_category = st.selectbox(
            "Category",
            categories
        )

        payment_mode = st.selectbox(
            "Payment Mode",
            [
                "UPI",
                "Cash",
                "Credit Card",
                "Debit Card",
                "Bank Transfer"
            ]
        )

    submit_expense = st.form_submit_button(
        "Save Expense",
        use_container_width=True
    )


if submit_expense:

    if amount > 0 and description.strip() != "":

        save_expense(
            str(expense_date),
            description,
            amount,
            expense_category,
            payment_mode
        )

        st.success("✅ Expense saved successfully!")

    else:

        st.warning(
            "Please enter description and amount."
        )


# --------------------------------------------------
# EXPENSE HISTORY
# --------------------------------------------------

st.subheader("📋 Expense History")

expense_history = get_expenses()

if not expense_history.empty:

    st.dataframe(
        expense_history,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No individual expenses added yet.")


# --------------------------------------------------
# MONTHLY HISTORY
# --------------------------------------------------

st.subheader("📅 Monthly Finance History")

monthly_history = get_monthly_history()

if not monthly_history.empty:

    st.dataframe(
        monthly_history,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# SPENDING TREND
# --------------------------------------------------

st.subheader("📈 Spending Trend")

if len(monthly_history) >= 2:

    fig, ax = plt.subplots()

    ax.plot(
        monthly_history["month"],
        monthly_history["total_expense"],
        marker="o"
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Total Expense (₹)")
    ax.set_title("Monthly Spending Trend")

    plt.xticks(rotation=45)

    st.pyplot(fig)

else:

    st.info(
        "Calculate finance for at least 2 months "
        "to see the spending trend."
    )


# --------------------------------------------------
# NEXT MONTH EXPENSE PREDICTION
# --------------------------------------------------

st.subheader("🔮 Next Month Expense Prediction")

if len(monthly_history) >= 2:

    y = monthly_history["total_expense"].values

    x = np.arange(len(y))

    # Linear trend model
    coefficients = np.polyfit(x, y, 1)

    next_month_index = len(y)

    predicted_expense = np.polyval(
        coefficients,
        next_month_index
    )

    predicted_expense = max(
        0,
        predicted_expense
    )

    st.metric(
        "Predicted Next Month Expense",
        f"₹{predicted_expense:,.0f}"
    )

    if predicted_expense > y[-1]:

        st.warning(
            "⚠️ Your predicted expense is increasing."
        )

    else:

        st.success(
            "✅ Your predicted expense is stable/decreasing."
        )

else:

    st.info(
        "At least 2 months of data are required "
        "for prediction."
    )


# --------------------------------------------------
# PERSONALIZED RECOMMENDATIONS
# --------------------------------------------------

st.subheader("💡 Personalized Recommendations")

if calculate:

    recommendations = []

    if savings_rate < 10:
        recommendations.append(
            "Try to increase your monthly savings."
        )

    if expense_ratio > 85:
        recommendations.append(
            "Your expenses are high compared to your income."
        )

    if highest_percentage > 40:
        recommendations.append(
            f"{highest_category} is your highest spending category. "
            "Consider setting a budget for it."
        )

    if savings_rate >= 20:
        recommendations.append(
            "Great job! Your savings rate is healthy."
        )

    if not recommendations:

        recommendations.append(
            "Your finances look balanced. Keep monitoring your spending."
        )

    for recommendation in recommendations:

        st.write(
            "👉 " + recommendation
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Personal Finance Intelligence | "
    "Data Science Final Year Project"
)