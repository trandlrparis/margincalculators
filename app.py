
import streamlit as st

st.set_page_config(page_title="Margin Calculator", layout="wide")

# Title
st.title("MARGIN CALCULATOR")

# Tool 1: CALCULATE SELLING PRICE BY MARGIN
st.header("CALCULATE SELLING PRICE BY MARGIN")
item_cost = st.number_input("ITEM COST", min_value=0.0, step=0.01, key="margin_item_cost")
margin = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, step=0.1, key="margin_margin") / 100

if margin < 1:
    try:
        selling_price = item_cost / (1 - margin)
        st.metric("SELLING PRICE", f"${selling_price:.2f}")
    except ZeroDivisionError:
        st.error("Margin cannot be 100%")

# Tool 2: CALCULATE MARGIN BY SELLING PRICE
st.header("CALCULATE MARGIN BY SELLING PRICE")
cost = st.number_input("ITEM COST", min_value=0.0, step=0.01, key="sell_cost")
price = st.number_input("SELLING PRICE", min_value=0.0, step=0.01, key="sell_price")

if price:
    margin = (price - cost) / price
    st.metric("MARGIN", f"{margin * 100:.2f}%")

# Tool 3: CALCULATE SELLING PRICE BY LANDED COST
st.header("CALCULATE SELLING PRICE BY LANDED COST")
item_cost_landed = st.number_input("ITEM COST", min_value=0.0, step=0.01, key="landed_item_cost")
quantity_landed = st.number_input("QUANTITY", min_value=0, step=1, key="landed_quantity")
run_charge_landed = st.number_input("RUN CHARGE", min_value=0.0, step=0.01, key="landed_run_charge")
shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, step=0.01, key="landed_shipping")
setup_cost = st.number_input("SETUP COST", min_value=0.0, step=0.01, key="landed_setup")
sample_cost = st.number_input("SAMPLE COST", min_value=0.0, step=0.01, key="landed_sample")
margin_landed_percent = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, step=0.1, key="landed_margin")

if quantity_landed > 0:
    run_total = run_charge_landed * quantity_landed
    base_cost = item_cost_landed * quantity_landed
    additional = shipping_cost + setup_cost + sample_cost
    pre_margin_cost = base_cost + run_total + additional
    margin = margin_landed_percent / 100
    selling_price = pre_margin_cost / (1 - margin)
    profit = selling_price - pre_margin_cost
    profit_per_unit = profit / quantity_landed

    st.metric("ALL-IN COST (BEFORE MARGIN)", f"${pre_margin_cost:.2f}")
    st.metric("SELLING PRICE", f"${selling_price:.2f}")
    st.metric("PROFIT PER UNIT", f"${profit_per_unit:.2f}")
    st.metric("TOTAL PROFIT", f"${profit:.2f}")

# Tool 4: CALCULATE APPAREL SELLING PRICE
st.header("CALCULATE APPAREL SELLING PRICE")
st.markdown("#### SIZE-BASED QUANTITIES AND COSTS")

qty_xxs_to_xl = st.number_input("XXS TO XL QTY", min_value=0, step=1, key="qty_xxs_to_xl")
cost_xxs_to_xl = st.number_input("XXS TO XL ITEM COST", min_value=0.0, step=0.01, key="cost_xxs_to_xl")

qty_2xl = st.number_input("2XL QTY", min_value=0, step=1, key="qty_2xl")
cost_2xl = st.number_input("2XL ITEM COST", min_value=0.0, step=0.01, key="cost_2xl")

qty_3xl = st.number_input("3XL QTY", min_value=0, step=1, key="qty_3xl")
cost_3xl = st.number_input("3XL ITEM COST", min_value=0.0, step=0.01, key="cost_3xl")

qty_4xl = st.number_input("4XL QTY", min_value=0, step=1, key="qty_4xl")
cost_4xl = st.number_input("4XL ITEM COST", min_value=0.0, step=0.01, key="cost_4xl")

st.markdown("#### ADDITIONAL COSTS")
run_charge = st.number_input("RUN CHARGE", min_value=0.0, step=0.01, key="apparel_run")
shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, step=0.01, key="apparel_shipping")
sample_cost = st.number_input("SAMPLE COST", min_value=0.0, step=0.01, key="apparel_sample")
setup_cost = st.number_input("SETUP COST", min_value=0.0, step=0.01, key="apparel_setup")
margin_percent = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, step=0.1, key="apparel_margin")

total_units = qty_xxs_to_xl + qty_2xl + qty_3xl + qty_4xl
item_cost_total = (
    (qty_xxs_to_xl * cost_xxs_to_xl)
    + (qty_2xl * cost_2xl)
    + (qty_3xl * cost_3xl)
    + (qty_4xl * cost_4xl)
)
run_total = run_charge * total_units
additional_costs = shipping_cost + sample_cost + setup_cost + run_total
total_cost = item_cost_total + additional_costs

margin = margin_percent / 100 if margin_percent is not None else 0
avg_cost_per_unit = total_cost / total_units if total_units else 0
selling_price_per_unit = avg_cost_per_unit / (1 - margin) if margin < 1 else 0
total_selling_price = selling_price_per_unit * total_units
profit = total_selling_price - total_cost
profit_per_unit = profit / total_units if total_units else 0

st.metric("TOTAL UNITS", total_units)
st.metric("AVERAGE COST PER UNIT", f"${avg_cost_per_unit:.2f}")
st.metric("SELLING PRICE PER UNIT", f"${selling_price_per_unit:.2f}")
st.metric("PROFIT PER UNIT", f"${profit_per_unit:.2f}")
st.metric("TOTAL PROFIT", f"${profit:.2f}")

# Tool 5: DISCOUNT CODES REFERENCE
st.header("PQR SYSTEM DISCOUNT CODES")
st.markdown("Use the table below to reference discount thresholds...")
# (The actual discount code table would go here)

# Reset Button
if st.button("RESET ALL FIELDS"):
    st.experimental_rerun()
