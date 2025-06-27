
import streamlit as st

st.set_page_config(layout="wide")

st.title("MARGIN & PRICING TOOLS")

# TOOL 1: Selling Price by Margin
with st.expander("🟦 SELLING PRICE BY MARGIN", expanded=True):
    cost = st.number_input("ITEM COST", min_value=0.0, step=0.01, key="margin_cost")
    margin = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, step=0.1, key="margin_percent")

    if margin == 100:
        st.error("Margin cannot be 100%")
    else:
        try:
            margin_decimal = margin / 100
            selling_price = cost / (1 - margin_decimal)
            st.metric("SELLING PRICE", f"${selling_price:,.2f}")
        except ZeroDivisionError:
            st.error("Invalid calculation due to margin")

# TOOL 2: Margin by Selling Price
with st.expander("🟩 MARGIN BY SELLING PRICE", expanded=False):
    cost = st.number_input("ITEM COST", min_value=0.0, step=0.01, key="margin_sp_cost")
    selling_price = st.number_input("SELLING PRICE", min_value=0.0, step=0.01, key="margin_sp_price")

    if selling_price != 0:
        margin_percent = ((selling_price - cost) / selling_price) * 100
        st.metric("MARGIN %", f"{margin_percent:.2f}%")
    else:
        st.error("Selling price must be greater than 0")

# TOOL 3: Selling Price by Landed Cost
with st.expander("🟨 SELLING PRICE BY LANDED COST", expanded=False):
    item_cost = st.number_input("ITEM COST", min_value=0.0, step=0.01, key="landed_cost")
    quantity = st.number_input("QUANTITY", min_value=0, step=1, key="landed_qty")
    run_charge = st.number_input("RUN CHARGE", min_value=0.0, step=0.01, key="landed_run")
    shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, step=0.01, key="landed_shipping")
    sample_cost = st.number_input("SAMPLE COST", min_value=0.0, step=0.01, key="landed_sample")
    setup_cost = st.number_input("SETUP COST", min_value=0.0, step=0.01, key="landed_setup")
    margin_percent = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, step=0.1, key="landed_margin")

    if quantity > 0:
        try:
            total_cost = (item_cost * quantity) + (run_charge * quantity) + shipping_cost + sample_cost + setup_cost
            margin_decimal = margin_percent / 100
            selling_price_per_unit = (total_cost / quantity) / (1 - margin_decimal)
            st.metric("SELLING PRICE PER UNIT", f"${selling_price_per_unit:,.2f}")
        except ZeroDivisionError:
            st.error("Invalid margin %")
    else:
        st.warning("Enter a quantity greater than 0")

# TOOL 4: Vendor Pricing
with st.expander("🟥 VENDOR PRICING", expanded=False):
    base_price = st.number_input("BASE PRICE", min_value=0.0, step=0.01, key="vendor_base")
    markup_percent = st.number_input("MARKUP %", min_value=0.0, step=0.1, key="vendor_markup")

    final_price = base_price * (1 + markup_percent / 100)
    st.metric("VENDOR PRICE", f"${final_price:,.2f}")
