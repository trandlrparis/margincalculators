
import streamlit as st
import pandas as pd

# Discount blocks
codes_dict_top = {
    "A": 0.5, "B": 0.45, "C": 0.4, "D": 0.35, "E": 0.3,
    "F": 0.25, "G": 0.2, "H": 0.15, "I": 0.1, "J": 0.05, "X": 0.1
}

codes_dict_bottom = {
    "L": 0.7, "M": 0.65, "N": 0.6, "O": 0.55, "P": 0.5, "Q": 0.45,
    "R": 0.4, "S": 0.35, "T": 0.3, "U": 0.25, "V": 0.2, "W": 0.15,
    "Y": 0.05, "Z": 0.0
}

st.set_page_config(layout="wide")
st.markdown("# **FINANCIAL CALCULATORS**")

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

# --- Selling Price by Landed Cost ---
with st.expander("CALCULATE SELLING PRICE BY LANDED COST", expanded=False):
    with st.container():
        item_cost = st.number_input("ITEM COST", min_value=0.0, key="landed_item", value=None, placeholder="")
        shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, key="landed_shipping", value=None, placeholder="")
        sample_cost = st.number_input("SAMPLE COST", min_value=0.0, key="landed_sample", value=None, placeholder="")
        quantity = st.number_input("QTY", min_value=1, key="landed_qty", value=None, placeholder="")
        margin2 = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, key="landed_margin", value=None, placeholder="")

        if all(v is not None for v in [item_cost, shipping_cost, sample_cost, quantity, margin2]) and margin2 < 100:
            unit_cost = (item_cost + shipping_cost + sample_cost) / quantity
            unit_price = unit_cost / (1 - margin2 / 100)
            profit2 = unit_price - unit_cost
        else:
            unit_cost = unit_price = profit2 = 0.0

        st.metric("UNIT COST", f"${unit_cost:.2f}")
        st.metric("SELLING PRICE", f"${unit_price:.2f}")
        st.metric("PROFIT", f"${profit2:.2f}")

# --- Margin by Selling Price ---
with st.expander("CALCULATE MARGIN BY SELLING PRICE", expanded=False):
    with st.container():
        total_cost3 = st.number_input("TOTAL COST", min_value=0.0, key="margin_by_cost", value=None, placeholder="")
        price3 = st.number_input("SELLING PRICE", min_value=0.0, key="margin_by_price", value=None, placeholder="")

        if total_cost3 is not None and price3 is not None and price3:
            profit3 = price3 - total_cost3
            margin3 = profit3 / price3 * 100
        else:
            profit3 = margin3 = 0.0

        st.metric("MARGIN", f"{margin3:.2f}%")
        st.metric("PROFIT", f"${profit3:.2f}")

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

        margin_vendor = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, key="margin_vendor", value=None, placeholder="")

        if unit_cost_vendor > 0 and margin_vendor is not None and margin_vendor < 100:
            selling_price_vendor = unit_cost_vendor / (1 - margin_vendor / 100)
            profit_vendor = selling_price_vendor - unit_cost_vendor
        else:
            selling_price_vendor = profit_vendor = 0.0

        st.metric("SELLING PRICE", f"${selling_price_vendor:.2f}")
        st.metric("PROFIT", f"${profit_vendor:.2f}")

# --- Discount Code Reference Tables ---
st.markdown("---")
st.markdown("### DISCOUNT CODE REFERENCE")

st.markdown("#### ABC System")
df_top = pd.DataFrame({
    "Code": list(codes_dict_top.keys()),
    "Discount %": [int(v * 100) for v in codes_dict_top.values()]
})

st.dataframe(df_top.style.set_table_styles([
    {'selector': 'th', 'props': [('background-color', '#DDEEFF'), ('color', 'black'), ('font-weight', 'bold')]},
    {'selector': 'td', 'props': [('background-color', '#FFFFFF'), ('color', 'black')]},
    {'selector': 'table', 'props': [('border', '2px solid #4477AA')]}
]), use_container_width=True)

st.markdown("#### PQR System")
df_bottom = pd.DataFrame({
    "Code": list(codes_dict_bottom.keys()),
    "Discount %": [int(v * 100) for v in codes_dict_bottom.values()]
})

st.dataframe(df_bottom.style.set_table_styles([
    {'selector': 'th', 'props': [('background-color', '#FFEEDD'), ('color', 'black'), ('font-weight', 'bold')]},
    {'selector': 'td', 'props': [('background-color', '#FFFFFF'), ('color', 'black')]},
    {'selector': 'table', 'props': [('border', '2px solid #AA7744')]}
]), use_container_width=True)

# Add CSS to prevent scroll lock and override tab navigation
st.markdown("""
    <style>
    .stNumberInput input[type=number]::-webkit-outer-spin-button,
    .stNumberInput input[type=number]::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    input:focus {
        outline: 2px solid #4A90E2;
    }
    input, select, textarea {
        tab-index: 0;
    }
    .block-container { overflow-y: auto; }
    </style>
""", unsafe_allow_html=True)
