import streamlit as st

home = st.Page(
    "home.py",
    title="Home",
    icon="🏠"
)

farmers = st.Page(
    "pages/farmers.py",
    title="Farmers",
    icon="👨‍🌾"
)

# Add this block
farms = st.Page(
    "pages/farms.py",
    title="Farms",
    icon="🌱"
)

farm_map = st.Page(
    "pages/farm_map.py",
    title="Farm Map",
    icon="🗺"
)

payment_types = st.Page(
    "pages/payment_types.py",
    title="Payment Types",
    icon="💳"
)

payment_page = st.Page(
    "pages/payments.py",
    title="Payments",
    icon="💵"
)
coffee_forms = st.Page(
    "pages/coffee_forms.py",
    title="Coffee Forms",
    icon="☕"
)

purchases = st.Page(
    "pages/purchases.py",
    title="Purchases",
    icon="🛒"
)

payment_page = st.Page(
    "pages/payments.py",
    title="Payments",
    icon="💰",
)

# Update this line
pg = st.navigation([
    home,
    farmers,
    farms,
    farm_map,
    coffee_forms,
    purchases,
    payment_types,
    payment_page
])

st.set_page_config(
    page_title="Barrie Coffee",
    page_icon="☕",
    layout="wide"
)

pg.run()