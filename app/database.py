import sqlite3
import pandas as pd

DB_NAME = "finance.db"


# Create database and tables
def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Monthly finance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monthly_finance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT,
            income REAL,
            total_expense REAL,
            balance REAL,
            savings_rate REAL
        )
    """)

    # Individual expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            description TEXT,
            amount REAL,
            category TEXT,
            payment_mode TEXT
        )
    """)

    conn.commit()
    conn.close()


# Save monthly finance data
def save_monthly_finance(month, income, total_expense, balance, savings_rate):
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO monthly_finance
        (month, income, total_expense, balance, savings_rate)
        VALUES (?, ?, ?, ?, ?)
    """, (
        month,
        income,
        total_expense,
        balance,
        savings_rate
    ))

    conn.commit()
    conn.close()


# Save individual expense
def save_expense(date, description, amount, category, payment_mode):
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO expenses
        (date, description, amount, category, payment_mode)
        VALUES (?, ?, ?, ?, ?)
    """, (
        date,
        description,
        amount,
        category,
        payment_mode
    ))

    conn.commit()
    conn.close()


# Get monthly finance history
def get_monthly_history():
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM monthly_finance ORDER BY id",
        conn
    )

    conn.close()
    return df


# Get expense history
def get_expenses():
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM expenses ORDER BY id DESC",
        conn
    )

    conn.close()
    return df


# Create database automatically
create_database()