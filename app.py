import streamlit as st


def calculate_selling_price_by_margin(total_cost, margin):
    price = total_cost / (1 - margin / 100) if margin < 100 else 0
    profit = price - total_cost
    return price, profit


def calculate_selling_price_by_landed(item_cost, shipping, sample_cost, qty, margin):
    total_cost = (item_cost + shipping + sample_cost) / qty if qty else 0
    price = total_cost / (1 - margin / 100) if margin < 100 else 0
    profit = price - total_cost
    return total_cost, price, profit


def calculate_margin_by_price(total_cost, selling_price):
    profit = selling_price - total_cost
    margin = (profit / selling_price) * 100 if selling_price else 0
    return margin, profit


def calculate_margin_by_landed(item_cost, shipping, sample_cost, qty, selling_price):
    total_cost = (item_cost + shipping + sample_cost) / qty if qty else 0
    profit = selling_price - total_cost
    margin = (profit / selling_price) * 100 if selling_price else 0
    return total_cost, margin, profit


def apply_discount(base_price, code, codes_dict):
    discount = codes_dict.get(code.upper(), 0)
    return base_price * (1 - discount)


st.title("Financial Calculator")

st.markdown("---")

st.header("Discount Codes")
codes_dict = {
    "A": 0.5, "B": 0.45, "C": 0.4, "D": 0.35, "E": 0.3, "F": 0.25, "G": 0.2, "H": 0.15,
    "I": 0.1, "J": 0.05, "X": 0.1, "L": 0.7, "M": 0.65, "N": 0.6, "O": 0.55, "P": 0.5,
    "Q": 0.45, "R": 0.4, "S": 0.35, "T": 0.3, "U": 0.25, "V": 0.2, "W": 0.15, "Y": 0.05, "Z": 0.0
}
st.write("Available discount codes:")
st.write("\n".join([f"{k}: {int(v * 100)}% off" for k, v in sorted(codes_dict.items())]))

st.markdown("---")

# --- Calculator 1: Selling Price by Margin ---
st.subheader("1. Selling Price by Margin")
total_cost_1 = st.number_input("Total Cost (Calculator 1)", key="cost1", min_value=0.0, value=0.0)
margin_1 = st.number_input("Desired Margin (%) (Calculator 1)", key="margin1", min_value=0.0, max_value=100.0, value=30.0)
discount_code_1 = st.text_input("Discount Code (optional)", key="disc1")
if st.button("Calculate (1)"):
    price, profit = calculate_selling_price_by_margin(total_cost_1, margin_1)
    discounted_price = apply_discount(price, discount_code_1, codes_dict)
    st.write(f"Selling Price: ${discounted_price:.2f} (after discount)")
    st.write(f"Profit: ${discounted_price - total_cost_1:.2f}")

# --- Calculator 2: Selling Price by Landed Cost ---
st.subheader("2. Selling Price by Landed Cost")
item_cost_2 = st.number_input("Item Cost (Calculator 2)", key="item2", min_value=0.0, value=0.0)
shipping_2 = st.number_input("Shipping Cost (Calculator 2)", key="ship2", min_value=0.0, value=0.0)
sample_cost_2 = st.number_input("Sample Cost (Calculator 2)", key="sample2", min_value=0.0, value=0.0)
qty_2 = st.number_input("Quantity (Calculator 2)", key="qty2", min_value=1, value=1)
margin_2 = st.number_input("Desired Margin (%) (Calculator 2)", key="margin2", min_value=0.0, max_value=100.0, value=30.0)
discount_code_2 = st.text_input("Discount Code (optional)", key="disc2")
if st.button("Calculate (2)"):
    total_cost, price, profit = calculate_selling_price_by_landed(item_cost_2, shipping_2, sample_cost_2, qty_2, margin_2)
    discounted_price = apply_discount(price, discount_code_2, codes_dict)
    st.write(f"Price per Unit (Total Cost): ${total_cost:.2f}")
    st.write(f"Selling Price: ${discounted_price:.2f} (after discount)")
    st.write(f"Profit: ${discounted_price - total_cost:.2f}")

# --- Calculator 3: Margin by Price ---
st.subheader("3. Margin by Price")
total_cost_3 = st.number_input("Total Cost (Calculator 3)", key="cost3", min_value=0.0, value=0.0)
selling_price_3 = st.number_input("Selling Price (Calculator 3)", key="price3", min_value=0.0, value=0.0)
if st.button("Calculate (3)"):
    margin, profit = calculate_margin_by_price(total_cost_3, selling_price_3)
    st.write(f"Margin: {margin:.2f}%")
    st.write(f"Profit: ${profit:.2f}")

# --- Calculator 4: Margin by Landed Cost ---
st.subheader("4. Margin by Landed Cost")
item_cost_4 = st.number_input("Item Cost (Calculator 4)", key="item4", min_value=0.0, value=0.0)
shipping_4 = st.number_input("Shipping Cost (Calculator 4)", key="ship4", min_value=0.0, value=0.0)
sample_cost_4 = st.number_input("Sample Cost (Calculator 4)", key="sample4", min_value=0.0, value=0.0)
qty_4 = st.number_input("Quantity (Calculator 4)", key="qty4", min_value=1, value=1)
selling_price_4 = st.number_input("Selling Price (Calculator 4)", key="price4", min_value=0.0, value=0.0)
if st.button("Calculate (4)"):
    total_cost, margin, profit = calculate_margin_by_landed(item_cost_4, shipping_4, sample_cost_4, qty_4, selling_price_4)
    st.write(f"Price per Unit (Total Cost): ${total_cost:.2f}")
    st.write(f"Margin: {margin:.2f}%")
    st.write(f"Profit: ${profit:.2f}")
