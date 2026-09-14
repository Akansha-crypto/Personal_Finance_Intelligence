import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Personal Finance Intelligence",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Finance Intelligence")
st.caption("Track • Analyze • Predict • Improve Your Finances")

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "monthly_history" not in st.session_state:
    st.session_state.monthly_history = []

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("📌 Finance Input")

income = st.sidebar.number_input(
    "Monthly Income (₹)",
    min_value=0.0,
    value=30000.0,
    step=500.0
)

st.sidebar.subheader("💸 Category-wise Expenses")

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
        f"{category} (₹)",
        min_value=0.0,
        value=0.0,
        step=100.0
    )

calculate = st.sidebar.button(
    "🔍 Calculate Finance",
    use_container_width=True
)

# ---------------------------------------------------
# CALCULATE CURRENT FINANCE
# ---------------------------------------------------

if calculate:

    total_expense = sum(category_expenses.values())
    balance = income - total_expense

    if income > 0:
        savings_rate = (balance / income) * 100
    else:
        savings_rate = 0

    # Save monthly record
    monthly_record = {
        "Date": str(date.today()),
        "Income": income,
        "Expense": total_expense,
        "Balance": balance
    }

    st.session_state.monthly_history.append(monthly_record)

    st.success("✅ Finance calculated successfully!")

else:

    total_expense = sum(category_expenses.values())
    balance = income - total_expense

    if income > 0:
        savings_rate = (balance / income) * 100
    else:
        savings_rate = 0


# ---------------------------------------------------
# TOP METRICS
# ---------------------------------------------------

st.header("📊 Financial Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Monthly Income",
    f"₹{income:,.0f}"
)

col2.metric(
    "💸 Total Expense",
    f"₹{total_expense:,.0f}"
)

col3.metric(
    "🏦 Remaining Balance",
    f"₹{balance:,.0f}"
)

col4.metric(
    "📈 Savings Rate",
    f"{savings_rate:.1f}%"
)


# ---------------------------------------------------
# FINANCIAL HEALTH SCORE
# ---------------------------------------------------

st.header("❤️ Financial Health")

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

# Expense ratio
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

    concentration = (
        highest_amount / total_expense
    ) * 100

    if concentration <= 25:
        score += 20
    elif concentration <= 40:
        score += 10
    else:
        score += 5
else:
    highest_category = "None"
    highest_amount = 0
    concentration = 0

# Positive balance
if balance > 0:
    score += 10

if score >= 80:
    health_status = "Excellent 🟢"
elif score >= 60:
    health_status = "Good 🟢"
elif score >= 40:
    health_status = "Average 🟡"
else:
    health_status = "Poor 🔴"


health_col1, health_col2 = st.columns(2)

health_col1.metric(
    "Financial Health Score",
    f"{score}/100"
)

health_col2.metric(
    "Financial Status",
    health_status
)


# ---------------------------------------------------
# CATEGORY ANALYSIS
# ---------------------------------------------------

st.header("📊 Spending Analysis")

expense_df = pd.DataFrame(
    list(category_expenses.items()),
    columns=["Category", "Amount"]
)

expense_df = expense_df[
    expense_df["Amount"] > 0
]

if not expense_df.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Category-wise Expenses")

        fig, ax = plt.subplots()

        ax.bar(
            expense_df["Category"],
            expense_df["Amount"]
        )

        ax.set_xlabel("Category")
        ax.set_ylabel("Expense (₹)")
        ax.set_title("Expense by Category")

        plt.xticks(rotation=45)

        st.pyplot(fig)

    with col2:

        st.subheader("Expense Distribution")

        fig2, ax2 = plt.subplots()

        ax2.pie(
            expense_df["Amount"],
            labels=expense_df["Category"],
            autopct="%1.1f%%"
        )

        ax2.set_title("Expense Distribution")

        st.pyplot(fig2)

else:

    st.info(
        "Enter your expenses from the sidebar to see spending analysis."
    )


# ---------------------------------------------------
# INDIVIDUAL EXPENSE ENTRY
# ---------------------------------------------------

st.header("➕ Add Individual Expense")

with st.form("expense_form"):

    col1, col2 = st.columns(2)

    with col1:

        expense_date = st.date_input(
            "Date",
            value=date.today()
        )

        description = st.text_input(
            "Description",
            placeholder="Example: Swiggy"
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=50.0
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
                "Debit Card",
                "Credit Card",
                "Bank Transfer"
            ]
        )

    add_expense = st.form_submit_button(
        "➕ Add Expense"
    )

    if add_expense:

        if amount > 0:

            new_expense = {
                "Date": expense_date,
                "Description": description,
                "Amount": amount,
                "Category": expense_category,
                "Payment_Mode": payment_mode
            }

            st.session_state.expenses.append(
                new_expense
            )

            st.success(
                "✅ Expense added successfully!"
            )

        else:

            st.warning(
                "Please enter an amount greater than 0."
            )


# ---------------------------------------------------
# EXPENSE HISTORY
# ---------------------------------------------------

