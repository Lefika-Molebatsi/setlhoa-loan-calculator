from datetime import date, timedelta
import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Setlhoa Cash Solutions - Pawn Calculator",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Setlhoa Cash Solutions")
st.subheader("Pawn & Loan Valuation Calculator")
st.write("Determine maximum loan offers based on item valuation and view 30-day repayment schedules.")

st.markdown("---")

# --- USER INPUTS ---
is_vehicle = st.checkbox("🚗 Pawn & Park (Vehicle Loan)", value=False)

col1, col2 = st.columns(2)

with col1:
    item_type = "Vehicle" if is_vehicle else st.selectbox(
        "Asset Category:",
        ["Electronics", "Furniture", "Machinery", "General Goods"]
    )
    
    second_hand_value = st.number_input(
        "2nd Hand Value of Item (BWP):", 
        min_value=100, 
        max_value=500000, 
        value=10000, 
        step=500
    )

# --- 40% LTV LOAN CALCULATION ---
ltv_rate = 0.40
loan_amount = second_hand_value * ltv_rate

with col2:
    st.metric(
        label="Calculated Loan Amount (40% LTV)", 
        value=f"P {loan_amount:,.2f}"
    )

# --- INTEREST LOGIC ---
if is_vehicle:
    interest_rate = 0.15  # 15% flat for cars
    tier_label = "Vehicle Pawn & Park (15% Monthly)"
else:
    interest_rate = 0.30  # 30% flat for electronics, furniture, machinery
    tier_label = f"Standard Pawn - {item_type} (30% Monthly)"

# --- REPAYMENT BREAKDOWN ---
st.markdown("---")
st.header("📊 Repayment Breakdown")
st.info(f"**Applied Asset Rule:** {tier_label}")

# Calculate financials and due date (30 days from today)
interest_due = loan_amount * interest_rate
total_payoff = loan_amount + interest_due
due_date = date.today() + timedelta(days=30)
formatted_due_date = due_date.strftime("%d %B %Y")

# Create 4 display columns instead of 3
col_a, col_b, col_c, col_d = st.columns(4)

col_a.metric(label="Loan Principal", value=f"P {loan_amount:,.2f}")
col_b.metric(label="Total Interest (30 Days)", value=f"P {interest_due:,.2f}")
col_c.metric(label="Total Payoff Due (Day 30)", value=f"P {total_payoff:,.2f}")
col_d.metric(label="Exact Due Date", value=formatted_due_date)

st.markdown("---")

# --- EXTENSION POLICY & OPERATIONAL RULES ---

# --- EXTENSION POLICY & OPERATIONAL RULES ---
st.subheader("📌 Loan Renewal & Extension Policy")

if is_vehicle:
    st.warning(
        f"**Vehicle Extension Rule:** To extend for an additional 30 days, the customer must pay **P {interest_due:,.2f}** (15% interest) + applicable monthly storage fees. "
        "Interest-only extensions permitted for a maximum of 3 renewals (90 days total)."
    )
else:
    st.warning(
        f"**Standard Extension Rule:** To extend for an additional 30 days, the customer must pay **P {interest_due:,.2f}** (30% interest fee). "
        "Extensions do not reduce the principal balance."
    )

st.caption("Setlhoa Cash Solutions © Valuation & Pawn Calculator")
