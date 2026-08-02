import streamlit as st
from auth.session import is_logged_in

if not is_logged_in():

    st.warning("Please login.")

    st.stop()


from streamlit_geolocation import streamlit_geolocation

from repositories.farm_repository import (
    insert_farm,
    get_all_farms,
    search_farms,
    get_farmer_dropdown,
    get_farm,
    update_farm,
    deactivate_farm
)

st.title("🌱 Farm Management")

tab1, tab2, tab3 = st.tabs([
    "➕ Add Farm",
    "📋 Farm List",
    "✏ Edit Farm"
])

# -----------------------
# Add Farm
# -----------------------

with tab1:

    farmers = get_farmer_dropdown()

    farmer = st.selectbox(
        "Farmer",
        farmers,
        format_func=lambda x: x[1]
    )

    farm_name = st.text_input("Farm Name")

    farm_number = st.text_input("Farm Number")

    farm_size = st.number_input(
        "Farm Size (Hectares)",
        min_value=0.0,
        step=0.1
    )

    elevation = st.number_input(
        "Elevation (Meters)",
        min_value=0,
        step=10
    )

    organic = st.checkbox(
        "Organic",
        key="add_organic"
    )

    notes = st.text_area("Notes")

    st.subheader("📍 Farm GPS Location")

    location = streamlit_geolocation()

    st.write(location)

    if location:

        st.session_state["gps_latitude"] = location.get("latitude")
        st.session_state["gps_longitude"] = location.get("longitude")
        st.session_state["gps_accuracy"] = location.get("accuracy") 

        st.write("Latitude:", st.session_state.get("gps_latitude"))
        st.write("Longitude:", st.session_state.get("gps_longitude"))

    if st.button("💾 Save Farm"):

        st.write("Saving...")
        st.write(st.session_state.get("gps_latitude"))
        st.write(st.session_state.get("gps_longitude"))

        code = insert_farm(
            farmer[0],
            farm_name,
            farm_number,
            farm_size,
            elevation,
            organic,
            notes,
            st.session_state.get("gps_latitude"),
            st.session_state.get("gps_longitude"),
            st.session_state.get("gps_accuracy")
        )

        st.success(f"Farm created successfully ({code})")

# -----------------------
# Farm List
# -----------------------

with tab2:

    # Search
    search = st.text_input("🔍 Search Farm")

    if search:
        farms = search_farms(search)
    else:
        farms = get_all_farms()

    # Dashboard Metrics
    total = len(farms)

    if farms.empty:
        active = 0
    else:
        active = farms["active"].sum()

    inactive = total - active

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Farms", total)

    with col2:
        st.metric("Active Farms", active)

    with col3:
        st.metric("Inactive Farms", inactive)

    st.divider()

    if farms.empty:

        st.warning("No farms found.")

    else:

        # Friendly column names
        display = farms.rename(
            columns={
                "farm_code": "Farm Code",
                "farmer_code": "Farmer Code",
                "farmer": "Farmer",
                "farm_name": "Farm Name",
                "farm_number": "Farm Number",
                "farm_size_hectares": "Size (Ha)",
                "elevation_meters": "Elevation",
                "organic": "Organic",
                "active": "Active"
            }
        )
        display["Organic"] = display["Organic"].map(
            {True: "Yes", False: "No"}
        )

        display["Active"] = display["Active"].map(
            {True: "Yes", False: "No"}
        )
        display["Size (Ha)"] = display["Size (Ha)"].map(
            lambda x: f"{x:.2f}"
        )
        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )
        st.subheader("📍 View Farms on Google Maps")

        for _, row in farms.iterrows():

            if row["gps_latitude"] and row["gps_longitude"]:

                google_url = (
                    f"https://maps.google.com/?q="
                    f"{row['gps_latitude']},{row['gps_longitude']}"
                )

                st.write(f"**{row['farm_code']} - {row['farm_name']}**")

                st.link_button("📍 View Map", google_url)

with tab3:

    farms = get_all_farms()

    selected = st.selectbox(
        "Select Farm",
        farms["farm_code"]
    )

    farm = farms.loc[
        farms["farm_code"] == selected
    ].iloc[0]

    details = get_farm(
        farm["farm_id"]
    )

    farm_name = st.text_input(
        "Farm Name",
        value=details["farm_name"]
    )

    farm_number = st.text_input(
        "Farm Number",
        value=details["farm_number"]
    )

    farm_size = st.number_input(
        "Farm Size",
        value=float(details["farm_size_hectares"])
    )

    elevation = st.number_input(
        "Elevation",
        value=int(details["elevation_meters"])
    )

    organic = st.checkbox(
        "Organic",
        value=details["organic"],
        key="edit_organic"
    )

    notes = st.text_area(
        "Notes",
        value=details["notes"]
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("💾 Update Farm"):

            update_farm(
                int(details["farm_id"]),
                farm_name,
                farm_number,
                float(farm_size),
                int(elevation),
                bool(organic),
                notes
            )

            st.success("Farm updated.")

    with col2:

        if st.button("🚫 Deactivate Farm"):

            deactivate_farm(
                int(details["farm_id"])
            )

            st.success("Farm deactivated.")