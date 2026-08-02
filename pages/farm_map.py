from auth.session import is_logged_in

if not is_logged_in():

    st.warning("Please login.")

    st.stop()

import streamlit as st
import folium

from streamlit_folium import st_folium

from repositories.farm_repository import get_farm_locations


st.title("🗺 Farm Map")

st.write("Farm Map page loaded.")

farms = get_farm_locations()


if farms.empty:

    st.warning("No farm locations available.")

    st.stop()


# Center the map on the average farm location

center_lat = farms["gps_latitude"].mean()

center_lon = farms["gps_longitude"].mean()


m = folium.Map(

    location=[center_lat, center_lon],

    zoom_start=12,

    control_scale=True

)


for _, row in farms.iterrows():

    popup = f"""
    <b>{row['farm_code']}</b><br>

    Farm: {row['farm_name']}<br>

    Elevation: {row['elevation_meters']} m<br>

    Organic: {"Yes" if row["organic"] else "No"}
    """

    folium.Marker(

        location=[
            row["gps_latitude"],
            row["gps_longitude"]
        ],

        popup=popup,

        tooltip=row["farm_name"],

        icon=folium.Icon(
            color="green",
            icon="leaf"
        )

    ).add_to(m)


st_folium(

    m,

    width=1200,

    height=700
)