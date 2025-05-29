
import streamlit as st

def calculate_selling_price_by_margin(total_cost, margin):
    price = total_cost / (1 - margin / 100)
    profit = price - total_cost
    return price, profit

def calculate_selling_price_by_landed(item_cost, shipping, sample_cost, qty, margin):
    total_cost = (item_cost + shipping + sample_cost) / qty
    price = total_cost / (1 - margin / 100)
    profit = price - total_cost
    return total_cost, price, profit

def calculate_margin_by_price(total_cost, selling_price):
    profit = selling_price - total_cost
    margin = (profit / selling_price) * 100 if selling_price else 0
    return margin, profit

def calculate_margin_by_landed(item_cost, shipping, sample_cost, qty, selling_price):
    total_cost = (item_cost + shipping + sample_cost) / qty
    profit = selling_price - total_cost
    margin = (profit / selling_price) * 100 if selling_price else 0
    return total_cost, margin, profit

st.title("Financial Calculator")

calc_type = st.radio("Choose a Calculator", [
    "Selling Price by Margin",
    "Selling Price by Landed Cost",
    "Margin by Price",
    "Margin by Landed Cost"
])

if calc_type == "Selling Price by Margin":
    total_cost = st.number_input("Total Cost", min_value=0.0, value=0.0)
    margin = st.number_input("Desired Margin (%)", min_value=0.0, max_value=100.0, value=30.0)
    if st.button("Calculate"):
        price, profit = calculate_selling_price_by_margin(total_cost, margin)
        st.write(f"**Selling Price:** ${price:.2f}")
        st.write(f"**Profit:** ${profit:.2f}")

elif calc_type == "Selling Price by Landed Cost":
    item_cost = st.number_input("Item Cost", min_value=0.0, value=0.0)
    shipping = st.number_input("Shipping Cost", min_value=0.0, value=0.0)
    sample_cost = st.number_input("Sample Cost", min_value=0.0, value=0.0)
    qty = st.number_input("Quantity", min_value=1, value=1)
    margin = st.number_input("Desired Margin (%)", min_value=0.0, max_value=100.0, value=30.0)
    if st.button("Calculate"):
        total_cost, price, profit = calculate_selling_price_by_landed(item_cost, shipping, sample_cost, qty, margin)
        st.write(f"**Price per Unit (Total Cost):** ${total_cost:.2f}")
        st.write(f"**Selling Price:** ${price:.2f}")
        st.write(f"**Profit:** ${profit:.2f}")

elif calc_type == "Margin by Price":
    total_cost = st.number_input("Total Cost", min_value=0.0, value=0.0)
    selling_price = st.number_input("Selling Price", min_value=0.0, value=0.0)
    if st.button("Calculate"):
        margin, profit = calculate_margin_by_price(total_cost, selling_price)
        st.write(f"**Margin:** {margin:.2f}%")
        st.write(f"**Profit:** ${profit:.2f}")

elif calc_type == "Margin by Landed Cost":
    item_cost = st.number_input("Item Cost", min_value=0.0, value=0.0)
    shipping = st.number_input("Shipping Cost", min_value=0.0, value=0.0)
    sample_cost = st.number_input("Sample Cost", min_value=0.0, value=0.0)
    qty = st.number_input("Quantity", min_value=1, value=1)
    selling_price = st.number_input("Selling Price", min_value=0.0, value=0.0)
    if st.button("Calculate"):
        total_cost, margin, profit = calculate_margin_by_landed(item_cost, shipping, sample_cost, qty, selling_price)
        st.write(f"**Price per Unit (Total Cost):** ${total_cost:.2f}")
        st.write(f"**Margin:** {margin:.2f}%")
        st.write(f"**Profit:** ${profit:.2f}")
