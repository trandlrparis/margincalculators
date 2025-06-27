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

# Reset function - reset input fields to their initial values
def reset_fields():
    # Reset fields to their default values based on their initial state
    reset_values = {
        # Fields with None/placeholder initial values
        'margin_total_cost': None,
        'margin_margin': None,
        'margin_by_cost': None,
        'margin_by_price': None,
        'vendor_price': None,
        'margin_vendor': None,
        # Fields with 0 initial values (integers for quantities)
        'landed_quantity': 0,
        'qty_xxs_to_xl': 0,
        'qty_2xl': 0,
        'qty_3xl': 0,
        'qty_4xl': 0,
        # Fields with 0.0 initial values (floats for costs and percentages)
        'landed_item_cost': 0.0,
        'landed_run_charge': 0.0,
        'landed_shipping_cost': 0.0,
        'landed_sample_cost': 0.0,
        'landed_setup_cost': 0.0,
        'landed_margin': 0.0,
        'cost_xxs_to_xl': 0.0,
        'cost_2xl': 0.0,
        'cost_3xl': 0.0,
        'cost_4xl': 0.0,
        'apparel_run_charge': 0.0,
        'apparel_shipping': 0.0,
        'apparel_sample': 0.0,
        'apparel_setup': 0.0,
        'apparel_margin': 0.0,
        # Text field with empty string
        'discount_code': ""
    }
    
    for key, value in reset_values.items():
        st.session_state[key] = value

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
        /* Disable scroll wheel on number inputs */
        input[type=number]::-webkit-outer-spin-button,
        input[type=number]::-webkit-inner-spin-button {
            -webkit-appearance: none;
            margin: 0;
        }
        input[type=number] {
            -moz-appearance: textfield;
        }
        /* This is the key - disable pointer events on scroll for number inputs */
        .stNumberInput input[type="number"] {
            pointer-events: none;
        }
        .stNumberInput input[type="number"]:focus {
            pointer-events: auto;
        }
        .stNumberInput:hover input[type="number"] {
            pointer-events: auto;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("# **FINANCIAL CALCULATORS**")
st.button("🔁 RESET ALL FIELDS", on_click=reset_fields)

# --- Selling Price by Margin ---
with st.expander("CALCULATE SELLING PRICE BY MARGIN", expanded=False):
    with st.container():
        total_cost = st.number_input("TOTAL COST", min_value=0.0, key="margin_total_cost", value=None, placeholder="")
        margin = st.number_input("MARGIN %", min_value=0.0, max_value=99.0, key="margin_margin", value=None, placeholder="")

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
    margin_percent = st.number_input("MARGIN %", min_value=0.0, max_value=99.0, key="landed_margin", value=0.0)

    if quantity > 0:
        total_cost = (item_cost * quantity) + (run_charge * quantity) + shipping_cost + sample_cost + setup_cost
        unit_cost = total_cost / quantity
        selling_price = unit_cost / (1 - margin_percent/100) if margin_percent < 100 else 0
        profit_per_unit = selling_price - unit_cost
        total_selling_price = selling_price * quantity
        total_profit = profit_per_unit * quantity

        st.metric("COST PER UNIT", f"${unit_cost:,.2f}")
        st.metric("SELLING PRICE", f"${selling_price:,.2f}")
        st.metric("PROFIT PER UNIT", f"${profit_per_unit:,.2f}")
        st.metric("TOTAL UNIT COST", f"${total_cost:,.2f}")
        st.metric("TOTAL SELLING PRICE", f"${total_selling_price:,.2f}")
        st.metric("TOTAL PROFIT", f"${total_profit:,.2f}")
    else:
        st.metric("COST PER UNIT", "$0.00")
        st.metric("SELLING PRICE", "$0.00")  
        st.metric("PROFIT PER UNIT", "$0.00")
        st.metric("TOTAL UNIT COST", "$0.00")
        st.metric("TOTAL SELLING PRICE", "$0.00")
        st.metric("TOTAL PROFIT", "$0.00")

# --- Apparel Selling Price ---
with st.expander("CALCULATE APPAREL SELLING PRICE", expanded=False):
    st.markdown("### SIZE-BASED QUANTITIES AND COSTS")
    
    # Create two columns for quantities and costs
    qty_col, cost_col = st.columns(2)
    
    with qty_col:
        st.markdown("**QUANTITIES**")
        qty_xxs_to_xl = st.number_input("XXS TO XL QTY", min_value=0, step=1, key="qty_xxs_to_xl", value=0)
        qty_2xl = st.number_input("2XL QTY", min_value=0, step=1, key="qty_2xl", value=0)
        qty_3xl = st.number_input("3XL QTY", min_value=0, step=1, key="qty_3xl", value=0)
        qty_4xl = st.number_input("4XL QTY", min_value=0, step=1, key="qty_4xl", value=0)
    
    with cost_col:
        st.markdown("**COSTS**")
        cost_xxs_to_xl = st.number_input("XXS TO XL ITEM COST", min_value=0.0, step=0.01, key="cost_xxs_to_xl", value=0.0)
        cost_2xl = st.number_input("2XL ITEM COST", min_value=0.0, step=0.01, key="cost_2xl", value=0.0)
        cost_3xl = st.number_input("3XL ITEM COST", min_value=0.0, step=0.01, key="cost_3xl", value=0.0)
        cost_4xl = st.number_input("4XL ITEM COST", min_value=0.0, step=0.01, key="cost_4xl", value=0.0)
    
    st.markdown("### ADDITIONAL COSTS")
    run_charge = st.number_input("RUN CHARGE", min_value=0.0, step=0.01, key="apparel_run_charge", value=0.0)
    shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, step=0.01, key="apparel_shipping", value=0.0)
    sample_cost = st.number_input("SAMPLE COST", min_value=0.0, step=0.01, key="apparel_sample", value=0.0)
    setup_cost = st.number_input("SETUP COST", min_value=0.0, step=0.01, key="apparel_setup", value=0.0)
    margin = st.number_input("MARGIN %", min_value=0.0, max_value=99.0, step=0.1, key="apparel_margin", value=0.0)
    
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
        cost_per_unit = total_cost / total_units
        selling_price_per_unit = cost_per_unit / (1 - margin/100) if margin < 100 else 0
        profit_per_unit = selling_price_per_unit - cost_per_unit
        total_selling_price = selling_price_per_unit * total_units
        total_profit = profit_per_unit * total_units
    else:
        cost_per_unit = selling_price_per_unit = profit_per_unit = total_cost = total_selling_price = total_profit = 0
    
    st.metric("COST PER UNIT", f"${cost_per_unit:.2f}")
    st.metric("SELLING PRICE", f"${selling_price_per_unit:.2f}")
    st.metric("PROFIT PER UNIT", f"${profit_per_unit:.2f}")
    st.metric("TOTAL UNIT COST", f"${total_cost:,.2f}")
    st.metric("TOTAL SELLING PRICE", f"${total_selling_price:,.2f}")
    st.metric("TOTAL PROFIT", f"${total_profit:,.2f}")

