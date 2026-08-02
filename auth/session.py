import streamlit as st


def is_logged_in():

    return "user" in st.session_state


def current_user():

    return st.session_state.get("user")