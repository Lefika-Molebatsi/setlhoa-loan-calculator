import streamlit as st
import numpy_financial as npf
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Setlhoa Cash Solutions - Loan Calculator",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Setlhoa Cash Solutions")
st.subheader("Pawn & Loan Calculator")
st.write("Calculate monthly installments, tier rules, and repayment schedules.")

st.markdown("---")

# --- USER INPUTS ---
col1, col2 = st.columns(2)

with col1:
    is_vehicle = st.checkbox("🚗 Pawn & Park (Vehicle Loan)", value=False)
    principal = st.number_input(
        "Loan Amount (BWP):", 
        min_value=100, 
        max_value=100000, 
        value=3500, 
        step=100
    )

# --- TIER LOGIC & DETERMINATION ---
if is_vehicle:
    tier_name = "Tier 4: Vehicle Pawn & Park"
    rate = 0.15  # 15% flat rate per month
    min_months = 1
    max_months = 1  # Issued as 30-day renewable contract
    rate_type = "Flat Monthly + Storage"
else:
    if principal < 3500:
        tier_name = "Tier 1: Micro Loan"
        rate = 0.30  # 30% flat rate
        min_months = 1
        max_months = 1
        rate_type = "Flat Rate (30 Days)"
    elif 3500 <= principal <= 10000:
        tier_name = "Tier 2: Medium Loan"
        rate = 0.15  # 15% amortized
        min_months = 2
        max_months = 3
        rate_type = "Monthly Amortized"
    elif 10100 <= principal <= 20000:
        tier_name = "Tier 3: Major Loan"
        rate = 0.10  # 10% amortized
        min_months = 3
        max_months = 6
        rate_type = "Monthly Amortized"
    else:
        tier_name = "Custom / Special Capital Tier"
        rate = 0.10
        min_months = 1
        max_months = 12
        rate_type = "Monthly Amortized"

with col2:
    if min_months == max_months:
        term_months = st.number_input("Loan Term (Months):", value=min_months, disabled=True)
    else:
        term_months = st.slider("Loan Term (Months):", min_value=min_months, max_value=max_months, value=min_months)

# --- DISPLAY TIER SUMMARY ---
st.info(f"**Applied Structure:** {tier_name} | **Rate:** {rate * 100:.1f}% ({rate_type})")

# --- CALCULATION ENGINE ---
st.markdown("---")
st.header("📊 Repayment Breakdown")

if is_vehicle:
    monthly_interest = principal * rate
    st.metric(label="Monthly Interest Due", value=f"P {monthly_interest:,.2f}")
    st.write("**Note:** Storage fees (e.g., P500/month) are billed separately. Renewable for up to 3 extensions (90 days).")

elif tier_name == "Tier 1: Micro Loan":
    total_interest = principal * rate
    total_due = principal + total_interest
    
    col_a, col_b = st.columns(2)
    col_a.metric(label="Total Interest (30 Days)", value=f"P {total_interest:,.2f}")
    col_b.metric(label="Total Payoff Due (Day 30)", value=f"P {total_due:,.2f}")

else:
    # Monthly Amortized Calculation (PMT)
    pmt = npf.pmt(rate, term_months, -principal)
    total_repaid = pmt * term_months
    total_interest = total_repaid - principal
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label="Monthly Installment", value=f"P {pmt:,.2f}")
    col_b.metric(label="Total Interest Earned", value=f"P {total_interest:,.2f}")
    col_c.metric(label="Total Amount Repaid", value=f"P {total_repaid:,.2f}")
    
    # Amortization Table
    st.subheader("📅 Month-by-Month Schedule")
    schedule = []
    balance = principal
    
    for month in range(1, term_months + 1):
        interest_payment = balance * rate
        principal_payment = pmt - interest_payment
        balance -= principal_payment
        schedule.append({
            "Month": month,
            "Installment (BWP)": f"P {pmt:,.2f}",
            "Principal Paid": f"P {principal_payment:,.2f}",
            "Interest Paid": f"P {interest_payment:,.2f}",
            "Remaining Balance": f"P {max(0, balance):,.2f}"
        })
    
    df = pd.DataFrame(schedule)
    st.dataframe(df, use_container_width=True)

st.caption("Setlhoa Cash Solutions © Internal Pawn Calculator")
