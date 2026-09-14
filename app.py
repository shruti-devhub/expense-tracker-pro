# app.py - Website Version - Shruti Mishra
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from collections import defaultdict

st.set_page_config(page_title="Expense Tracker - Shruti", page_icon="💰", layout="wide")

# Dark Theme CSS
st.markdown("""
<style>
.stApp {background-color: #0F0F10;}
div[data-testid="stMetric"] {background-color: #1C1C1E; border: 1px solid #2C2C2E; padding: 15px; border-radius: 12px;}
div[data-testid="stMetricLabel"] {color: #8E8E93;}
div[data-testid="stMetricValue"] {color: #FFFFFF;}
</style>
""", unsafe_allow_html=True)

DB_NAME = "expense.db"
conn = sqlite3.connect(DB_NAME)
conn.execute('''CREATE TABLE IF NOT EXISTS expenses
            (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, category TEXT, amount REAL, note TEXT)''')
conn.commit(); conn.close()

st.title("💰 EXPENSE TRACKER - Dark Pro")
st.caption("SHRUTI MISHRA • NIELIT LKO • S GRADE • Reg: NIELIT/LKO/IC/Q11/39701")

# Fetch Data
con = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM expenses ORDER BY id DESC", con)
con.close()

total = df['amount'].sum() if not df.empty else 0
cat = df.groupby('category')['amount'].sum() if not df.empty else {}

# Dashboard
c1, c2, c3, c4 = st.columns(4)
c1.metric("TOTAL SPENT", f"₹ {total:,.0f}", f"{len(df)} Transactions")
c2.metric("FOOD", f"₹ {cat.get('Food',0):,.0f}")
c3.metric("SHOPPING", f"₹ {cat.get('Shopping',0):,.0f}")
c4.metric("TRAVEL", f"₹ {cat.get('Travel',0):,.0f}")

st.divider()

# Add Form
with st.form("add_form"):
    col1, col2, col3, col4 = st.columns(4)
    date = col1.text_input("DATE (DD-MM-YYYY)", datetime.now().strftime("%d-%m-%Y"))
    category = col2.selectbox("CATEGORY", ["Food","Travel","Shopping","Study","Other"])
    amount = col3.number_input("AMOUNT", min_value=1.0, step=10.0)
    note = col4.text_input("NOTE", placeholder="Chai at canteen")
    submitted = st.form_submit_button("ADD EXPENSE →", use_container_width=True, type="primary")
    if submitted:
        con = sqlite3.connect(DB_NAME)
        con.execute("INSERT INTO expenses (date, category, amount, note) VALUES (?,?,?,?)", (date, category, amount, note))
        con.commit(); con.close()
        st.success("Added!"); st.rerun()
# --- NEW USER KE LIYE 0 SE START KARNE KA BUTTON ---
if st.button("🗑️ Clear All & Start from 0"):
    con = sqlite3.connect(DB_NAME)
    con.execute("DELETE FROM expenses")
    con.commit()
    con.close()
    st.success("Sab clear! Ab new user 0 se start kar sakta hai")
    st.rerun()
# Table
st.subheader("Recent Transactions")
if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "expenses.csv", "text/csv")
else:
    st.info("There is no any kharcha", add from top.")
