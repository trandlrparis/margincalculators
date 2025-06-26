
import streamlit as st

# Reset function
def reset_fields():
    st.session_state.clear()

st.set_page_config(layout="wide")

st.markdown("# **FINANCIAL CALCULATORS**")
st.button("🔁 RESET ALL FIELDS", on_click=reset_fields)

# --- 1. Selling Price by Margin ---
with st.expander("1️⃣ CALCULATE SELLING PRICE BY MARGIN", expanded=False):
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

# --- 2. Calculate Margin by Selling Price ---
with st.expander("2️⃣ CALCULATE MARGIN BY SELLING PRICE", expanded=False):
    with st.container():
        cost = st.number_input("COST", min_value=0.0, key="cost_margin", value=None, placeholder="")
        price = st.number_input("SELLING PRICE", min_value=0.0, key="price_margin", value=None, placeholder="")

        if cost is not None and price is not None and price > 0:
            margin = (price - cost) / price * 100
        else:
            margin = 0.0

        st.metric("MARGIN %", f"{margin:.2f}%")

# --- 3. Selling Price by Landed Cost ---
with st.expander("3️⃣ CALCULATE SELLING PRICE BY LANDED COST", expanded=False):
    with st.container():
        item_cost = st.number_input("ITEM COST", min_value=0.0, key="landed_item", value=None, placeholder="")
        shipping_cost = st.number_input("SHIPPING COST", min_value=0.0, key="landed_shipping", value=0.0, placeholder="")
        sample_cost = st.number_input("SAMPLE COST", min_value=0.0, key="landed_sample", value=0.0, placeholder="")
        setup_cost = st.number_input("SETUP COST", min_value=0.0, key="landed_setup", value=0.0, placeholder="")
        run_charge = st.number_input("RUN CHARGE", min_value=0.0, key="landed_run", value=0.0, placeholder="")
        quantity = st.number_input("QTY", min_value=1, key="landed_qty", value=None, placeholder="")
        margin2 = st.number_input("MARGIN %", min_value=0.0, max_value=99.9, key="landed_margin", value=None, placeholder="")

        if all(v is not None for v in [item_cost, quantity, margin2]) and quantity > 0 and margin2 < 100:
            total_cost = item_cost * quantity + shipping_cost + sample_cost + setup_cost + (run_charge * quantity)
            selling_price = total_cost / (1 - margin2 / 100)
        else:
            total_cost = selling_price = 0.0

        st.metric("TOTAL COST", f"${total_cost:.2f}")
        st.metric("SELLING PRICE", f"${selling_price:.2f}")

# --- 4. Apparel Selling Price Tool ---
with st.expander("4️⃣ CALCULATE APPAREL SELLING PRICE", expanded=False):
    with st.container():
        st.markdown("### Size-Based Quantity and Cost Inputs")
        col1, col2 = st.columns(2)
        with col1:
            qty_xxs_to_xl = st.number_input("XXS–XL Quantity", min_value=0, value=0, key="qty_xxs_to_xl")
            qty_2xl = st.number_input("2XL Quantity", min_value=0, value=0, key="qty_2xl")
            qty_3xl = st.number_input("3XL Quantity", min_value=0, value=0, key="qty_3xl")
            qty_4xl = st.number_input("4XL Quantity", min_value=0, value=0, key="qty_4xl")
        with col2:
            cost_xxs_to_xl = st.number_input("XXS–XL Unit Cost", min_value=0.0, value=0.0, key="cost_xxs_to_xl")
            cost_2xl = st.number_input("2XL Unit Cost", min_value=0.0, value=0.0, key="cost_2xl")
            cost_3xl = st.number_input("3XL Unit Cost", min_value=0.0, value=0.0, key="cost_3xl")
            cost_4xl = st.number_input("4XL Unit Cost", min_value=0.0, value=0.0, key="cost_4xl")

        st.markdown("### Additional Cost Inputs")
        shipping_cost = st.number_input("Shipping Cost", min_value=0.0, value=0.0, key="apparel_shipping_cost")
        sample_cost = st.number_input("Sample Cost", min_value=0.0, value=0.0, key="apparel_sample_cost")
        setup_cost = st.number_input("Setup Cost", min_value=0.0, value=0.0, key="apparel_setup_cost")
        run_charge = st.number_input("Run Charge per Unit", min_value=0.0, value=0.0, key="apparel_run_charge")
        margin = st.number_input("Margin (e.g., 0.4 for 40%)", min_value=0.0, max_value=0.99, value=0.4, key="apparel_margin")

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

        st.markdown(f"**Total Units:** {total_units}")
        st.markdown(f"**Item Cost Total:** ${item_cost_total:,.2f}")
        st.markdown(f"**Run Charge Total:** ${run_charge_total:,.2f}")
        st.markdown(f"**All-In Cost (Before Margin):** ${pre_margin_cost:,.2f}")
        st.markdown(f"**Selling Price (After Margin):** ${selling_price:,.2f}")

# --- 5. Calculate Vendor Pricing Tool ---
with st.expander("5️⃣ CALCULATE VENDOR PRICING", expanded=False):
    with st.container():
        net_price = st.number_input("ENTER NET PRICE", min_value=0.0, key="vendor_net", value=None, placeholder="")
        top_code = st.selectbox("Top Code", options=[""] + list("ABCDEFGHIJX"), index=0, key="vendor_top")
        bottom_code = st.selectbox("Bottom Code", options=[""] + list("LMNOPQRSTUVWXYZ"), index=0, key="vendor_bottom")

        top_discount = {"A": 0.5, "B": 0.45, "C": 0.4, "D": 0.35, "E": 0.3,
                        "F": 0.25, "G": 0.2, "H": 0.15, "I": 0.1, "J": 0.05, "X": 0.0}.get(top_code, 0)
        bottom_discount = {"L": 0.7, "M": 0.65, "N": 0.6, "O": 0.55, "P": 0.5,
                           "Q": 0.45, "R": 0.4, "S": 0.35, "T": 0.3, "U": 0.25,
                           "V": 0.2, "W": 0.15, "Y": 0.05, "Z": 0.0}.get(bottom_code, 0)

        if net_price and top_code and bottom_code:
            list_price = net_price / ((1 - top_discount) * (1 - bottom_discount))
        else:
            list_price = 0.0

        st.metric("LIST PRICE", f"${list_price:.2f}")
