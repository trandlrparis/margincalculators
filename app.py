
import streamlit as st

st.set_page_config(page_title="Margin Calculators", layout="wide")

st.title("🧮 Margin Calculators")

# Reset fields functionality
if "reset" not in st.session_state:
    st.session_state.reset = False

def reset_all_fields():
    for key in list(st.session_state.keys()):
        if key != "reset":
            del st.session_state[key]
    st.session_state.reset = True

st.button("🔄 RESET ALL FIELDS", on_click=reset_all_fields)

# --- TOOL 1: Calculate Selling Price by Margin ---
st.header("CALCULATE SELLING PRICE BY MARGIN")
cost = st.number_input("ITEM COST", min_value=0.0, step=0.01, key="cost_margin")
margin = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, value=0.0, key="margin_margin")

if margin >= 100:
    st.error("Margin cannot be 100%")
else:
    try:
        selling_price = cost / (1 - (margin / 100))
        st.metric("SELLING PRICE", f"${selling_price:.2f}")
    except ZeroDivisionError:
        st.error("Invalid margin value")

# --- TOOL 2: Calculate Margin by Selling Price ---
st.header("CALCULATE MARGIN BY SELLING PRICE")
cost = st.number_input("ITEM COST", min_value=0.0, step=0.01, key="cost_margin2")
selling_price = st.number_input("SELLING PRICE", min_value=0.0, step=0.01, key="selling_margin2")

if selling_price > 0:
    margin = (selling_price - cost) / selling_price * 100
    st.metric("MARGIN %", f"{margin:.2f}%")

# --- TOOL 3: Calculate Selling Price by Landed Cost ---
st.header("CALCULATE SELLING PRICE BY LANDED COST")
item_cost = st.number_input("ITEM COST", min_value=0.0, step=0.01, key="lc_item_cost")
quantity = st.number_input("QUANTITY", min_value=0, step=1, key="lc_quantity")
run_charge = st.number_input("RUN CHARGE", min_value=0.0, step=0.01, key="lc_run_charge")
shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, step=0.01, key="lc_shipping_cost")
sample_cost = st.number_input("SAMPLE COST", min_value=0.0, step=0.01, key="lc_sample_cost")
setup_cost = st.number_input("SETUP COST", min_value=0.0, step=0.01, key="lc_setup_cost")
margin_percent = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, value=0.0, key="lc_margin")

if quantity > 0:
    try:
        item_cost_total = item_cost * quantity
        additional_costs = shipping_cost + sample_cost + setup_cost + (run_charge * quantity)
        total_cost = item_cost_total + additional_costs
        margin = margin_percent / 100 if margin_percent is not None else 0
        avg_cost_per_unit = total_cost / quantity if quantity else 0
        selling_price = avg_cost_per_unit / (1 - margin) if margin < 1 else 0
        profit_per_unit = selling_price - avg_cost_per_unit
        total_profit = profit_per_unit * quantity

        st.metric("ALL-IN COST (BEFORE MARGIN)", f"${total_cost:,.2f}")
        st.metric("COST PER UNIT", f"${avg_cost_per_unit:.2f}")
        st.metric("SELLING PRICE", f"${selling_price:.2f}")
        st.metric("PROFIT PER UNIT", f"${profit_per_unit:.2f}")
        st.metric("TOTAL PROFIT", f"${total_profit:,.2f}")
    except Exception as e:
        st.error(f"Error in calculation: {e}")

# --- TOOL 4: Calculate Apparel Selling Price ---
st.header("CALCULATE APPAREL SELLING PRICE")
cost_xxs_to_xl = st.number_input("XXS TO XL ITEM COST", min_value=0.0, step=0.01, key="cost_xxs_to_xl")
qty_xxs_to_xl = st.number_input("XXS TO XL QTY", min_value=0, step=1, key="qty_xxs_to_xl")
cost_2xl = st.number_input("2XL ITEM COST", min_value=0.0, step=0.01, key="cost_2xl")
qty_2xl = st.number_input("2XL QTY", min_value=0, step=1, key="qty_2xl")
cost_3xl = st.number_input("3XL ITEM COST", min_value=0.0, step=0.01, key="cost_3xl")
qty_3xl = st.number_input("3XL QTY", min_value=0, step=1, key="qty_3xl")
cost_4xl = st.number_input("4XL ITEM COST", min_value=0.0, step=0.01, key="cost_4xl")
qty_4xl = st.number_input("4XL QTY", min_value=0, step=1, key="qty_4xl")

st.markdown("### ADDITIONAL COSTS")
run_charge = st.number_input("RUN CHARGE", min_value=0.0, step=0.01, key="apparel_run_charge")
shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, step=0.01, key="apparel_shipping")
sample_cost = st.number_input("SAMPLE COST", min_value=0.0, step=0.01, key="apparel_sample")
setup_cost = st.number_input("SETUP COST", min_value=0.0, step=0.01, key="apparel_setup")
margin_percent = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, value=0.0, key="apparel_margin")

try:
    total_units = qty_xxs_to_xl + qty_2xl + qty_3xl + qty_4xl
    total_cost = (
        (cost_xxs_to_xl * qty_xxs_to_xl) +
        (cost_2xl * qty_2xl) +
        (cost_3xl * qty_3xl) +
        (cost_4xl * qty_4xl) +
        (run_charge * total_units) +
        shipping_cost +
        sample_cost +
        setup_cost
    )

    margin = margin_percent / 100 if margin_percent is not None else 0
    avg_cost_per_unit = total_cost / total_units if total_units else 0
    avg_selling_price = avg_cost_per_unit / (1 - margin) if margin < 1 else 0
    profit_per_unit = avg_selling_price - avg_cost_per_unit
    total_profit = profit_per_unit * total_units

    st.metric("UNITS", total_units)
    st.metric("AVG COST PER UNIT", f"${avg_cost_per_unit:.2f}")
    st.metric("AVG SELLING PRICE PER UNIT", f"${avg_selling_price:.2f}")
    st.metric("PROFIT PER UNIT", f"${profit_per_unit:.2f}")
    st.metric("TOTAL PROFIT", f"${total_profit:,.2f}")
except Exception as e:
    st.error(f"Error in apparel calculation: {e}")

# --- TOOL 5: Reference Discount Codes ---
st.header("📘 PQR SYSTEM DISCOUNT CODES")
st.markdown("""
- **A**: 1000 pcs or more
- **B**: 500-999 pcs
- **C**: 250-499 pcs
- **D**: 100-249 pcs
- **E**: 50-99 pcs
- **F**: 25-49 pcs
- **G**: 10-24 pcs
- **H**: 5-9 pcs
- **I**: 2-4 pcs
""")

