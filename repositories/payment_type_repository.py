import pandas as pd
from db import get_connection
from psycopg2.errors import UniqueViolation


# ==================================================
# INSERT
# ==================================================

def insert_payment_type(
    payment_type_name,
    payment_category,
    description
):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO barrie.payment_types
            (
                payment_type_name,
                payment_category,
                description
            )
            VALUES
            (%s,%s,%s)
            RETURNING payment_type_id;
            """,
            (
                payment_type_name,
                payment_category,
                description
            )
        )

        payment_type_id = cur.fetchone()[0]

        conn.commit()

        return payment_type_id

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ==================================================
# SELECT
# ==================================================

def get_all_payment_types():

    conn = get_connection()

    query = """
        SELECT

            payment_type_id,
            payment_type_name,
            payment_category,
            COALESCE(description,'') AS description,
            active

        FROM barrie.payment_types

        ORDER BY payment_category,
                 payment_type_name;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def search_payment_types(search):

    conn = get_connection()

    query = """
        SELECT

            payment_type_id,
            payment_type_name,
            payment_category,
            COALESCE(description,'') AS description,
            active

        FROM barrie.payment_types

        WHERE

            payment_type_name ILIKE %s

            OR payment_category ILIKE %s

            OR description ILIKE %s

        ORDER BY payment_category,
                 payment_type_name;
    """

    value = f"%{search}%"

    df = pd.read_sql(
        query,
        conn,
        params=(value, value, value)
    )

    conn.close()

    return df


def get_payment_type(payment_type_id):

    payment_type_id = int(payment_type_id)

    conn = get_connection()

    query = """
        SELECT *

        FROM barrie.payment_types

        WHERE payment_type_id=%s;
    """

    df = pd.read_sql(
        query,
        conn,
        params=(payment_type_id,)
    )

    conn.close()

    return df.iloc[0]


# ==================================================
# UPDATE
# ==================================================

def update_payment_type(
    payment_type_id,
    payment_type_name,
    payment_category,
    description
):

    payment_type_id = int(payment_type_id)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE barrie.payment_types

        SET

            payment_type_name=%s,
            payment_category=%s,
            description=%s,
            updated_at=CURRENT_TIMESTAMP

        WHERE payment_type_id=%s;
        """,
        (
            payment_type_name,
            payment_category,
            description,
            payment_type_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()


# ==================================================
# DEACTIVATE
# ==================================================

def deactivate_payment_type(payment_type_id):

    payment_type_id = int(payment_type_id)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE barrie.payment_types

        SET

            active=FALSE,
            updated_at=CURRENT_TIMESTAMP

        WHERE payment_type_id=%s;
        """,
        (payment_type_id,)
    )

    conn.commit()

    cur.close()
    conn.close()


# ==================================================
# DROPDOWN
# ==================================================

def get_payment_type_dropdown():

    conn = get_connection()

    query = """
        SELECT

            payment_type_id,
            payment_type_name

        FROM barrie.payment_types

        WHERE active = TRUE

        ORDER BY
            payment_category,
            payment_type_name;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df