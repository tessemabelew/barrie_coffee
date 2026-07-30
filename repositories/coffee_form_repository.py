import pandas as pd

from db import get_connection


# ======================================================
# INSERT
# ======================================================

def insert_coffee_form(
    coffee_form_name,
    description,
    active=True,
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO barrie.coffee_forms
        (
            coffee_form_name,
            description,
            active
        )
        VALUES
        (
            %s,%s,%s
        );
        """,
        (
            coffee_form_name,
            description,
            active,
        ),
    )

    conn.commit()

    cur.close()
    conn.close()


# ======================================================
# SELECT
# ======================================================

def get_all_coffee_forms():

    conn = get_connection()

    query = """
        SELECT

            coffee_form_id,
            coffee_form_name,
            COALESCE(description,'') AS description,
            active

        FROM barrie.coffee_forms

        WHERE active = TRUE

        ORDER BY coffee_form_name;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def search_coffee_forms(search):

    conn = get_connection()

    query = """
        SELECT

            coffee_form_id,
            coffee_form_name,
            description,
            active

        FROM barrie.coffee_forms

        WHERE active = TRUE

        AND
        (
            coffee_form_name ILIKE %s
            OR description ILIKE %s
        )

        ORDER BY coffee_form_name;
    """

    df = pd.read_sql(
        query,
        conn,
        params=(
            f"%{search}%",
            f"%{search}%"
        ),
    )

    conn.close()

    return df


def get_coffee_form(coffee_form_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT

            coffee_form_id,
            coffee_form_name,
            description,
            active

        FROM barrie.coffee_forms

        WHERE coffee_form_id = %s;
        """,
        (coffee_form_id,),
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return None

    return {
        "coffee_form_id": row[0],
        "coffee_form_name": row[1],
        "description": row[2],
        "active": row[3],
    }


# ======================================================
# UPDATE
# ======================================================

def update_coffee_form(
    coffee_form_id,
    coffee_form_name,
    description,
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE barrie.coffee_forms

        SET

            coffee_form_name = %s,
            description = %s

        WHERE coffee_form_id = %s;
        """,
        (
            coffee_form_name,
            description,
            coffee_form_id,
        ),
    )

    conn.commit()

    cur.close()
    conn.close()


# ======================================================
# DEACTIVATE
# ======================================================

def deactivate_coffee_form(coffee_form_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE barrie.coffee_forms

        SET

            active = FALSE

        WHERE coffee_form_id = %s;
        """,
        (coffee_form_id,),
    )

    conn.commit()

    cur.close()
    conn.close()


# ======================================================
# DROPDOWN
# ======================================================

def get_coffee_form_dropdown():

    conn = get_connection()

    query = """
        SELECT

            coffee_form_id,
            coffee_form_name

        FROM barrie.coffee_forms

        WHERE active = TRUE

        ORDER BY coffee_form_name;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df