import streamlit as st
from datetime import datetime

# Title
st.title("🏢 Maintenance Calculator")

# Inputs
area = st.number_input("📐 Enter apartment area (in sq ft)", min_value=100, max_value=10000, value=1410)
move_in_month = st.selectbox("📅 Select move-in month", 
                             options=["January", "February", "March", "April", "May", "June", 
                                      "July", "August", "September", "October", "November", "December"])
move_in_year = st.number_input("📆 Enter move-in year", min_value=2020, max_value=2030, value=2025)

if st.button("🔍 Calculate"):
    # Mapping month names to numbers
    month_mapping = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }

    move_in_month_number = month_mapping[move_in_month]

    # Rates
    rate_old = 5.00
    rate_new = 3.95

    # Full maintenance paid in Jan 2025
    total_maintenance_paid = area * rate_old * 12

    # Maintenance used only if move-in is on or before March 2025
    if move_in_year == 2025 and move_in_month_number <= 3:
        used_months = 3 - move_in_month_number + 1  # e.g., Feb => 2 months (Feb, Mar)
    elif move_in_year == 2025 and move_in_month_number > 3:
        used_months = 0  # moved in after March 2025
    else:
        used_months = 3  # default assumption, moved in earlier than 2025

    used_amount = area * rate_old * used_months
    remaining_balance = total_maintenance_paid - used_amount

    # Months covered at new rate
    months_covered = int(remaining_balance // (area * rate_new))

    # Month and year from which payment resumes
    start_month = 4 + months_covered  # Starting from April 2025
    start_year = 2025
    if start_month > 12:
        start_year += (start_month - 1) // 12
        start_month = (start_month - 1) % 12 + 1

    # Base monthly and quarterly maintenance
    monthly_base = area * rate_new
    quarterly_base = monthly_base * 3

    # Payable after subtracting balance
    quarter_payable = quarterly_base - remaining_balance
    if quarter_payable < 0:
        quarter_payable = 0.0

    # Quarter label
    def get_quarter_label(month):
        if month in [1, 2, 3]:
            return "Q1 (Jan–Mar)"
        elif month in [4, 5, 6]:
            return "Q2 (Apr–Jun)"
        elif month in [7, 8, 9]:
            return "Q3 (Jul–Sep)"
        else:
            return "Q4 (Oct–Dec)"

    quarter_label = get_quarter_label(start_month)
    readable_month = datetime(start_year, start_month, 1).strftime('%B %Y')

    # Display
    st.markdown("---")
    st.success(f"✅ Next maintenance due from: **{readable_month}**")

    st.info(
        f"🧾 **Quarterly Maintenance ({quarter_label}):**\n"
        f"• Quarter Base: ₹{quarterly_base:,.2f}\n"
        f"• Minus Remaining Balance: ₹{remaining_balance:,.2f}\n"
        f"👉 **You Need to Pay: ₹{quarter_payable:,.2f}**"
    )

    st.markdown("---")
    st.subheader("📊 Detailed Breakdown")
    st.write(f"• Total maintenance paid in Jan 2025: ₹{total_maintenance_paid:,.2f}")
    st.write(f"• Maintenance used till March 2025: ₹{used_amount:,.2f}")
    st.write(f"• Remaining balance carried forward: ₹{remaining_balance:,.2f}")
    st.write(f"• Covers {months_covered} month(s) from April 2025 at ₹3.95/sqft")
