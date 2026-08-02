from db import get_connection


def get_refresh_token():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT refresh_token
        FROM barrie.application_tokens
        WHERE provider='onedrive'
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        raise Exception("OneDrive refresh token not found.")

    return row[0]