if st.session_state.expenses:

    st.header("📋 Expense History")

    history_df = pd.DataFrame(
        st.session_state.expenses
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

    individual_total = history_df["Amount"].sum()

    st.metric(
        "Total Individual Expenses",
        f"₹{individual_total:,.0f}"
    )


# ---------------------------------------------------
# SPENDING TREND
# ---------------------------------------------------

st.header("📈 Spending Trend")

if len(st.session_state.monthly_history) >= 2:

    history = pd.DataFrame(
        st.session_state.monthly_history
    )

    fig3, ax3 = plt.subplots()

    ax3.plot(
        history["Date"],
        history["Expense"],
        marker="o"
    )

    ax3.set_xlabel("Date")
    ax3.set_ylabel("Expense (₹)")
    ax3.set_title("Expense Trend")

    plt.xticks(rotation=45)

    st.pyplot(fig3)

else:

    st.info(
        "Calculate finance for at least 2 months to see your spending trend."
    )


# ---------------------------------------------------
# NEXT MONTH EXPENSE PREDICTION
# ---------------------------------------------------

st.header("🤖 Next Month Expense Prediction")

if len(st.session_state.monthly_history) >= 2:

    history = pd.DataFrame(
        st.session_state.monthly_history
    )

    expenses = history["Expense"].values

    # Simple trend-based prediction
    x = np.arange(len(expenses))

    slope, intercept = np.polyfit(
        x,
        expenses,
        1
    )

    next_month = slope * len(expenses) + intercept

    next_month = max(
        0,
        next_month
    )

    st.success(
        f"🔮 Predicted Next Month Expense: ₹{next_month:,.0f}"
    )

    last_expense = expenses[-1]

    if next_month > last_expense:

        st.warning(
            "⚠️ Your predicted expenses may increase next month."
        )

    else:

        st.info(
            "✅ Your predicted expenses may remain stable or decrease."
        )

else:

    st.info(
        "Enter and calculate finance for at least 2 months to generate a prediction."
    )


# ---------------------------------------------------
# SPENDING TREND INSIGHT
# ---------------------------------------------------

st.header("📌 Spending Trend Insight")

if len(st.session_state.monthly_history) >= 2:

    history = pd.DataFrame(
        st.session_state.monthly_history
    )

    first_expense = history["Expense"].iloc[0]
    last_expense = history["Expense"].iloc[-1]

    if last_expense > first_expense:

        percentage_change = (
            (last_expense - first_expense)
            / first_expense
            * 100
        )

        st.warning(
            f"📈 Your expenses increased by "
            f"{percentage_change:.1f}%."
        )

    elif last_expense < first_expense:

        percentage_change = (
            (first_expense - last_expense)
            / first_expense
            * 100
        )

        st.success(
            f"📉 Your expenses decreased by "
            f"{percentage_change:.1f}%."
        )

    else:

        st.info(
            "➡️ Your expenses are approximately stable."
        )

else:

    st.info(
        "More monthly data is required for trend analysis."
    )


# ---------------------------------------------------
# UNUSUAL EXPENSE DETECTION
# ---------------------------------------------------

st.header("🚨 Unusual Expense Detection")

if st.session_state.expenses:

    history_df = pd.DataFrame(
        st.session_state.expenses
    )

    mean_expense = history_df["Amount"].mean()
    std_expense = history_df["Amount"].std()

    if std_expense > 0:

        unusual = history_df[
            history_df["Amount"]
            > mean_expense + (2 * std_expense)
        ]

        if not unusual.empty:

            st.warning(
                "⚠️ These expenses are unusually high:"
            )

            st.dataframe(
                unusual,
                use_container_width=True
            )

        else:

            st.success(
                "✅ No unusually high expenses detected."
            )

    else:

        st.info(
            "Add more individual expenses for anomaly detection."
        )

else:

    st.info(
        "Add individual expenses to detect unusual spending."
    )


# ---------------------------------------------------
# PERSONALIZED RECOMMENDATIONS
# ---------------------------------------------------

st.header("💡 Personalized Financial Recommendations")

recommendations = []

if savings_rate < 10:

    recommendations.append(
        "💰 Try to increase your savings rate to at least 10%."
    )

elif savings_rate >= 20:

    recommendations.append(
        "🎉 Great! Your savings rate is healthy."
    )

if highest_category != "None":

    if concentration > 40:

        recommendations.append(
            f"⚠️ {highest_category} is taking "
            f"{concentration:.1f}% of your total expenses. "
            "Consider reducing this category."
        )

if category_expenses["Shopping"] > 0:

    if total_expense > 0 and (
        category_expenses["Shopping"]
        / total_expense
        * 100
    ) > 15:

        recommendations.append(
            "🛍️ Shopping expenses are relatively high. "
            "Consider setting a monthly shopping limit."
        )

if category_expenses["Entertainment"] > 0:

    if total_expense > 0 and (
        category_expenses["Entertainment"]
        / total_expense
        * 100
    ) > 10:

        recommendations.append(
            "🎬 Consider reducing entertainment expenses."
        )

if category_expenses["Food"] > 0:

    if total_expense > 0 and (
        category_expenses["Food"]
        / total_expense
        * 100
    ) > 15:

        recommendations.append(
            "🍔 Food expenses are relatively high. "
            "Try setting a weekly food budget."
        )

if balance < 0:

    recommendations.append(
        "🚨 Your expenses are higher than your income. "
        "Reduce non-essential spending."
    )

if not recommendations:

    recommendations.append(
        "✅ Your current spending pattern looks reasonable. "
        "Continue tracking your expenses regularly."
    )

for recommendation in recommendations:

    st.write(
        "• " + recommendation
    )


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Personal Finance Intelligence System | "
    "Data Science Final Year Project"
)