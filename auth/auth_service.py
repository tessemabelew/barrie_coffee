import bcrypt
import streamlit as st
from db import get_connection


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        password_hash.encode()
    )


def login(username, password):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            user_id,
            username,
            password_hash,
            full_name,
            role,
            active
        FROM barrie.users
        WHERE username = %s
    """, (username,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return False

    if not user[5]:
        return False

    if not verify_password(password, user[2]):
        return False

    st.session_state.user = {
        "user_id": user[0],
        "username": user[1],
        "full_name": user[3],
        "role": user[4]
    }

    return True


def logout():

    if "user" in st.session_state:
        del st.session_state["user"]