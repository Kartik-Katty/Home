import streamlit as st
from datetime import datetime

def calculate_maintenance(area, move_in_month, move_in_year):
    rate_old = 5
    rate_new = 3.95
    full_year_months = 12

    # Total base maintenance paid (no GST)
    total_maintenance_paid = area * rate_old * full_year_months

    # Build list of 12 months from move-in
    months_covered = []
    month = move_in_month
    year = move_in_year

    for _ in range(full_year_months):
        months_covered.append((month, year))
        month += 1
        if month > 12:
            month = 1
            year += 1

    # Calculate how much was used at ₹5 rate
    used_amount = 0
    for m, y in months_covered:
        if y < 2025 or (y == 2025 and m < 4):
            used_amount += area * rate_old
        else:
            break  # From April 2025, only ₹3.95 rates apply

    remaining_balance = total_maintenance_paid - used_amount

    # From April 2025 onward, how many months are free?
    start_index = next((i for i, (m, y) in enumerate(months_covered) if y > 2025 or (y == 2025 and m >= 4)), None)

    if start_index is not None:
        current_month = months_covered[start_index][0]
        current_year = months_covered[start_index][1]
    else:
        current_month = 4
        current_year = 2025

    months_free = 0
    while remaining_balance >= area * rate_new:
        remaining_balance -= area * rate_new
        months_free += 1
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1

    # Determine next quarter
    quarter_month = ((current_month - 1) // 3) * 3 + 1
    quarter_months = [quarter_month, quarter_month + 1, quarter_month + 2]
    quarter_label = f"{datetime(current_year, quarter_months[0], 1).strftime('%b')}–{datetime(current_year, quarter_months[-1], 1).strftime('%b')} {current_year}"
    quarter_base = rate_new * area * 3

    # Subtract any remaining balance from quarter bill
    quarter_payable = max(quarter_base - remaining_balance, 0)

    return {
        "base_amount": total_maintenance_paid,
        "used_amount": used_amount,
        "remaining_balance": remaining_balance,
        "months_free": months_free,
        "next_due_month": current_month,
        "next_due_year": current_year,
        "quarter_label": quarter_label,
        "quarter_base": quarter_base,
        "quarter_payable": quarter_payable
    }

# --- Streamlit UI ---
st.title("🏢 Maintenance Coverage Calculator")

area = st.number_input("Enter your apartment size (sq. ft):", min_value=100, max_value=10000, value=1410)

move_in_month = st.selectbox(
    "Select your move-in month:",
    list(range(1, 13)),
    format_func=lambda x: datetime(2025, x, 1).strftime('%B')
)

move_in_year = st.number_input("Enter your move-in year:", min_value=2020, max_value=2030, value=2025)

if st.button("Calculate"):
    result = calculate_maintenance(area, move_in_month, move_in_year)

    st.subheader("🔍 Maintenance Summary")
    st.write(f"**Total Maintenance Paid:** ₹{result['base_amount']:.2f}")
    st.write(f"• Used till March 2025 (if applicable): ₹{result['used_amount']:.2f}")
    st.write(f"• Remaining Balance: ₹{result['remaining_balance']:.2f}")
    st.write(f"• Covers ≈ {result['months_free']} full month(s) post-April 2025 at ₹3.95/sqft")

    readable_month = datetime(result['next_due_year'], result['next_due_month'], 1).strftime('%B %Y')
    st.success(f"✅ Next maintenance due from: **{readable_month}**")

    st.info(
        f"🧾 **Quarterly Maintenance ({result['quarter_label']}):**\n"
        f"• Quarter Base: ₹{result['quarter_base']:.2f}\n"
        f"• Minus Remaining Balance: ₹{result['remaining_balance']:.2f}\n"
        f"👉 **You Need to Pay: ₹{result['quarter_payable']:.2f}**"
    )
