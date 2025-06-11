
import streamlit as st

st.set_page_config(page_title="Selling Price Calculator", layout="wide")
st.title("LR Paris: Selling Price Calculator")

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

col1, col2, col3 = st.columns(3)

with col1:
    unit_cost_input = st.text_input("Unit Cost (USD)", value="")
    margin_pct_input = st.text_input("Desired Margin (%)", value="")

with col2:
    quantity_input = st.text_input("Quantity", value="")
    shipping_input = st.text_input("Shipping Total (USD)", value="")
    run_charge_input = st.text_input("Run Charge (USD per unit)", value="")

with col3:
    sample_input = st.text_input("Sample Cost (USD)", value="")
    setup_input = st.text_input("Setup Cost (USD)", value="")

# Parse safely
unit_cost = safe_float(unit_cost_input)
margin_pct = safe_float(margin_pct_input)
quantity = safe_float(quantity_input)
shipping = safe_float(shipping_input)
run_charge = safe_float(run_charge_input)
sample = safe_float(sample_input)
setup = safe_float(setup_input)

# Check readiness
required_fields_ready = unit_cost > 0 and margin_pct > 0 and quantity > 0

if required_fields_ready:
    margin = margin_pct / 100

    shipping_per_unit = shipping / quantity if quantity else 0
    setup_per_unit = setup / quantity if quantity else 0
    sample_per_unit = sample / quantity if quantity else 0

    landed_unit_cost = unit_cost + run_charge + shipping_per_unit + setup_per_unit + sample_per_unit

    selling_price = landed_unit_cost / (1 - margin) if (1 - margin) != 0 else 0.0

    total_revenue = selling_price * quantity
    total_cost = landed_unit_cost * quantity
    profit = total_revenue - total_cost

    # Display results
    st.markdown("### Results")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Landed Unit Cost", f"${landed_unit_cost:.2f}")
        st.metric("Selling Price (per unit)", f"${selling_price:.2f}")

    with col2:
        st.metric("Total Revenue", f"${total_revenue:.2f}")
        st.metric("Profit", f"${profit:.2f}")
else:
    st.info("Enter Unit Cost, Margin (%), and Quantity to begin calculation.")
