
import streamlit as st

st.set_page_config(page_title="Landed Cost Calculator", layout="wide")
st.title("LR Paris: Calculate Selling Price by Landed Cost")

# Discount dictionaries
codes_dict_top = {
    "A": 0.5, "B": 0.45, "C": 0.4, "D": 0.35, "E": 0.3,
    "F": 0.25, "G": 0.2, "H": 0.15, "I": 0.1, "J": 0.05, "X": 0.0
}
codes_dict_bottom = {
    "L": 0.7, "M": 0.65, "N": 0.6, "O": 0.55, "P": 0.5,
    "Q": 0.45, "R": 0.4, "S": 0.35, "T": 0.3, "U": 0.25,
    "V": 0.2, "W": 0.15, "Y": 0.1, "Z": 0.05, "Z*": 0.0
}

# Input fields without form
col1, col2, col3 = st.columns(3)

with col1:
    cost = st.number_input("Landed Cost (per unit, USD)", value=0.0, step=0.01)
    run_charge = st.number_input("Run Charge (USD per unit)", value=0.0, step=0.01)

with col2:
    quantity = st.number_input("Quantity", value=1, min_value=1, step=1)
    shipping = st.number_input("Shipping Total (USD)", value=0.0, step=0.01)

with col3:
    sample_cost = st.number_input("Sample Cost (USD)", value=0.0, step=0.01)
    setup_cost = st.number_input("Setup Cost (USD)", value=0.0, step=0.01)
    code_top = st.selectbox("Top Discount Code", list(codes_dict_top.keys()))
    code_bottom = st.selectbox("Bottom Discount Code", list(codes_dict_bottom.keys()))

# Ensure all values are usable
cost = cost or 0.0
run_charge = run_charge or 0.0
quantity = quantity or 1
shipping = shipping or 0.0
sample_cost = sample_cost or 0.0
setup_cost = setup_cost or 0.0

# Get discounts
discount_top = codes_dict_top.get(code_top, 0.0)
discount_bottom = codes_dict_bottom.get(code_bottom, 0.0)

# Safe calculations
try:
    total_cost = (cost + run_charge) * quantity + shipping + sample_cost + setup_cost
    unit_cost = total_cost / quantity
    net_cost = unit_cost / (1 - discount_bottom) if (1 - discount_bottom) != 0 else 0
    selling_price = net_cost / (1 - discount_top) if (1 - discount_top) != 0 else 0
except Exception as e:
    st.error(f"Calculation failed: {e}")
    total_cost = unit_cost = net_cost = selling_price = 0.0

# Output
st.markdown("### Results")
st.metric("Total Cost (All In)", f"${total_cost:.2f}")
st.metric("Unit Cost", f"${unit_cost:.2f}")
st.metric("Net Cost", f"${net_cost:.2f}")
st.metric("Selling Price", f"${selling_price:.2f}")
