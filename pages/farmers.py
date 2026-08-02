from auth.session import is_logged_in

if not is_logged_in():

    st.warning("Please login.")

    st.stop()

import streamlit as st

from repositories.farmer_repository import (
    insert_farmer,
    get_all_farmers,
    search_farmers
)

st.title("👨‍🌾 Farmer Management")

tab1, tab2 = st.tabs(
    [
        "➕ Add Farmer",
        "📋 Farmer List"
    ]
)

##################################
# ADD FARMER
##################################

with tab1:

    with st.form("farmer_form"):

        first_name = st.text_input("First Name")

        last_name = st.text_input("Last Name")

        phone = st.text_input("Phone")

        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Save Farmer")

        if submitted:

            farmer_code = insert_farmer(
                first_name,
                last_name,
                phone,
                notes
            )

            st.success(
                f"Farmer saved successfully ({farmer_code})"
            )

##################################
# FARMER LIST
##################################


with tab2:

    # Search box
    search = st.text_input("🔍 Search Farmer")

    if search:
        farmers = search_farmers(search)
    else:
        farmers = get_all_farmers()

        # Dashboard Metrics
    inactive = len(farmers) - farmers["active"].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Farmers", len(farmers))

    with col2:
        st.metric("Active Farmers", farmers["active"].sum())

    with col3:
        st.metric("Inactive Farmers", inactive)

    # Display the results
if farmers.empty:
    st.warning("No farmers found.")
else:
    st.dataframe(
        farmers,
        use_container_width=True,
        hide_index=True
    )