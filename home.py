import streamlit as st

st.set_page_config(
    page_title="Barrie Coffee Management System",
    page_icon="☕",
    layout="wide",
)

st.title("☕ Barrie Coffee Management System")

st.markdown(
    """
    ### Welcome!

    Manage your coffee operations from one place.

    - 👨‍🌾 Farmer Registration
    - 🌱 Farm Management
    - 🗺️ Farm Mapping
    - ☕ Coffee Collection
    - 🛒 Purchases
    - 💰 Payments
    - 📄 Receipts
    """
)

st.info(
    """
    **Welcome to Barrie Coffee Management System**

    እንኳን ወደ **ባሬ ኮፊ አስተዳደር ስርዓት**
    በደህና መጡ።
    """
)

st.divider()

st.caption(
    "Version 1.0 • Barrie Coffee • Built with Streamlit & PostgreSQL"
)