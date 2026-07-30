from db import get_connection
import pandas as pd


####################################
# CREATE
####################################

def insert_farmer(first_name, last_name, phone, notes):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO barrie.farmers
        (
            first_name,
            last_name,
            phone,
            notes
        )
        VALUES (%s,%s,%s,%s)
        RETURNING farmer_code;
    """,
    (first_name,last_name,phone,notes))

    farmer_code = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return farmer_code


####################################
# READ
####################################

def get_all_farmers():

    conn = get_connection()

    query = """
    SELECT
        farmer_code AS "Code",
        first_name AS "First Name",
        last_name AS "Last Name",
        phone AS "Phone",
        active AS "active"
    FROM barrie.farmers
    ORDER BY farmer_id;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


####################################
# SEARCH
####################################

def search_farmers(search):

    conn = get_connection()

    query = """
    SELECT

        farmer_id,

        farmer_code,

        first_name,

        last_name,

        phone,

        active

    FROM barrie.farmers

    WHERE

        farmer_code ILIKE %s

        OR first_name ILIKE %s

        OR last_name ILIKE %s

        OR phone ILIKE %s

    ORDER BY farmer_id;
    """

    pattern = f"%{search}%"

    df = pd.read_sql(
        query,
        conn,
        params=(pattern,pattern,pattern,pattern)
    )

    conn.close()

    return df


####################################
# UPDATE
####################################

def update_farmer(
        farmer_id,
        first_name,
        last_name,
        phone,
        notes):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        UPDATE barrie.farmers

        SET

            first_name=%s,

            last_name=%s,

            phone=%s,

            notes=%s

        WHERE farmer_id=%s

    """,
    (
        first_name,
        last_name,
        phone,
        notes,
        farmer_id
    ))

    conn.commit()

    cur.close()

    conn.close()


####################################
# DEACTIVATE
####################################

def deactivate_farmer(farmer_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        UPDATE barrie.farmers

        SET active=FALSE

        WHERE farmer_id=%s

    """,
    (farmer_id,)
    )

    conn.commit()

    cur.close()

    conn.close()

def get_farm_locations():

    conn = get_connection()

    query = """
        SELECT

            farm_code,
            farm_name,
            gps_latitude,
            gps_longitude,
            organic,
            elevation_meters

        FROM barrie.farms

        WHERE
            gps_latitude IS NOT NULL
        AND
            gps_longitude IS NOT NULL

        ORDER BY farm_code;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df 

# ======================================================
# DROPDOWN
# ======================================================

def get_farmer_dropdown():

    conn = get_connection()

    query = """
        SELECT

            farmer_id,
            first_name || ' ' || last_name AS farmer_name

        FROM barrie.farmers

        WHERE active = TRUE

        ORDER BY
            first_name,
            last_name;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df   