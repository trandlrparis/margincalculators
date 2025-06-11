import streamlit as st
import pandas as pd

# Discount blocks
codes_dict_top = {
    "A": 0.5, "B": 0.45, "C": 0.4, "D": 0.35, "E": 0.3,
    "F": 0.25, "G": 0.2, "H": 0.15, "I": 0.1, "J": 0.05, "X": 0.0
}

codes_dict_bottom = {
    "L": 0.7, "M": 0.65, "N": 0.6, "O": 0.55, "P": 0.5,
    "Q": 0.45, "R": 0.4, "S": 0.35, "T": 0.3, "U": 0.25,
    "V": 0.2, "W": 0.15, "Y": 0.1, "Z": 0.05, "Z*": 0.0
}

st.set_page_config(page_title="LR Paris Pricing Tool", layout="wide")
st.title("LR Paris: Calculate Selling Price by Landed Cost")

with st.form("pricing_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        cost = st.number_input("Landed Cost (per unit, USD)", min_value=0.0, step=0.01)
        run_charge = st.number_input("Run Charge (USD per unit)", min_value=0.0, step=0.01)

    with col2:
        quantity = st.number_input("Quantity", min_value=1, step=1)
        shipping = st.number_input("Shipping Total (USD)", min_value=0.0, step=0.01)

    with col3:
        sample_cost = st.number_input("Sample Cost (USD)", min_value=0.0, step=0.01)
        setup_cost = st.number_input("Setup Cost (USD)", min_value=0.0, step=0.01)
        code_top = st.selectbox("Top Discount Code", options=list(codes_dict_top.keys()))
        code_bottom = st.selectbox("Bottom Discount Code", options=list(codes_dict_bottom.keys()))

    reset = st.form_submit_button("Reset")
    submit = st.form_submit_button("Calculate")

if reset:
    st.experimental_rerun()

if submit:
    discount_top = codes_dict_top.get(code_top, 0)
    discount_bottom = codes_dict_bottom.get(code_bottom, 0)

    total_cost = (cost * quantity) + (run_charge * quantity) + shipping + sample_cost + setup_cost
    unit_cost = total_cost / quantity
    net_cost = unit_cost / (1 - discount_bottom)
    selling_price = net_cost / (1 - discount_top)

    st.markdown("---")
    st.subheader("Results")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Cost (incl. all fees)", f"${total_cost:.2f}")
        st.metric("Unit Cost", f"${unit_cost:.2f}")

    with col2:
        st.metric("Net Cost", f"${net_cost:.2f}")
        st.metric("Selling Price", f"${selling_price:.2f}")
