# Rebuilding correct version of the margin calculator app.
import streamlit as st
import math

st.set_page_config(page_title='Margin Calculators', layout='wide')
st.title('🧮 MARGIN CALCULATOR TOOLS')


# TOOL 1: Selling Price by Margin
with st.expander('CALCULATE SELLING PRICE BY MARGIN', expanded=False):
    cost = st.number_input('ITEM COST', min_value=0.0, step=0.01, key='spbm_cost')
    margin_percent = st.number_input('MARGIN %', min_value=0.0, max_value=99.9, value=40.0, step=0.1, key='spbm_margin')
    if margin_percent != 100:
        margin = margin_percent / 100
        try:
            selling_price = cost / (1 - margin)
            st.metric('SELLING PRICE', f'${selling_price:,.2f}')
            except ZeroDivisionError:
                st.error('Margin cannot be 100%')

                # TOOL 2: Calculate Margin by Selling Price
                with st.expander('CALCULATE MARGIN BY SELLING PRICE', expanded=False):
                    cost2 = st.number_input('ITEM COST', min_value=0.0, step=0.01, key='mbsp_cost')
                    selling_price2 = st.number_input('SELLING PRICE', min_value=0.0, step=0.01, key='mbsp_price')
                    if selling_price2 > 0:
                        margin = (selling_price2 - cost2) / selling_price2
                        st.metric('MARGIN %', f'{margin * 100:.2f}%')

                        # TOOL 3: Selling Price by Landed Cost
                        with st.expander('CALCULATE SELLING PRICE BY LANDED COST', expanded=False):
                            item_cost = st.number_input('ITEM COST', min_value=0.0, step=0.01, key='lc_item_cost')
                            quantity = st.number_input('QUANTITY', min_value=1, step=1, key='lc_quantity')
                            run_charge = st.number_input('RUN CHARGE', min_value=0.0, step=0.01, key='lc_run_charge')
                            shipping_cost = st.number_input('SHIPPING COST', min_value=0.0, step=0.01, key='lc_shipping')
                            sample_cost = st.number_input('SAMPLE COST', min_value=0.0, step=0.01, key='lc_sample')
                            setup_cost = st.number_input('SETUP COST', min_value=0.0, step=0.01, key='lc_setup')
                            margin_percent = st.number_input('MARGIN %', min_value=0.0, max_value=99.9, value=40.0, step=0.1, key='lc_margin')
                            if margin_percent != 100 and quantity > 0:
                                margin = margin_percent / 100
                                pre_margin_cost = (item_cost * quantity) + shipping_cost + sample_cost + setup_cost + (run_charge * quantity)
                                all_in_cost_per_unit = pre_margin_cost / quantity
                                selling_price = all_in_cost_per_unit / (1 - margin)
                                profit_per_unit = selling_price - all_in_cost_per_unit
                                total_profit = profit_per_unit * quantity
                                st.metric('ALL-IN COST (BEFORE MARGIN)', f'${pre_margin_cost:,.2f}')
                                st.metric('SELLING PRICE', f'${selling_price:,.2f}')
                                st.metric('PROFIT PER UNIT', f'${profit_per_unit:,.2f}')
                                st.metric('TOTAL PROFIT', f'${total_profit:,.2f}')

                                # TOOL 4: Calculate Apparel Selling Price
                                with st.expander('CALCULATE APPAREL SELLING PRICE', expanded=False):
                                    st.markdown('#### SIZE-BASED QUANTITIES AND COSTS')
                                    qty_xxs_to_xl = st.number_input('XXS TO XL QTY', min_value=0, step=1, key='qty_xxs_to_xl')
                                    cost_xxs_to_xl = st.number_input('XXS TO XL ITEM COST', min_value=0.0, step=0.01, key='cost_xxs_to_xl')
                                    qty_2xl = st.number_input('2XL QTY', min_value=0, step=1, key='qty_2xl')
                                    cost_2xl = st.number_input('2XL ITEM COST', min_value=0.0, step=0.01, key='cost_2xl')
                                    qty_3xl = st.number_input('3XL QTY', min_value=0, step=1, key='qty_3xl')
                                    cost_3xl = st.number_input('3XL ITEM COST', min_value=0.0, step=0.01, key='cost_3xl')
                                    qty_4xl = st.number_input('4XL QTY', min_value=0, step=1, key='qty_4xl')
                                    cost_4xl = st.number_input('4XL ITEM COST', min_value=0.0, step=0.01, key='cost_4xl')

                                    st.markdown('#### ADDITIONAL COSTS')
                                    run_charge = st.number_input('RUN CHARGE', min_value=0.0, step=0.01, key='apparel_run_charge')
                                    shipping_cost = st.number_input('SHIPPING COST', min_value=0.0, step=0.01, key='apparel_shipping')
                                    sample_cost = st.number_input('SAMPLE COST', min_value=0.0, step=0.01, key='apparel_sample')
                                    setup_cost = st.number_input('SETUP COST', min_value=0.0, step=0.01, key='apparel_setup')
                                    margin_percent = st.number_input('MARGIN %', min_value=0.0, max_value=99.9, step=0.1, key='apparel_margin')

                                    if any([qty_xxs_to_xl, qty_2xl, qty_3xl, qty_4xl]):
                                        total_units = qty_xxs_to_xl + qty_2xl + qty_3xl + qty_4xl
                                        item_cost_total = (
                                        (qty_xxs_to_xl * cost_xxs_to_xl)
                                        + (qty_2xl * cost_2xl)
                                        + (qty_3xl * cost_3xl)
                                        + (qty_4xl * cost_4xl)
                                        )
                                        additional_costs = shipping_cost + sample_cost + setup_cost + (run_charge * total_units)
                                        total_cost = item_cost_total + additional_costs if 'additional_costs' in locals() else item_cost_total
                                        margin = margin_percent / 100 if margin_percent is not None else 0
                                        avg_cost_per_unit = total_cost / total_units if total_units else 0
                                        avg_selling_price_per_unit = avg_cost_per_unit / (1 - margin) if margin < 1 else 0
                                        profit_per_unit = avg_selling_price_per_unit - avg_cost_per_unit
                                        total_selling_price = avg_selling_price_per_unit * total_units
                                        total_profit = total_selling_price - total_cost
                                        st.metric('TOTAL UNITS', f'{total_units:,}')
                                        st.metric('TOTAL COST', f'${total_cost:,.2f}')
                                        st.metric('SELLING PRICE', f'${total_selling_price:,.2f}')
                                        st.metric('PROFIT PER UNIT', f'${profit_per_unit:,.2f}')
                                        st.metric('TOTAL PROFIT', f'${total_profit:,.2f}')
                                        st.metric('AVG COST PER UNIT', f'${avg_cost_per_unit:,.2f}')
                                        st.metric('AVG SELLING PRICE PER UNIT', f'${avg_selling_price_per_unit:,.2f}')

                                        # TOOL 5: Vendor Pricing Notes
                                        with st.expander('REFERENCE: VENDOR PRICING NOTES', expanded=False):
                                            st.markdown('''
                                            - Gildan pricing includes all sizes up to 5XL.
                                            - Comfort Colors 6014: Upcharge for sizes 2XL and above.
                                            - Next Level 3600: 2XL and up has a higher base cost.
                                            ''')

                                            # TOOL 6: PQR System Discount Codes
                                            with st.expander('REFERENCE: PQR SYSTEM DISCOUNT CODES', expanded=False):
                                                st.markdown('''
                                                **STANDARD DISCOUNTS**
                                                - P100: 0%
                                                - P80: 20%
                                                - P60: 40%
                                                - P50: 50%
                                                - P40: 60%
                                                - P30: 70%
                                                ''')
