import streamlit as st
from datetime import datetime

st.title("🏢 Maintenance Calculator")

# Inputs
area = st.number_input("📐 Enter apartment area (in sq ft)", min_value=100, max_value=10000, value=1410)
move_in_month = st.selectbox("📅 Select move-in month", 
                             options=["January", "February", "March", "April", "May", "June", 
                                      "July", "August", "September", "October", "November", "December"])
move_in_year = st.number_input("📆 Enter move-in year", min_value=2020, max_value=2030, value=2025)

if st.button("🔍 Calculate"):
    month_mapping = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }
    move_in_month_num = month_mapping[move_in_month]

    # Rates
    rate_old = 5.00
    rate_new = 3.95
    monthly_cost_old = area * rate_old
    monthly_cost_new = area * rate_new

    # Dates
    changeover_month = 4
    changeover_year = 2025
    changeover_date = datetime(changeover_year, changeover_month, 1)
    start_date = datetime(move_in_year, move_in_month_num, 1)

    # Total paid for 12 months at old rate
    total_paid = area * rate_old * 12

    # Calculate number of months from move-in to March 2025
    march_2025 = datetime(2025, 3, 1)
    used_months = 0
    for i in range(12):
        month = (move_in_month_num + i - 1) % 12 + 1
        year = move_in_year + (move_in_month_num + i - 1) // 12
        curr_date = datetime(year, month, 1)
        if curr_date <= march_2025:
            used_months += 1
        else:
            break

    used_amount = used_months * monthly_cost_old
    remaining_balance = total_paid - used_amount
    remaining_balance = max(0, remaining_balance)

    # From April 2025, how many months can this balance cover at ₹3.95/sqft?
    months_covered = int(remaining_balance // monthly_cost_new)

    # Next maintenance due date
    next_due_month = 4 + months_covered
    next_due_year = 2025 + (next_due_month - 1) // 12
    next_due_month = (next_due_month - 1) % 12 + 1
    next_due_date = datetime(next_due_year, next_due_month, 1)

    # Quarterly calculations
    def get_quarter_label(month):
        if month in [1, 2, 3]:
            return "Q1 (Jan–Mar)"
        elif month in [4, 5, 6]:
            return "Q2 (Apr–Jun)"
        elif month in [7, 8, 9]:
            return "Q3 (Jul–Sep)"
        else:
            return "Q4 (Oct–Dec)"

    quarter_label = get_quarter_label(next_due_month)
    quarter_base = monthly_cost_new * 3
    quarter_payable = max(0, quarter_base - remaining_balance)

    readable_month = next_due_date.strftime('%B %Y')

    # Outputs
    st.markdown("---")
    st.success(f"✅ Next maintenance due from: **{readable_month}**")

    st.info(
        f"🧾 **Quarterly Maintenance ({quarter_label}):**\n"
        f"• Quarter Base: ₹{quarter_base:,.2f}\n"
        f"• Minus Remaining Balance: ₹{remaining_balance:,.2f}\n"
        f"👉 **You Need to Pay: ₹{quarter_payable:,.2f}**"
    )

    st.markdown("---")
    st.subheader("📊 Detailed Breakdown")
    st.write(f"• Maintenance paid from **{move_in_month} {move_in_year}** for 12 months: ₹{total_paid:,.2f}")
    st.write(f"• Used till March 2025: ₹{used_amount:,.2f} ({used_months} month(s) × ₹{monthly_cost_old:,.2f})")
    st.write(f"• Remaining balance: ₹{remaining_balance:,.2f}")
    st.write(f"• Covers ≈ {months_covered} month(s) from April 2025 at ₹3.95/sqft")
