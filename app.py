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
    
        input[type=number]::-webkit-inner-spin-button {
            opacity: 1 !important;
        }
        input, select, textarea {
            pointer-events: auto !important;
        }
        .stNumberInput input:focus {
            pointer-events: auto !important;
        }
        .stNumberInput {
            overflow: visible !important;
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

# --- Selling Price by Landed Cost ---
with st.expander("CALCULATE SELLING PRICE BY LANDED COST", expanded=False):
    with st.container():
        item_cost = st.number_input("ITEM COST", min_value=0.0, key="landed_item", value=None, placeholder="")
        shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, key="landed_shipping", value=0.0, placeholder="")
        sample_cost = st.number_input("SAMPLE COST", min_value=0.0, key="landed_sample", value=0.0, placeholder="")
        setup_cost = st.number_input("SETUP COST", min_value=0.0, key="landed_setup", value=0.0, placeholder="")
        run_charge = st.number_input("RUN CHARGE", min_value=0.0, key="landed_run", value=0.0, placeholder="")
        quantity = st.number_input("QTY", min_value=1, key="landed_qty", value=None, placeholder="")
        margin2 = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, key="landed_margin", value=None, placeholder="")

        if all(v is not None for v in [item_cost, run_charge, quantity, shipping_cost, sample_cost, setup_cost, margin2]) and margin2 < 100:
            total_cost = ((item_cost + run_charge) * quantity + shipping_cost + sample_cost + setup_cost)
            unit_cost = total_cost / quantity
            unit_price = unit_cost / (1 - margin2 / 100)
            total_selling_price = unit_price * quantity
            profit2 = unit_price - unit_cost

            st.metric("UNIT COST", f"${unit_cost:.2f}")
            st.metric("TOTAL COST", f"${total_cost:.2f}")
            st.metric("SELLING PRICE", f"${unit_price:.2f}")
            st.metric("TOTAL SELLING PRICE", f"${total_selling_price:.2f}")
            st.metric("PROFIT", f"${profit2:.2f}")
        else:
            st.metric("UNIT COST", "$0.00")
            st.metric("TOTAL COST", "$0.00")
            st.metric("SELLING PRICE", "$0.00")
            st.metric("TOTAL SELLING PRICE", "$0.00")
            st.metric("PROFIT", "$0.00")

# --- Apparel Selling Price Tool ---
with st.expander("CALCULATE APPAREL SELLING PRICE", expanded=False):
    with st.container():
        st.markdown("### SIZE-BASED QUANTITIES AND COSTS")
        col1, col2 = st.columns(2)
        with col1:
            qty_xxs_to_xl = st.number_input("XXS–XL QUANTITY", min_value=0, value=0, key="qty_xxs_to_xl")
            qty_2xl = st.number_input("2XL QUANTITY", min_value=0, value=0, key="qty_2xl")
            qty_3xl = st.number_input("3XL QUANTITY", min_value=0, value=0, key="qty_3xl")
            qty_4xl = st.number_input("4XL QUANTITY", min_value=0, value=0, key="qty_4xl")
        with col2:
            cost_xxs_to_xl = st.number_input("XXS–XL UNIT COST", min_value=0.0, value=0.0, key="cost_xxs_to_xl")
            cost_2xl = st.number_input("2XL UNIT COST", min_value=0.0, value=0.0, key="cost_2xl")
            cost_3xl = st.number_input("3XL UNIT COST", min_value=0.0, value=0.0, key="cost_3xl")
            cost_4xl = st.number_input("4XL UNIT COST", min_value=0.0, value=0.0, key="cost_4xl")

        st.markdown("### ADDITIONAL COSTS")
        shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, value=0.0, key="apparel_shipping_cost")
        sample_cost = st.number_input("SAMPLE COST", min_value=0.0, value=0.0, key="apparel_sample_cost")
        setup_cost = st.number_input("SETUP COST", min_value=0.0, value=0.0, key="apparel_setup_cost")
        run_charge = st.number_input("RUN CHARGE PER UNIT", min_value=0.0, value=0.0, key="apparel_run_charge")
        margin_percent = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, value=40.0, key="apparel_margin")
        margin = margin_percent / 100

        total_units = qty_xxs_to_xl + qty_2xl + qty_3xl + qty_4xl
        item_cost_total = (
            qty_xxs_to_xl * cost_xxs_to_xl +
            qty_2xl * cost_2xl +
            qty_3xl * cost_3xl +
            qty_4xl * cost_4xl
        )
        run_charge_total = total_units * run_charge
        pre_margin_cost = item_cost_total + run_charge_total + shipping_cost + sample_cost + setup_cost

        selling_price = pre_margin_cost / (1 - margin) if (1 - margin) > 0 else 0.0
        profit_per_unit = selling_price / total_units - pre_margin_cost / total_units if total_units else 0
        total_profit = selling_price - pre_margin_cost

        st.metric("TOTAL UNITS", f"{total_units}")
        st.metric("ITEM COST TOTAL", f"${item_cost_total:,.2f}")
        st.metric("RUN CHARGE TOTAL", f"${run_charge_total:,.2f}")
        st.metric("ALL-IN COST (BEFORE MARGIN)", f"${pre_margin_cost:,.2f}")
        st.metric("SELLING PRICE (AFTER MARGIN)", f"${selling_price:,.2f}")



        st.metric("AVERAGE COST PER UNIT", f"${pre_margin_cost / total_units:.2f}" if total_units else "$0.00")
        st.metric("AVERAGE SELLING PRICE PER UNIT", f"${selling_price / total_units:.2f}" if total_units else "$0.00")

        st.metric("PROFIT PER UNIT", f"${profit_per_unit:.2f}")
        st.metric("TOTAL PROFIT", f"${total_profit:.2f}")# --- Vendor Pricing ---
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

# --- Display Discount Codes ---
st.markdown("### ABC System")
abc_table = pd.DataFrame.from_dict(codes_dict_top, orient='index', columns=["Discount"]).reset_index()
abc_table.columns = ["Code", "Discount"]
abc_table["Discount"] = abc_table["Discount"].apply(lambda x: f"{int(x*100)}%")
st.dataframe(abc_table, use_container_width=True, hide_index=True)

st.markdown("### PQR System")
pqr_table = pd.DataFrame.from_dict(codes_dict_bottom, orient='index', columns=["Discount"]).reset_index()
pqr_table.columns = ["Code", "Discount"]
pqr_table["Discount"] = pqr_table["Discount"].apply(lambda x: f"{int(x*100)}%")
st.dataframe(pqr_table, use_container_width=True, hide_index=True)
