import streamlit as st

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

col1, col2 = st.columns(2)

with col1:
    st.markdown("### CALCULATE SELLING PRICE BY MARGIN")
    total_cost = st.number_input("TOTAL COST", min_value=0.0, value=0.0, key="margin_total_cost")
    margin = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, value=30.0, key="margin_margin")

    if margin < 100:
        selling_price = total_cost / (1 - margin / 100)
        profit = selling_price - total_cost
    else:
        selling_price = profit = 0.0

    st.metric("SELLING PRICE", f"${selling_price:.2f}")
    st.metric("PROFIT", f"${profit:.2f}")

with col2:
    st.markdown("### CALCULATE SELLING PRICE BY LANDED COST")
    item_cost = st.number_input("ITEM COST", min_value=0.0, value=0.0, key="landed_item")
    shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, value=0.0, key="landed_shipping")
    sample_cost = st.number_input("SAMPLE COST", min_value=0.0, value=0.0, key="landed_sample")
    quantity = st.number_input("QTY", min_value=1, value=10, key="landed_qty")
    margin2 = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, value=30.0, key="landed_margin")

    if quantity > 0 and margin2 < 100:
        total_cost_landed = item_cost + shipping_cost + sample_cost
        unit_cost = total_cost_landed / quantity
        selling_price2 = (total_cost_landed / (1 - margin2 / 100)) / quantity
        profit2 = selling_price2 - unit_cost
    else:
        unit_cost = selling_price2 = profit2 = 0.0

    st.metric("PRICE PER UNIT TOTAL COST", f"${unit_cost:.2f}")
    st.metric("SELLING PRICE", f"${selling_price2:.2f}")
    st.metric("PROFIT", f"${profit2:.2f}")

col3, col4 = st.columns(2)

with col3:
    st.markdown("### CALCULATE MARGIN BY SELLING PRICE")
    total_cost3 = st.number_input("TOTAL COST", min_value=0.0, value=0.0, key="margin_by_price_total")
    price3 = st.number_input("SELLING PRICE", min_value=0.0, value=0.0, key="margin_by_price_price")

    if price3 > 0:
        profit3 = price3 - total_cost3
        margin3 = profit3 / price3 * 100
    else:
        profit3 = margin3 = 0.0

    st.metric("MARGIN", f"{margin3:.2f}%")
    st.metric("PROFIT", f"${profit3:.2f}")

with col4:
    st.markdown("### CALCULATE MARGIN BY LANDED COST (VENDOR)")
    item_cost4 = st.number_input("ITEM COST", min_value=0.0, value=0.0, key="vendor_item")
    shipping_cost4 = st.number_input("SHIPPING COST", min_value=0.0, value=0.0, key="vendor_shipping")
    sample_cost4 = st.number_input("SAMPLE COST", min_value=0.0, value=0.0, key="vendor_sample")
    qty4 = st.number_input("QTY", min_value=1, value=10, key="vendor_qty")
    price4 = st.number_input("SELLING PRICE", min_value=0.0, value=0.0, key="vendor_price")
    discount_code4 = st.text_input("DISCOUNT CODE", key="vendor_discount").upper()

    if qty4 > 0:
        discount = codes_dict.get(discount_code4, 0)
        total_cost_vendor = item_cost4 + shipping_cost4 + sample_cost4
        unit_cost_vendor = total_cost_vendor / qty4
        discounted_price = price4 * (1 - discount)
        profit4 = discounted_price - unit_cost_vendor
        margin4 = (profit4 / discounted_price) * 100 if discounted_price > 0 else 0
    else:
        unit_cost_vendor = discounted_price = profit4 = margin4 = 0.0

    st.metric("PRICE PER UNIT TOTAL COST", f"${unit_cost_vendor:.2f}")
    st.metric("MARGIN", f"{margin4:.2f}%")
    st.metric("PROFIT", f"${profit4:.2f}")

st.markdown("---")
st.markdown("### DISCOUNT CODE REFERENCE")

col5, col6 = st.columns(2)
with col5:
    for code, value in codes_dict_top.items():
        st.write(f"{code}: {int(value * 100)}% OFF")

with col6:
    for code, value in codes_dict_bottom.items():
        st.write(f"{code}: {int(value * 100)}% OFF")
