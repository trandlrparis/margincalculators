import streamlit as st

# Discount blocks as defined in the Excel sheet
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
st.title("Financial Calculator (Excel-Style)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### CALCULATE SELLING PRICE BY MARGIN")
    total_cost = st.number_input("Total Cost", min_value=0.0, value=0.0, key="margin_total_cost")
    margin = st.number_input("Margin %", min_value=0.0, max_value=99.9, value=30.0, key="margin_margin")
    discount_code = st.text_input("Discount Code", key="margin_code").upper()

    if margin < 100:
        selling_price = total_cost / (1 - margin / 100)
        discounted_price = selling_price * (1 - codes_dict.get(discount_code, 0))
        profit = discounted_price - total_cost
    else:
        selling_price = discounted_price = profit = 0.0

    st.metric("Selling Price (after discount)", f"${discounted_price:.2f}")
    st.metric("Profit", f"${profit:.2f}")

with col2:
    st.markdown("### CALCULATE SELLING PRICE BY LANDED COST")
    item_cost = st.number_input("Item Cost", min_value=0.0, value=0.0, key="landed_item")
    shipping_cost = st.number_input("Shipping Cost", min_value=0.0, value=0.0, key="landed_shipping")
    sample_cost = st.number_input("Sample Cost", min_value=0.0, value=0.0, key="landed_sample")
    quantity = st.number_input("Quantity", min_value=1, value=10, key="landed_qty")
    margin2 = st.number_input("Margin %", min_value=0.0, max_value=99.9, value=30.0, key="landed_margin")
    discount_code2 = st.text_input("Discount Code", key="landed_code").upper()

    if quantity > 0 and margin2 < 100:
        unit_cost = (item_cost + shipping_cost + sample_cost) / quantity
        landed_price = unit_cost / (1 - margin2 / 100)
        discounted_price2 = landed_price * (1 - codes_dict.get(discount_code2, 0))
        profit2 = discounted_price2 - unit_cost
    else:
        unit_cost = landed_price = discounted_price2 = profit2 = 0.0

    st.metric("Price per Unit (Total Cost)", f"${unit_cost:.2f}")
    st.metric("Selling Price (after discount)", f"${discounted_price2:.2f}")
    st.metric("Profit", f"${profit2:.2f}")

st.markdown("---")
st.markdown("### Discount Code Reference")

col3, col4 = st.columns(2)
with col3:
    st.markdown("**Top Codes (S81:AC82)**")
    for code, value in codes_dict_top.items():
        st.write(f"{code}: {int(value * 100)}% off")

with col4:
    st.markdown("**Bottom Codes (S84:AG85)**")
    for code, value in codes_dict_bottom.items():
        st.write(f"{code}: {int(value * 100)}% off")
