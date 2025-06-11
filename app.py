
import streamlit as st

st.set_page_config(page_title="Selling Price Calculator", layout="wide")
st.title("LR Paris: Selling Price Calculator")

# Inputs
col1, col2, col3 = st.columns(3)

with col1:
    unit_cost = st.number_input("Unit Cost (USD)", min_value=0.0, step=0.01)
    margin_pct = st.number_input("Desired Margin (%)", min_value=0.0, step=0.5)

with col2:
    quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
    shipping = st.number_input("Shipping Total (USD)", min_value=0.0, step=0.01)
    run_charge = st.number_input("Run Charge (USD per unit)", min_value=0.0, step=0.01)

with col3:
    sample = st.number_input("Sample Cost (USD)", min_value=0.0, step=0.01)
    setup = st.number_input("Setup Cost (USD)", min_value=0.0, step=0.01)

# Convert margin
margin = margin_pct / 100

# Calculate optional fields per unit
shipping_per_unit = shipping / quantity if quantity else 0.0
setup_per_unit = setup / quantity if quantity else 0.0
sample_per_unit = sample / quantity if quantity else 0.0

# Landed unit cost = unit cost + all optional unit-level add-ons
landed_unit_cost = unit_cost + run_charge + shipping_per_unit + setup_per_unit + sample_per_unit

# Selling price calculation
selling_price = landed_unit_cost / (1 - margin) if (1 - margin) != 0 else 0.0

# Total revenue and profit
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
