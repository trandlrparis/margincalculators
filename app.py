import streamlit as st
import pandas as pd

# Discount blocks
codes_dict_top = {
    "A": 0.5, "B": 0.45, "C": 0.4, "D": 0.35, "E": 0.3,
    "F": 0.25, "G": 0.2, "H": 0.15, "I": 0.1, "J": 0.05, "X": 0.0
}

codes_dict_bottom = {
    "L": 0.7, "M": 0.65, "N": 0.6, "O": 0.55, "P": 0.5, "Q": 0.45,
    "R": 0.4, "S": 0.35, "T": 0.3, "U": 0.25, "V": 0.2, "W": 0.15,
    "Y": 0.05, "Z": 0.0
}

# Reset function
def reset_fields():
    st.session_state.clear()

st.set_page_config(layout="wide")

# Apply LR Paris style
st.markdown("""
    <style>
        body, .block-container {
            background-color: #f5f3f0;
            color: #002855;
        }
        .stNumberInput > div > input {
            background-color: #ffffff;
            color: #002855;
        }
        .stButton > button {
            background-color: #002855;
            color: white;
            border: none;
            padding: 0.5em 1em;
            border-radius: 5px;
        }
        .stMetricLabel, .stMetricValue {
            color: #002855 !important;
        }
        .stExpanderHeader {
            font-weight: bold;
            color: #002855;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("# **FINANCIAL CALCULATORS**")
st.button("🔁 RESET ALL FIELDS", on_click=reset_fields)

# --- Selling Price by Margin ---
with st.expander("CALCULATE SELLING PRICE BY MARGIN", expanded=False):
    with st.container():
        total_cost = st.number_input("TOTAL COST", min_value=0.0, key="margin_total_cost", value=None, placeholder="")
        margin = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, key="margin_margin", value=None, placeholder="")

        if total_cost is not None and margin is not None and margin < 100:
            selling_price = total_cost / (1 - margin / 100)
            profit = selling_price - total_cost
        else:
            selling_price = profit = 0.0

        st.metric("SELLING PRICE", f"${selling_price:.2f}")
        st.metric("PROFIT", f"${profit:.2f}")

# --- Calculate Margin by Selling Price ---
with st.expander("CALCULATE MARGIN BY SELLING PRICE", expanded=False):
    with st.container():
        total_cost3 = st.number_input("TOTAL COST", min_value=0.0, key="margin_by_cost", value=None, placeholder="")
        price3 = st.number_input("SELLING PRICE", min_value=0.0, key="margin_by_price", value=None, placeholder="")

        if total_cost3 is not None and price3 is not None and price3 > 0:
            profit3 = price3 - total_cost3
            margin3 = profit3 / price3 * 100
        else:
            profit3 = margin3 = 0.0

        st.metric("MARGIN", f"{margin3:.2f}%")
        st.metric("PROFIT", f"${profit3:.2f}")

# --- Selling Price by Landed Cost ---
with st.expander("CALCULATE SELLING PRICE BY LANDED COST", expanded=False):
    item_cost = st.number_input("ITEM COST", min_value=0.0, key="landed_item_cost", value=0.0)
    quantity = st.number_input("QUANTITY", min_value=0, key="landed_quantity", value=0)
    run_charge = st.number_input("RUN CHARGE", min_value=0.0, key="landed_run_charge", value=0.0)
    shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, key="landed_shipping_cost", value=0.0)
    sample_cost = st.number_input("SAMPLE COST", min_value=0.0, key="landed_sample_cost", value=0.0)
    setup_cost = st.number_input("SETUP COST", min_value=0.0, key="landed_setup_cost", value=0.0)
    margin_percent = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, key="landed_margin", value=0.0)

    if quantity > 0:
        total_cost = (item_cost * quantity) + (run_charge * quantity) + shipping_cost + sample_cost + setup_cost
        unit_cost = total_cost / quantity
        selling_price = unit_cost / (1 - margin_percent/100) if margin_percent < 100 else 0
        profit_per_unit = selling_price - unit_cost
        total_profit = profit_per_unit * quantity

        st.metric("TOTAL COST", f"${total_cost:,.2f}")
        st.metric("COST PER UNIT", f"${unit_cost:,.2f}")
        st.metric("SELLING PRICE", f"${selling_price:,.2f}")
        st.metric("PROFIT PER UNIT", f"${profit_per_unit:,.2f}")
        st.metric("TOTAL PROFIT", f"${total_profit:,.2f}")
    else:
        st.metric("TOTAL COST", "$0.00")
        st.metric("COST PER UNIT", "$0.00")
        st.metric("SELLING PRICE", "$0.00")
        st.metric("PROFIT PER UNIT", "$0.00")
        st.metric("TOTAL PROFIT", "$0.00")

# --- Apparel Selling Price ---
with st.expander("CALCULATE APPAREL SELLING PRICE", expanded=False):
    st.markdown("### SIZE-BASED QUANTITIES AND COSTS")
    cost_xxs_to_xl = st.number_input("XXS TO XL ITEM COST", min_value=0.0, step=0.01, key="cost_xxs_to_xl", value=0.0)
    qty_xxs_to_xl = st.number_input("XXS TO XL QTY", min_value=0, step=1, key="qty_xxs_to_xl", value=0)
    cost_2xl = st.number_input("2XL ITEM COST", min_value=0.0, step=0.01, key="cost_2xl", value=0.0)
    qty_2xl = st.number_input("2XL QTY", min_value=0, step=1, key="qty_2xl", value=0)
    cost_3xl = st.number_input("3XL ITEM COST", min_value=0.0, step=0.01, key="cost_3xl", value=0.0)
    qty_3xl = st.number_input("3XL QTY", min_value=0, step=1, key="qty_3xl", value=0)
    cost_4xl = st.number_input("4XL ITEM COST", min_value=0.0, step=0.01, key="cost_4xl", value=0.0)
    qty_4xl = st.number_input("4XL QTY", min_value=0, step=1, key="qty_4xl", value=0)
    
    st.markdown("### ADDITIONAL COSTS")
    run_charge = st.number_input("RUN CHARGE", min_value=0.0, step=0.01, key="apparel_run_charge", value=0.0)
    shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, step=0.01, key="apparel_shipping", value=0.0)
    sample_cost = st.number_input("SAMPLE COST", min_value=0.0, step=0.01, key="apparel_sample", value=0.0)
    setup_cost = st.number_input("SETUP COST", min_value=0.0, step=0.01, key="apparel_setup", value=0.0)
    margin = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, step=0.1, key="apparel_margin", value=0.0)
    
    total_units = qty_xxs_to_xl + qty_2xl + qty_3xl + qty_4xl
    item_cost_total = (
        cost_xxs_to_xl * qty_xxs_to_xl +
        cost_2xl * qty_2xl +
        cost_3xl * qty_3xl +
        cost_4xl * qty_4xl
    )
    additional_costs = shipping_cost + sample_cost + setup_cost + (run_charge * total_units)
    total_cost = item_cost_total + additional_costs
    
    if total_units > 0:
        avg_cost_per_unit = total_cost / total_units
        selling_price_per_unit = avg_cost_per_unit / (1 - margin/100) if margin < 100 else 0
        profit_per_unit = selling_price_per_unit - avg_cost_per_unit
        total_profit = profit_per_unit * total_units
    else:
        avg_cost_per_unit = selling_price_per_unit = profit_per_unit = total_profit = 0
    
    st.metric("TOTAL UNITS", total_units)
    st.metric("AVG COST PER UNIT", f"${avg_cost_per_unit:.2f}")
    st.metric("SELLING PRICE PER UNIT", f"${selling_price_per_unit:.2f}")
    st.metric("PROFIT PER UNIT", f"${profit_per_unit:.2f}")
    st.metric("TOTAL PROFIT", f"${total_profit:,.2f}")

# --- Vendor Pricing ---
with st.expander("VENDOR PRICING", expanded=False):
    base_price = st.number_input("BASE PRICE", min_value=0.0, step=0.01, key="vendor_base_price", value=0.0)
    markup_percent = st.number_input("MARKUP %", min_value=0.0, max_value=100.0, step=0.1, key="vendor_markup_percent", value=0.0)
    vendor_price = base_price * (1 + markup_percent/100)
    st.metric("VENDOR PRICE", f"${vendor_price:,.2f}")

# --- Discount Codes Reference ---
with st.expander("REFERENCE: DISCOUNT CODES", expanded=False):
    st.markdown('''
    **ABC SYSTEM DISCOUNTS**
    - A: 1000 pcs or more
    - B: 500–999 pcs
    - C: 250–499 pcs
    - D: 100–249 pcs

    **PQR SYSTEM DISCOUNTS**
    - P100: 0%
    - P80: 20%
    - P60: 40%
    - P50: 50%
    - P40: 60%
    - P30: 70%
    ''')