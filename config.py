import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st

    if "database" in st.secrets:
        DB_CONFIG = {
            "host": st.secrets["database"]["host"],
            "port": st.secrets["database"]["port"],
            "dbname": st.secrets["database"]["dbname"],
            "user": st.secrets["database"]["user"],
            "password": st.secrets["database"]["password"],
            "sslmode": st.secrets["database"].get("sslmode", "require"),
        }
    else:
        raise KeyError

except Exception:
    DB_CONFIG = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "sslmode": os.getenv("DB_SSLMODE", "prefer"),
    }