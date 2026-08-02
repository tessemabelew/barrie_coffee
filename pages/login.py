import streamlit as st
from auth.auth_service import login

st.title("Barrie Coffee Login")

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login"):

    if login(username, password):

        st.success("Welcome!")

        st.rerun()

    else:

        st.error("Invalid username or password")