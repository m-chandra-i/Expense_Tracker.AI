import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

st.set_page_config(page_title="Money Tracker AI", page_icon="💸", layout="wide")

DATA_FILE = Path("expenses.csv")

if not DATA_FILE.exists():
    df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Note"])
    df.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(data):
    data.to_csv(DATA_FILE, index=False)

st.title("Money Tracker AI")
st.write("Track your income, expenses, savings, and spending habits.")

data = load_data()

st.sidebar.header("Add Transaction")

transaction_type = st.sidebar.selectbox("Transaction Type", ["Expense", "Income"])
category = st.sidebar.selectbox(
    "Category",
    ["Food", "Travel", "Shopping", "Bills", "Salary", "Education", "Health", "Other"]
)
amount = st.sidebar.number_input("Amount", min_value=0.0, step=10.0)
note = st.sidebar.text_input("Note")
transaction_date = st.sidebar.date_input("Date", date.today())

if st.sidebar.button("Add Transaction"):
    if amount > 0:
        new_data = pd.DataFrame(
            [[transaction_date, transaction_type, category, amount, note]],
            columns=["Date", "Type", "Category", "Amount", "Note"]
        )
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)
        st.sidebar.success("Transaction added successfully!")
        st.rerun()
    else:
        st.sidebar.error("Please enter a valid amount.")

st.subheader("Dashboard")

income = data[data["Type"] == "Income"]["Amount"].sum()
expense = data[data["Type"] == "Expense"]["Amount"].sum()
balance = income - expense

col1, col2, col3 = st.columns(3)

col1.metric("Total Income", f"₹{income:.2f}")
col2.metric("Total Expense", f"₹{expense:.2f}")
col3.metric("Balance", f"₹{balance:.2f}")

st.subheader("All Transactions")
st.dataframe(data, use_container_width=True)

if not data.empty:
    st.subheader("Expense by Category")

    expense_data = data[data["Type"] == "Expense"]

    if not expense_data.empty:
        category_data = expense_data.groupby("Category")["Amount"].sum()
        st.bar_chart(category_data)

        highest_category = category_data.idxmax()
        highest_amount = category_data.max()

        st.subheader("AI Money Saving Tip")

        if highest_amount > 0:
            st.info(
                f"You are spending the most on {highest_category}. "
                f"Try to reduce unnecessary spending in this category to save more money."
            )
    else:
        st.info("No expense data available yet.")

st.subheader("Delete All Data")

if st.button("Clear All Transactions"):
    empty_data = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Note"])
    save_data(empty_data)
    st.success("All transactions deleted.")
    st.rerun()