# --- Vendor Pricing ---
with st.expander("CALCULATE VENDOR PRICING", expanded=True):
    with st.container():
        vendor_price = st.number_input("VENDOR PRICE", min_value=0.0, key="vendor_price", value=None, placeholder="")
        discount_code = st.text_input("DISCOUNT CODE", key="discount_code").upper()

        discount = codes_dict_top.get(discount_code, codes_dict_bottom.get(discount_code, 0))

        if vendor_price is not None:
            unit_cost_vendor = vendor_price * (1 - discount)
        else:
            unit_cost_vendor = 0.0

        st.metric("UNIT COST", f"${unit_cost_vendor:.2f}")

        margin_vendor = st.number_input("MARGIN %", min_value=0.0, max_value=99.0, key="margin_vendor", value=None, placeholder="")

        if unit_cost_vendor > 0 and margin_vendor is not None and margin_vendor < 100:
            selling_price_vendor = unit_cost_vendor / (1 - margin_vendor / 100)
            profit_vendor = selling_price_vendor - unit_cost_vendor
        else:
            selling_price_vendor = profit_vendor = 0.0

        st.metric("SELLING PRICE", f"${selling_price_vendor:.2f}")
        st.metric("PROFIT", f"${profit_vendor:.2f}")

# --- Discount Codes Reference - At bottom of page ---
st.markdown("---")
st.markdown("## **DISCOUNT CODES REFERENCE**")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**ABC SYSTEM**")
    abc_table = pd.DataFrame.from_dict(codes_dict_top, orient='index', columns=["Discount"]).reset_index()
    abc_table.columns = ["Code", "Discount"]
    abc_table["Discount"] = abc_table["Discount"].apply(lambda x: f"{int(x*100)}%")
    st.dataframe(abc_table, use_container_width=True, hide_index=True)

with col2:
    st.markdown("**PQR SYSTEM**")
    pqr_table = pd.DataFrame.from_dict(codes_dict_bottom, orient='index', columns=["Discount"]).reset_index()
    pqr_table.columns = ["Code", "Discount"]
    pqr_table["Discount"] = pqr_table["Discount"].apply(lambda x: f"{int(x*100)}%")
    st.dataframe(pqr_table, use_container_width=True, hide_index=True)