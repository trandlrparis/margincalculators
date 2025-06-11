
import streamlit as st

st.set_page_config(page_title="Selling Price Calculator", layout="wide")
st.title("LR Paris: Selling Price Calculator")

# Safe float parser to convert erased fields to 0.0
def safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0

# Inputs
col1, col2, col3 = st.columns(3)

with col1:
    unit_cost = safe_float(st.text_input("Unit Cost (USD)", value="0.00"))
    margin_pct = safe_float(st.text_input("Desired Margin (%)", value="0.00"))

with col2:
    quantity = int(safe_float(st.text_input("Quantity", value="1")))
    shipping = safe_float(st.text_input("Shipping Total (USD)", value="0.00"))
    run_charge = safe_float(st.text_input("Run Charge (USD per unit)", value="0.00"))

with col3:
    sample = safe_float(st.text_input("Sample Cost (USD)", value="0.00"))
    setup = safe_float(st.text_input("Setup Cost (USD)", value="0.00"))

# Convert margin
margin = margin_pct / 100

# Calculate optional fields per unit
shipping_per_unit = shipping / quantity if quantity else 0.0
setup_per_unit = setup / quantity if quantity else 0.0
sample_per_unit = sample / quantity if quantity else 0.0

# Landed unit cost
landed_unit_cost = unit_cost + run_charge + shipping_per_unit + setup_per_unit + sample_per_unit

# Selling price
selling_price = landed_unit_cost / (1 - margin) if (1 - margin) != 0 else 0.0

# Totals
total_revenue = selling_price * quantity
total_cost = landed_unit_cost * quantity
profit = total_revenue - total_cost

# Output
st.markdown("### Results")
col1, col2 = st.columns(2)

with col1:
    st.metric("Landed Unit Cost", f"${landed_unit_cost:.2f}")
    st.metric("Selling Price (per unit)", f"${selling_price:.2f}")

with col2:
    st.metric("Total Revenue", f"${total_revenue:.2f}")
    st.metric("Profit", f"${profit:.2f}")
