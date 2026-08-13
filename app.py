import numpy_financial as npf
import streamlit as st

st.set_page_config(
    page_title="Setlhoa Cash Solutions - Loan Calculator",
    page_icon="💰",
    layout="centered",
)

st.title("💰 Setlhoa Cash Solutions")
st.subheader("Interactive Loan & Amortization Calculator")

# Customer Inputs
principal = st.number_input(
    "Loan Principal (Pula):",
    min_value=1000,
    max_value=50000,
    value=5000,
    step=500,
)
term = st.number_input(
    "Repayment Term (Months):", min_value=1, max_value=9, value=3, step=1
)

# Tier Matrix Logic
if principal < 3000:
  tier = "Tier 1: Short Term (30 Days)"
  rate = 0.30
elif principal <= 10000:
  tier = "Tier 2: Medium Term (2–5 Months)"
  rate = 0.15
else:
  tier = "Tier 3: Long Term (6–9 Months)"
  rate = 0.075

# Calculation
if term == 1:
  monthly_pmt = principal * (1 + rate)
  total_repayment = monthly_pmt
else:
  monthly_pmt = -npf.pmt(rate, term, principal)
  total_repayment = monthly_pmt * term

total_profit = total_repayment - principal

# Output Display
st.markdown("---")
st.write(f"**Applied Tier:** {tier}")
st.write(f"**Monthly Interest Rate:** {rate*100:.1f}%")

col1, col2, col3 = st.columns(3)
col1.metric("Monthly Payment", f"P {monthly_pmt:,.2f}")
col2.metric("Total Repayment", f"P {total_repayment:,.2f}")
col3.metric("Total Profit", f"P {total_profit:,.2f}")
