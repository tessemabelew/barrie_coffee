import pandas as pd
from db import get_connection


def insert_farm(
    farmer_id,
    farm_name,
    farm_number,
    farm_size_hectares,
    elevation_meters,
    organic,
    notes,
    gps_latitude,
    gps_longitude,
    gps_accuracy
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO barrie.farms
        (
            farmer_id,
            farm_name,
            farm_number,
            farm_size_hectares,
            elevation_meters,
            organic,
            notes,
            gps_latitude,
            gps_longitude,
            gps_accuracy
        )

        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        RETURNING farm_code;
        """,
        (
            farmer_id,
            farm_name,
            farm_number,
            farm_size_hectares,
            elevation_meters,
            organic,
            notes,
            gps_latitude,
            gps_longitude,
            gps_accuracy
        )
    )

    farm_code = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return farm_code


def get_all_farms():

    conn = get_connection()

    query = """
        SELECT
            f.farm_id,
            f.farm_code,
            fm.farmer_code,
            fm.first_name || ' ' || fm.last_name AS farmer,
            f.farm_name,
            COALESCE(f.farm_number, '') AS farm_number,
            f.farm_size_hectares,
            f.elevation_meters,
            f.organic,
            f.gps_latitude,
            f.gps_longitude,
            f.gps_accuracy,
            f.active

        FROM barrie.farms f

        JOIN barrie.farmers fm
            ON f.farmer_id = fm.farmer_id

        ORDER BY f.farm_code;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def search_farms(search):

    conn = get_connection()

    query = """
        SELECT
            f.farm_id,
            f.farm_code,
            fm.farmer_code,
            fm.first_name || ' ' || fm.last_name AS farmer,
            f.farm_name,
            COALESCE(f.farm_number, '') AS farm_number,
            f.farm_size_hectares,
            f.elevation_meters,
            f.organic,
            f.gps_latitude,
            f.gps_longitude,
            f.gps_accuracy,
            f.active

        FROM barrie.farms f

        JOIN barrie.farmers fm
            ON f.farmer_id = fm.farmer_id

        WHERE

            f.farm_code ILIKE %s

            OR

            f.farm_name ILIKE %s

            OR

            fm.first_name ILIKE %s

            OR

            fm.last_name ILIKE %s

        ORDER BY f.farm_code;
    """

    value = f"%{search}%"

    df = pd.read_sql(
        query,
        conn,
        params=(value, value, value, value)
    )

    conn.close()

    return df


def get_farmer_dropdown():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT

            farmer_id,

            farmer_code || ' - ' ||
            first_name || ' ' ||
            last_name

        FROM barrie.farmers

        WHERE active = TRUE

        ORDER BY farmer_code;
        """
    )

    farmers = cur.fetchall()

    cur.close()
    conn.close()

    return farmers

def update_farm(
    farm_id,
    farm_name,
    farm_number,
    farm_size_hectares,
    elevation_meters,
    organic,
    notes
):

    # Convert NumPy/Pandas types to native Python types
    farm_id = int(farm_id)
    farm_size_hectares = float(farm_size_hectares)
    elevation_meters = int(elevation_meters)
    organic = bool(organic)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE barrie.farms

        SET

            farm_name=%s,
            farm_number=%s,
            farm_size_hectares=%s,
            elevation_meters=%s,
            organic=%s,
            notes=%s

        WHERE farm_id=%s;
        """,
        (
            farm_name,
            farm_number,
            farm_size_hectares,
            elevation_meters,
            organic,
            notes,
            farm_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()

def deactivate_farm(farm_id):

    # Convert NumPy/Pandas type to native Python int
    farm_id = int(farm_id)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE barrie.farms

        SET active = FALSE

        WHERE farm_id = %s;
        """,
        (farm_id,)
    )

    conn.commit()

    cur.close()
    conn.close()

def get_farm(farm_id):

    farm_id = int(farm_id)

    conn = get_connection()

    query = """
        SELECT *
        FROM barrie.farms
        WHERE farm_id = %s;
    """

    df = pd.read_sql(
        query,
        conn,
        params=(farm_id,)
    )

    conn.close()

    return df.iloc[0]  


def get_farm_locations():

    conn = get_connection()

    query = """
        SELECT
            farm_code,
            farm_name,
            gps_latitude,
            gps_longitude,
            elevation_meters,
            organic

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

def get_farm_dropdown():

    conn = get_connection()

    query = """
        SELECT
            farm_id,
            farm_name
        FROM barrie.farms
        WHERE active = TRUE
        ORDER BY farm_name;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df   