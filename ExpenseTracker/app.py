import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Expense Tracker", layout="wide")

# ---------------- APP TITLE ----------------
st.title("💰 Expense Tracker Dashboard")

# ---------------- CONSTANTS ----------------
FILE_NAME = "expenses.csv"
COLUMNS = ["Date", "Description", "Amount", "Category"]

# ---------------- SESSION STATE ----------------
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# ---------------- LOAD CSV DATA ----------------
if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
    try:
        df_existing = pd.read_csv(FILE_NAME)
        df_existing["Date"] = pd.to_datetime(df_existing["Date"])
        st.session_state.expenses = df_existing.to_dict("records")
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")

# ---------------- SIDEBAR FORM ----------------
st.sidebar.header("➕ Add New Expense")

with st.sidebar.form("expense_form"):
    date = st.date_input("Date", datetime.today())
    category = st.selectbox(
        "Category", ["Food", "Transport", "Shopping", "Rent", "Bills", "Others"]
    )
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    description = st.text_input("Description")
    submit = st.form_submit_button("Add Expense")

# ---------------- FORM SUBMIT ----------------
if submit:
    if amount > 0 and description.strip():
        entry = {
            "Date": pd.to_datetime(date),
            "Description": description,
            "Amount": amount,
            "Category": category,
        }

        st.session_state.expenses.append(entry)

        # Save to CSV
        df_save = pd.DataFrame([entry])
        df_save.to_csv(
            FILE_NAME,
            mode="a",
            header=not os.path.exists(FILE_NAME),
            index=False,
        )

        st.sidebar.success("✅ Expense Added Successfully")
    else:
        st.sidebar.error("❌ Please enter valid data")

# ---------------- MAIN CONTENT ----------------
df = pd.DataFrame(st.session_state.expenses, columns=COLUMNS)

if not df.empty:
    # 🔑 FIX: normalize Date column (PyArrow safe)
    df["Date"] = pd.to_datetime(df["Date"])

    # ---------------- TABLE ----------------
    st.subheader("📋 Expense List")
    st.dataframe(df, use_container_width=True)

    # ---------------- CHARTS ----------------
    col1, col2 = st.columns(2)

    # -------- Monthly Bar Chart --------
    with col1:
        st.subheader("📊 Monthly Spending")

        df["Month"] = df["Date"].dt.strftime("%B")
        monthly_spending = df.groupby("Month")["Amount"].sum()

        fig1, ax1 = plt.subplots()
        monthly_spending.plot(kind="bar", ax=ax1)
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Amount")
        st.pyplot(fig1)

    # -------- Category Pie Chart --------
    with col2:
        st.subheader("🥧 Category-wise Spending")

        category_spending = df.groupby("Category")["Amount"].sum()

        fig2, ax2 = plt.subplots()
        ax2.pie(
            category_spending,
            labels=category_spending.index,
            autopct="%1.1f%%",
            startangle=90,
        )
        ax2.axis("equal")
        st.pyplot(fig2)

else:
    st.info("ℹ️ No expenses added yet. Use the sidebar to add expenses.")
