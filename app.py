
import streamlit as st

st.set_page_config(page_title="Selling Price Calculator", layout="wide")
st.title("LR Paris: Selling Price Calculator")

# Input fields
col1, col2, col3 = st.columns(3)

with col1:
    unit_cost = st.number_input("Unit Cost (USD)", value=0.0, step=0.01)
    margin_pct = st.number_input("Desired Margin (%)", value=0.0, step=0.5)

with col2:
    quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
    shipping_total = st.number_input("Total Shipping (USD)", value=0.0, step=0.01)

with col3:
    setup_cost = st.number_input("Setup Cost (USD)", value=0.0, step=0.01)
    sample_cost = st.number_input("Sample Cost (USD)", value=0.0, step=0.01)

# Safe value handling
unit_cost = unit_cost or 0.0
margin_pct = margin_pct or 0.0
quantity = quantity or 1
shipping_total = shipping_total or 0.0
setup_cost = setup_cost or 0.0
sample_cost = sample_cost or 0.0

# Add optional costs per unit
extras_total = shipping_total + setup_cost + sample_cost
extras_per_unit = extras_total / quantity if quantity else 0.0
true_unit_cost = unit_cost + extras_per_unit

# Selling price calculation
margin = margin_pct / 100
try:
    selling_price = true_unit_cost / (1 - margin) if (1 - margin) != 0 else 0.0
except:
    selling_price = 0.0

total_revenue = selling_price * quantity
total_cost = true_unit_cost * quantity
profit = total_revenue - total_cost

# Output
st.markdown("### Results")
st.metric("Selling Price (per unit)", f"${selling_price:.2f}")
st.metric("Total Revenue", f"${total_revenue:.2f}")
st.metric("Total Cost", f"${total_cost:.2f}")
st.metric("Profit", f"${profit:.2f}")
