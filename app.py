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
        total_cost = st.number_input("TOTAL COST (Margin)", min_value=0.0, key="margin_total_cost", value=None, placeholder="")
        margin = st.number_input("MARGIN % (Margin)", min_value=0.0, max_value=99.9, key="margin_margin", value=None, placeholder="")

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
        item_cost = st.number_input("ITEM COST (Landed)", min_value=0.0, key="landed_item", value=None, placeholder="")
        shipping_cost = st.number_input("SHIPPING COST (Landed)", min_value=0.0, key="landed_shipping", value=None, placeholder="")
        sample_cost = st.number_input("SAMPLE COST (Landed)", min_value=0.0, key="landed_sample", value=None, placeholder="")
        quantity = st.number_input("QTY (Landed)", min_value=1, key="landed_qty", value=None, placeholder="")
        margin2 = st.number_input("MARGIN % (Landed)", min_value=0.0, max_value=99.9, key="landed_margin", value=None, placeholder="")

        if all(v is not None for v in [item_cost, shipping_cost, sample_cost, quantity, margin2]) and margin2 < 100:
            unit_cost = (item_cost + shipping_cost / quantity + sample_cost / quantity)
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
        total_cost3 = st.number_input("TOTAL COST (Margin %)", min_value=0.0, key="margin_by_cost", value=None, placeholder="")
        price3 = st.number_input("SELLING PRICE (Margin %)", min_value=0.0, key="margin_by_price", value=None, placeholder="")

        if total_cost3 is not None and price3 is not None and price3:
            profit3 = price3 - total_cost3
            margin3 = profit3 / price3 * 100
        else:
            profit3 = margin3 = 0.0

        st.metric("MARGIN", f"{margin3:.2f}%")
        st.metric("PROFIT", f"${profit3:.2f}")

# --- Vendor Pricing (Based on R72:X75) ---
with st.expander("CALCULATE VENDOR PRICING", expanded=False):
    with st.container():
        unit_cost_v = st.number_input("UNIT COST (Vendor)", min_value=0.0, key="vendor_cost", value=None, placeholder="")
        discount_code_v = st.text_input("DISCOUNT CODE (Vendor)", key="vendor_code").upper()
        price_v = st.number_input("SELLING PRICE (Vendor)", min_value=0.0, key="vendor_price", value=None, placeholder="")

        discount = codes_dict_top.get(discount_code_v, codes_dict_bottom.get(discount_code_v, 0))
        discounted_price = price_v * (1 - discount)
        margin_v = ((discounted_price - unit_cost_v) / discounted_price * 100) if discounted_price > 0 else 0
        profit_v = discounted_price - unit_cost_v

        st.metric("DISCOUNTED PRICE", f"${discounted_price:.2f}")
        st.metric("MARGIN", f"{margin_v:.2f}%")
        st.metric("PROFIT", f"${profit_v:.2f}")

# --- Discount Code Reference Tables ---
st.markdown("---")
st.markdown("### DISCOUNT CODE REFERENCE")

df_top = pd.DataFrame({
    "Code": list(codes_dict_top.keys()),
    "Discount %": [int(v * 100) for v in codes_dict_top.values()]
})

df_bottom = pd.DataFrame({
    "Code": list(codes_dict_bottom.keys()),
    "Discount %": [int(v * 100) for v in codes_dict_bottom.values()]
})

st.markdown("#### Top Codes")
st.dataframe(df_top.style.set_properties(**{'background-color': '#F5F5F5', 'border': '1px solid black'}), use_container_width=True)

st.markdown("#### Bottom Codes")
st.dataframe(df_bottom.style.set_properties(**{'background-color': '#F5F5F5', 'border': '1px solid black'}), use_container_width=True)
