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

codes_dict = {**codes_dict_top, **codes_dict_bottom}

st.set_page_config(layout="wide")
st.markdown("# **FINANCIAL CALCULATOR**")

# --- Selling Price by Margin ---
with st.expander("CALCULATE SELLING PRICE BY MARGIN", expanded=False):
    with st.container():
        total_cost = st.number_input("TOTAL COST", min_value=0.0, value=0.0, key="margin_total_cost")
        margin = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, value=30.0, key="margin_margin")

        if margin < 100:
            selling_price = total_cost / (1 - margin / 100)
            profit = selling_price - total_cost
        else:
            selling_price = profit = 0.0

        st.metric("SELLING PRICE", f"${selling_price:.2f}")
        st.metric("PROFIT", f"${profit:.2f}")

# --- Selling Price by Landed Cost ---
with st.expander("CALCULATE SELLING PRICE BY LANDED COST", expanded=False):
    with st.container():
        item_cost = st.number_input("ITEM COST", min_value=0.0, value=0.0, key="landed_item")
        shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, value=0.0, key="landed_shipping")
        sample_cost = st.number_input("SAMPLE COST", min_value=0.0, value=0.0, key="landed_sample")
        quantity = st.number_input("QTY", min_value=1, value=10, key="landed_qty")
        margin2 = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, value=30.0, key="landed_margin")

        if quantity > 0 and margin2 < 100:
            total_cost = item_cost + shipping_cost + sample_cost
            unit_cost = total_cost / quantity
            selling_price2 = (total_cost / (1 - margin2 / 100)) / quantity
            profit2 = selling_price2 - unit_cost
        else:
            unit_cost = selling_price2 = profit2 = 0.0

        st.metric("PRICE PER UNIT TOTAL COST", f"${unit_cost:.2f}")
        st.metric("SELLING PRICE", f"${selling_price2:.2f}")
        st.metric("PROFIT", f"${profit2:.2f}")

# --- Margin by Price ---
with st.expander("CALCULATE MARGIN BY SELLING PRICE", expanded=False):
    with st.container():
        total_cost3 = st.number_input("TOTAL COST", min_value=0.0, value=0.0, key="margin_by_price_total")
        price3 = st.number_input("SELLING PRICE", min_value=0.0, value=0.0, key="margin_by_price_price")

        if price3 > 0:
            profit3 = price3 - total_cost3
            margin3 = profit3 / price3 * 100
        else:
            profit3 = margin3 = 0.0

        st.metric("MARGIN", f"{margin3:.2f}%")
        st.metric("PROFIT", f"${profit3:.2f}")

# --- Vendor Pricing (Corrected as per R72:X75) ---
with st.expander("CALCULATE MARGIN BY VENDOR PRICING", expanded=True):
    with st.container():
        unit_cost_v = st.number_input("UNIT COST", min_value=0.0, value=0.0, key="vendor_unit_cost")
        shipping_cost_v = st.number_input("SHIPPING COST", min_value=0.0, value=0.0, key="vendor_shipping")
        sample_cost_v = st.number_input("SAMPLE COST", min_value=0.0, value=0.0, key="vendor_sample")
        price_v = st.number_input("SELLING PRICE", min_value=0.0, value=0.0, key="vendor_price")
        discount_code_v = st.text_input("DISCOUNT CODE", key="vendor_discount").upper()

        discount = codes_dict.get(discount_code_v, 0)
        adjusted_price = price_v * (1 - discount)
        total_cost_v = unit_cost_v + shipping_cost_v + sample_cost_v
        profit_v = adjusted_price - total_cost_v
        margin_v = (profit_v / adjusted_price * 100) if adjusted_price > 0 else 0

        st.metric("TOTAL COST", f"${total_cost_v:.2f}")
        st.metric("MARGIN", f"{margin_v:.2f}%")
        st.metric("PROFIT", f"${profit_v:.2f}")

# --- Discount Code Reference Table ---
st.markdown("---")
st.markdown("### DISCOUNT CODE REFERENCE")

discount_table = pd.DataFrame({
    "Code": list(codes_dict.keys()),
    "Discount %": [int(v * 100) for v in codes_dict.values()]
})

st.dataframe(discount_table.sort_values("Code").reset_index(drop=True), use_container_width=True, hide_index=True)
